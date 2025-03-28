import logging

from ephemeral_pulumi_deploy import get_aws_account_id
from ephemeral_pulumi_deploy import get_config
from lab_auto_pulumi import AwsLogicalWorkload
from pulumi import export
from pulumi_aws.iam import GetPolicyDocumentStatementArgs
from pulumi_aws.iam import GetPolicyDocumentStatementConditionArgs
from pulumi_aws.iam import get_policy_document

from aws_central_infrastructure.iac_management.lib.workload_params import load_workload_info

from ..cloud_courier_permissions import configure_cloud_courier_permissions
from ..permissions import create_permissions
from ..users import create_users
from .lib import all_created_users
from .permissions import ALL_PERM_SET_CONTAINERS
from .permissions import AwsSsoPermissionSet
from .permissions import AwsSsoPermissionSetAccountAssignments

logger = logging.getLogger(__name__)


def create_all_permissions(workloads_dict: dict[str, AwsLogicalWorkload]):
    create_permissions(workloads_dict)
    core_infra_base_access = AwsSsoPermissionSet(
        name="CoreInfraBaseAccess",
        description="Base access everyone should have for the Central/Core Infrastructure Account",
        inline_policy=get_policy_document(
            statements=[
                GetPolicyDocumentStatementArgs(
                    effect="Allow",
                    actions=["sts:GetServiceBearerToken"],
                    resources=["*"],
                    conditions=[
                        GetPolicyDocumentStatementConditionArgs(
                            test="StringEquals", variable="sts:AWSServiceName", values=["codeartifact.amazonaws.com"]
                        )
                    ],
                ),
            ]
        ).json,
    )

    _ = AwsSsoPermissionSetAccountAssignments(
        account_info=workloads_dict["central-infra"].prod_accounts[0],
        permission_set=core_infra_base_access,
        users=list(all_created_users.values()),
    )


def pulumi_program() -> None:
    """Execute creating the stack."""
    env = get_config("proj:env")
    export("env", env)
    aws_account_id = get_aws_account_id()
    export("aws-account-id", aws_account_id)

    # Create Resources Here
    workloads_dict, _ = load_workload_info(exclude_central_infra_workload=False)
    # Note: If you are directly creating users (and not using your external SSO Identity Provider), you must create any new users and deploy them before you can assign any permissions to them (otherwise the Preview will fail)
    create_users()
    for perm_set_container in ALL_PERM_SET_CONTAINERS:
        _ = perm_set_container.create_permission_set()

    create_all_permissions(workloads_dict)

    # Application-specific permissions managed by copier template
    configure_cloud_courier_permissions(workload_info=workloads_dict["cloud-courier"])
