from pulumi_aws.iam import GetPolicyDocumentStatementArgs
from pulumi_aws.iam import get_policy_document

from aws_central_infrastructure.iac_management.lib import AwsLogicalWorkload

from .lib import AwsSsoPermissionSet
from .lib import AwsSsoPermissionSetAccountAssignments
from .lib import DefaultWorkloadPermissionAssignments
from .lib import UserInfo
from .lib import all_created_users


def _create_read_permission_set() -> AwsSsoPermissionSet:
    cloud_courier_bucket_pattern = "raw-data*--cloud-courier--*"  # TODO: consider if it's worth tagging the bucket with a specific tag to make this less dependent on naming
    return AwsSsoPermissionSet(
        name="CloudCourierRawDataReadAccess",
        description="Read access to raw data files uploaded by Cloud Courier",
        inline_policy=get_policy_document(
            statements=[
                GetPolicyDocumentStatementArgs(
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
            ]
        ).json,
    )


def create_cloud_courier_permissions(*, workload_info: AwsLogicalWorkload) -> None:
    read_access = _create_read_permission_set()
    # Read access for end-users
    _ = AwsSsoPermissionSetAccountAssignments(
        account_info=workload_info.prod_accounts[0],
        permission_set=read_access,
        users=[all_created_users["eli.fine"]],
    )

    cloud_courier_administrators: list[UserInfo] = [all_created_users["eli.fine"]]
    _ = DefaultWorkloadPermissionAssignments(
        workload_info=workload_info,
        users=cloud_courier_administrators,
    )
