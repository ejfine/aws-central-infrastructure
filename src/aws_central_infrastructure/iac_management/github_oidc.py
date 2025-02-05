from collections import defaultdict

from ..constants import CENTRAL_INFRA_GITHUB_ORG_NAME
from ..constants import CENTRAL_INFRA_REPO_NAME
from .github_oidc_lib import GithubOidcConfig
from .github_oidc_lib import WorkloadName
from .github_oidc_lib import create_oidc_for_single_account_workload
from .github_oidc_lib import create_oidc_for_standard_workload
from .shared_lib import AwsLogicalWorkload


def generate_all_oidc(
    *, workloads_info: dict[WorkloadName, AwsLogicalWorkload]
) -> dict[WorkloadName, list[GithubOidcConfig]]:
    all_oidc: dict[WorkloadName, list[GithubOidcConfig]] = defaultdict(list)

    workload_name = "identity-center"
    identity_center_workload = workloads_info[workload_name]
    all_oidc[workload_name].extend(
        create_oidc_for_single_account_workload(
            aws_account_id=identity_center_workload.prod_accounts[0].id,
            repo_org=CENTRAL_INFRA_GITHUB_ORG_NAME,
            repo_name=CENTRAL_INFRA_REPO_NAME,
            role_name_suffix="identity-center",
        )
    )

    workload_name = "cloud-courier"
    cloud_courier_workload = workloads_info[workload_name]
    all_oidc[workload_name].extend(
        create_oidc_for_standard_workload(
            workload_info=cloud_courier_workload,
            repo_org=CENTRAL_INFRA_GITHUB_ORG_NAME,
            repo_name="cloud-courier-infrastructure",
        )
    )

    return all_oidc
