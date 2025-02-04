import logging

import boto3
from ephemeral_pulumi_deploy import get_aws_account_id
from ephemeral_pulumi_deploy import get_config
from ephemeral_pulumi_deploy import get_config_str
from pulumi import export
from pulumi_aws.iam import GetPolicyDocumentStatementArgs
from pulumi_aws.iam import GetPolicyDocumentStatementConditionArgs
from pulumi_aws.iam import GetPolicyDocumentStatementPrincipalArgs
from pulumi_aws.iam import get_policy_document
from pulumi_aws.organizations import get_organization
from pulumi_aws_native import s3

from .shared_lib import WORKLOAD_INFO_SSM_PARAM_PREFIX
from .shared_lib import AwsLogicalWorkload

logger = logging.getLogger(__name__)


def create_bucket_policy(bucket_name: str) -> str:
    org_id = get_organization().id
    return get_policy_document(
        statements=[
            GetPolicyDocumentStatementArgs(
                effect="Allow",
                principals=[
                    GetPolicyDocumentStatementPrincipalArgs(
                        type="*",
                        identifiers=["*"],  # Allows all principals
                    )
                ],
                actions=["s3:PutObject", "s3:GetObject", "s3:DeleteObject"],
                resources=[f"arn:aws:s3:::{bucket_name}/${{aws:PrincipalAccount}}/*"],
                conditions=[
                    GetPolicyDocumentStatementConditionArgs(
                        test="StringEquals",
                        variable="aws:PrincipalOrgID",
                        values=[org_id],  # Limit to the AWS Organization
                    ),
                ],
            ),
            GetPolicyDocumentStatementArgs(
                effect="Allow",
                principals=[GetPolicyDocumentStatementPrincipalArgs(type="*", identifiers=["*"])],
                actions=["s3:ListBucket"],
                resources=[f"arn:aws:s3:::{bucket_name}"],
                conditions=[
                    GetPolicyDocumentStatementConditionArgs(
                        test="StringEquals", variable="aws:PrincipalOrgID", values=[org_id]
                    ),
                    GetPolicyDocumentStatementConditionArgs(
                        test="StringLike", variable="s3:prefix", values=["${aws:PrincipalAccount}/*"]
                    ),
                ],
            ),
        ]
    ).json


def pulumi_program() -> None:
    """Execute creating the stack."""
    aws_account_id = get_aws_account_id()
    export("aws-account-id", aws_account_id)
    env = get_config("proj:env")
    export("env", env)

    # Create Resources Here
    organization_home_region = "us-east-1"
    central_state_bucket_name = get_config_str("proj:backend_bucket_name")
    _ = s3.BucketPolicy(
        "bucket-policy",
        bucket=central_state_bucket_name,
        policy_document=create_bucket_policy(central_state_bucket_name),
    )

    ssm_client = boto3.client("ssm", region_name=organization_home_region)

    parameters = []
    next_token = None

    while True:
        # API call with optional pagination
        response = ssm_client.describe_parameters(
            ParameterFilters=[{"Key": "Name", "Option": "BeginsWith", "Values": [WORKLOAD_INFO_SSM_PARAM_PREFIX]}],
            MaxResults=50,  # AWS allows up to 50 results per call
            NextToken=next_token if next_token else "",
        )

        # Add parameters from this page
        parameters.extend(response.get("Parameters", []))

        # Check if more pages exist
        next_token = response.get("NextToken")
        if not next_token:
            break

    def get_parameter_value(name: str) -> str:
        response = ssm_client.get_parameter(
            Name=name,
        )
        return response["Parameter"]["Value"]

    param_values: list[str] = []
    for param in parameters:
        param_name = param["Name"]
        param_value = get_parameter_value(param_name)
        param_values.append(param_value)

    workloads_info = [AwsLogicalWorkload.model_validate_json(param) for param in param_values]

    # for workload_info in workloads_info:
    #     all_accounts = [*workload_info.prod_accounts, *workload_info.staging_accounts, *workload_info.dev_accounts]
    #     for account in all_accounts:
    #         deploy_role_arn = f"arn:aws:iam::{account.id}:role/InfraDeploy--{CENTRAL_INFRA_REPO_NAME}"

    #         assume_role = ProviderAssumeRoleArgs(role_arn=central_infra_role_arn, session_name="pulumi")
    #         central_infra_provider = Provider(
    #             f"{central_infra_account_name}",
    #             assume_role=assume_role,
    #             allowed_account_ids=[central_infra_account.account.id],
    #             region="us-east-1",
    #             opts=ResourceOptions(
    #                 parent=central_infra_account,
    #             ),
    #         )
