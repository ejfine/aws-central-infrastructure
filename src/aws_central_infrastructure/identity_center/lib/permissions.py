from typing import Any
from typing import override

from pulumi import ComponentResource
from pulumi import ResourceOptions
from pulumi_aws import identitystore as identitystore_classic
from pulumi_aws import ssoadmin
from pydantic import BaseModel

from aws_central_infrastructure.iac_management.lib.shared_lib import AwsAccountInfo
from aws_central_infrastructure.iac_management.lib.shared_lib import AwsLogicalWorkload

from .lib import ORG_INFO
from .lib import UserAttributes
from .lib import Username

_all_users: dict[Username, UserAttributes] = {}


def lookup_user_id(username: Username) -> str:
    """Convert a username name into an AWS SSO User ID."""
    return identitystore_classic.get_user(
        alternate_identifier=identitystore_classic.GetUserAlternateIdentifierArgs(
            unique_attribute=identitystore_classic.GetUserAlternateIdentifierUniqueAttributeArgs(
                attribute_path="UserName", attribute_value=username
            )
        ),
        identity_store_id=ORG_INFO.identity_store_id,
    ).user_id


class AwsSsoPermissionSet(ComponentResource):
    def __init__(self, *, name: str, description: str, managed_policies: list[str], inline_policy: str | None = None):
        super().__init__("labauto:AwsSsoPermissionSet", name, None)
        self.name = name
        permission_set = ssoadmin.PermissionSet(
            name,
            instance_arn=ORG_INFO.sso_instance_arn,
            name=name,
            description=description,
            session_duration="PT12H",
            opts=ResourceOptions(parent=self),
        )
        self.permission_set_arn = permission_set.arn
        for policy_name in managed_policies:
            _ = ssoadmin.ManagedPolicyAttachment(
                f"{name}-{policy_name}",
                instance_arn=ORG_INFO.sso_instance_arn,
                managed_policy_arn=f"arn:aws:iam::aws:policy/{policy_name}",
                permission_set_arn=self.permission_set_arn,
                opts=ResourceOptions(parent=self),
            )
        if inline_policy is not None:
            _ = ssoadmin.PermissionSetInlinePolicy(
                f"{name}-inline-policy",
                instance_arn=ORG_INFO.sso_instance_arn,
                permission_set_arn=self.permission_set_arn,
                inline_policy=inline_policy,
                opts=ResourceOptions(parent=self),
            )
        self.register_outputs(
            {
                "permission_set_arn": self.permission_set_arn,
            }
        )


class AwsSsoPermissionSetContainer(BaseModel):
    name: str
    description: str
    managed_policies: list[str]
    _permission_set: AwsSsoPermissionSet | None = None

    def create_permission_set(self, inline_policy: str | None = None) -> AwsSsoPermissionSet:
        self._permission_set = AwsSsoPermissionSet(
            name=self.name,
            description=self.description,
            managed_policies=self.managed_policies,
            inline_policy=inline_policy,
        )
        return self._permission_set

    @property
    def permission_set(self) -> AwsSsoPermissionSet:
        assert self._permission_set is not None
        return self._permission_set


LOW_RISK_ADMIN_PERM_SET_CONTAINER = AwsSsoPermissionSetContainer(
    name="LowRiskAccountAdminAccess",
    description="Low Risk Account Admin Access",
    managed_policies=["AdministratorAccess"],
)

VIEW_ONLY_PERM_SET_CONTAINER = AwsSsoPermissionSetContainer(
    name="ViewOnlyAccess",
    description="The ability to view logs and other resource details in protected environments for troubleshooting.",
    managed_policies=[
        "AWSSupportAccess",  # Allow users to request AWS support for technical questions.
        "job-function/ViewOnlyAccess",  # wide ranging attribute view access across a variety of services
        "CloudWatchReadOnlyAccess",  # be able to read CloudWatch logs/metrics/etc
        "AmazonAppStreamReadOnlyAccess",  # look at the details of stack/fleet information to troubleshoot any issues
        "AmazonSSMReadOnlyAccess",  # look at SSM fleet/hybrid activation details
        "AWSLambda_ReadOnlyAccess",  # review traces and logs for debugging Lambdas easily through the console
        "CloudWatchEventsReadOnlyAccess",  # see information about event rules and patterns
        "AmazonEventBridgeReadOnlyAccess",  # see basic metrics about Event Bridges to troubleshoot
        "AmazonEventBridgeSchemasReadOnlyAccess",  # look at basic metrics about EventBridge Schemas to troubleshoot
        "AmazonEC2ContainerRegistryReadOnly",  # describe ECR images
    ],
)


class AwsSsoPermissionSetAccountAssignments(ComponentResource):
    def __init__(
        self,
        *,
        account_info: AwsAccountInfo,
        permission_set: AwsSsoPermissionSet,
        users: list[str],
    ):
        resource_name = f"{permission_set.name}-{account_info.name}"
        super().__init__(
            "labauto:AwsSsoPermissionSetAccountAssignments",
            resource_name,
            None,
        )
        users = list(set(users))  # Remove any duplicates in the list

        for user in users:
            _ = ssoadmin.AccountAssignment(
                f"{resource_name}-{user}",
                instance_arn=ORG_INFO.sso_instance_arn,
                permission_set_arn=permission_set.permission_set_arn,
                principal_id=lookup_user_id(user),
                principal_type="USER",
                target_id=account_info.id,
                target_type="AWS_ACCOUNT",
                opts=ResourceOptions(parent=self),
            )


class DefaultWorkloadPermissionAssignments(BaseModel):
    workload_info: AwsLogicalWorkload
    users: list[str]

    @override
    def model_post_init(self, _: Any) -> None:
        for protected_env_account in [*self.workload_info.prod_accounts, *self.workload_info.staging_accounts]:
            _ = AwsSsoPermissionSetAccountAssignments(
                account_info=protected_env_account,
                permission_set=VIEW_ONLY_PERM_SET_CONTAINER.permission_set,
                users=self.users,
            )
        for unprotected_env_account in self.workload_info.dev_accounts:
            _ = AwsSsoPermissionSetAccountAssignments(
                account_info=unprotected_env_account,
                permission_set=LOW_RISK_ADMIN_PERM_SET_CONTAINER.permission_set,
                users=self.users,
            )
