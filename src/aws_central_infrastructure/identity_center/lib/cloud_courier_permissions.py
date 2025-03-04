from pulumi_aws.iam import GetPolicyDocumentStatementArgs
from pulumi_aws.iam import GetPolicyDocumentStatementConditionArgs
from pulumi_aws.iam import get_policy_document

from .lib import UserInfo
from .permissions import AwsLogicalWorkload
from .permissions import AwsSsoPermissionSet
from .permissions import AwsSsoPermissionSetAccountAssignments
from .permissions import DefaultWorkloadPermissionAssignments


def create_read_permission_set() -> AwsSsoPermissionSet:
    cloud_courier_bucket_pattern = "raw-data*--cloud-courier--*"  # TODO: consider if it's worth tagging the bucket with a specific tag to make this less dependent on naming
    return AwsSsoPermissionSet(
        name="CloudCourierRawDataReadAccess",
        description="Read access to raw data files uploaded by Cloud Courier",
        inline_policy=get_policy_document(
            statements=[
                GetPolicyDocumentStatementArgs(
                    sid="ObjectLevelPermissions",
                    effect="Allow",
                    actions=[
                        "s3:GetObject",
                        "s3:GetObjectVersion",
                        "s3:GetObjectVersionAttributes",
                        "s3:GetObjectTagging",
                    ],
                    resources=[f"arn:aws:s3:::{cloud_courier_bucket_pattern}/*"],
                ),
                GetPolicyDocumentStatementArgs(
                    sid="BucketLevelPermissions",
                    effect="Allow",
                    actions=[
                        "s3:ListBucket",
                        "s3:ListBucketVersions",
                        "s3:ListTagsForResource",
                        "s3:GetBucketLocation",
                        "s3:GetBucketTagging",
                        "s3:GetBucketMetadataTableConfiguration",
                    ],
                    resources=[f"arn:aws:s3:::{cloud_courier_bucket_pattern}"],
                ),
                GetPolicyDocumentStatementArgs(  # TODO: remove this if we can get the SSO Permission Set Relay working better
                    sid="TopLevelS3Permissions",
                    effect="Allow",
                    actions=[
                        "s3:ListAllMyBuckets",
                    ],
                    resources=["*"],
                ),
                GetPolicyDocumentStatementArgs(
                    sid="ReadBucketMetrics",
                    effect="Allow",
                    actions=[
                        "cloudwatch:ListMetrics",
                    ],  # there doesn't appear to be a simple way to further lock down with RequestConditions
                    resources=["*"],
                ),
            ]
        ).json,
    )


def create_ssm_permission_set() -> AwsSsoPermissionSet:
    return AwsSsoPermissionSet(
        name="CloudCourierUploadAgentAdmin",
        description="Permissions to install, stop, start, and update the Cloud Courier Upload Agent running on the Lab computers.",
        inline_policy=get_policy_document(
            statements=[
                GetPolicyDocumentStatementArgs(
                    sid="TopLevelSsmPermissions",
                    effect="Allow",
                    actions=[
                        "ssm:ListCommands",
                        "ssm:ListAssociations",
                        "ssm:ListTagsForResource",  # this could be locked down further...but low risk
                    ],
                    resources=["*"],
                ),
                GetPolicyDocumentStatementArgs(
                    sid="SsmInstancePermissions",
                    effect="Allow",
                    actions=[
                        "ssm:ListInstanceAssociations",
                        "ssm:ListNodes",
                        "ssm:DescribeInstanceInformation",
                        "ssm:DescribeInstanceProperties",
                    ],
                    resources=["*"],
                ),
                GetPolicyDocumentStatementArgs(
                    sid="SsmDocumentPermissions",
                    effect="Allow",
                    actions=[
                        "ssm:ListDocumentMetadataHistory",
                        "ssm:ListDocuments",
                        "ssm:DescribeDocument",
                        "ssm:ListDocumentVersions",
                    ],
                    resources=["*"],
                    conditions=[
                        GetPolicyDocumentStatementConditionArgs(
                            test="StringEquals",
                            variable="aws:ResourceTag/pulumi-project-name",
                            values=["cloud-courier"],
                        ),
                    ],
                ),
            ]
        ).json,
    )


def create_cloud_courier_permissions(
    *,
    workload_info: AwsLogicalWorkload,
    end_users: list[UserInfo] | None = None,
    administrators: list[UserInfo] | None = None,
) -> None:
    read_access = create_read_permission_set()
    # Read access for end-users
    _ = AwsSsoPermissionSetAccountAssignments(
        account_info=workload_info.prod_accounts[0],
        permission_set=read_access,
        # TODO: add a relay to the S3 console for buckets....TBD what to do about region
        users=end_users,
    )

    _ = DefaultWorkloadPermissionAssignments(
        workload_info=workload_info,
        users=administrators,
    )
    ssm_access = create_ssm_permission_set()
    for protected_env_account in [
        *workload_info.prod_accounts,
        *workload_info.staging_accounts,
        *workload_info.dev_accounts,  # TODO: remove before merge
    ]:
        _ = AwsSsoPermissionSetAccountAssignments(
            account_info=protected_env_account,
            permission_set=ssm_access,
            users=administrators,
        )
