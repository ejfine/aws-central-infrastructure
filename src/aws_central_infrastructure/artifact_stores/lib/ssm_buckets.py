import logging

from ephemeral_pulumi_deploy import append_resource_suffix
from ephemeral_pulumi_deploy import common_tags_native
from pulumi import ComponentResource
from pulumi import ResourceOptions
from pulumi_aws.iam import GetPolicyDocumentStatementArgs
from pulumi_aws.iam import GetPolicyDocumentStatementConditionArgs
from pulumi_aws.iam import GetPolicyDocumentStatementPrincipalArgs
from pulumi_aws.iam import get_policy_document
from pulumi_aws.organizations import get_organization
from pulumi_aws_native import s3

logger = logging.getLogger(__name__)


class ManualArtifactsBucket(ComponentResource):
    def __init__(
        self,
    ):
        super().__init__("labauto:ManualArtifactsBucket", append_resource_suffix(), None)
        # These artifacts are deployed to machines and devices. It's too much of a security risk to let people overwrite them, so setting up WORM.
        self.bucket = s3.Bucket(
            append_resource_suffix("manual-artifacts"),
            versioning_configuration=s3.BucketVersioningConfigurationArgs(
                status=s3.BucketVersioningConfigurationStatus.ENABLED
            ),
            object_lock_enabled=True,
            object_lock_configuration=s3.BucketObjectLockConfigurationArgs(
                object_lock_enabled="Enabled",
                rule=s3.BucketObjectLockRuleArgs(
                    default_retention=s3.BucketDefaultRetentionArgs(
                        mode=s3.BucketDefaultRetentionMode.GOVERNANCE, years=10
                    )
                ),
            ),
            opts=ResourceOptions(parent=self),
            tags=common_tags_native(),
        )
        org_id = get_organization().id
        _ = s3.BucketPolicy(
            "bucket-policy",
            bucket=self.bucket.bucket_name,  # type: ignore[reportArgumentType] # pyright somehow thinks a bucket name can be Output[None], which doesn't seem possible
            policy_document=get_policy_document(
                statements=[
                    GetPolicyDocumentStatementArgs(
                        effect="Allow",
                        actions=["s3:PutObject", "s3:GetObject", "s3:ListBucket"],
                        principals=[
                            GetPolicyDocumentStatementPrincipalArgs(
                                type="*",
                                identifiers=[
                                    "*"
                                ],  # Anyone can do anything with this bucket if they themselves have been granted permission. WORM model keeps files secure.
                            )
                        ],
                        resources=["*"],
                        conditions=[
                            GetPolicyDocumentStatementConditionArgs(
                                test="StringEquals",
                                variable="aws:PrincipalOrgID",
                                values=[org_id],  # Limit to the AWS Organization
                            ),
                        ],
                    ),
                ]
            ).json,
        )
