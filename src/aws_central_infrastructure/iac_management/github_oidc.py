# ============== WARNING ==============================================================================
# File is managed by copier template: gh:LabAutomationAndScreening/copier-aws-central-infrastructure.git
# See .config/.copier-managed-files.json for details.
#
# You are welcome to make changes to this file in your repo if they are custom to your project,
# but if the change should be shared with other projects, please backport it to the template repo.
# =====================================================================================================
from lab_auto_pulumi import AwsLogicalWorkload
from lab_auto_pulumi import WorkloadName

from .lib import CENTRAL_INFRA_GITHUB_ORG_NAME
from .lib import GithubOidcConfig
from .lib import create_oidc_for_standard_workload


def generate_oidc(
    *,
    workloads_info: dict[WorkloadName, AwsLogicalWorkload],
    all_oidc: dict[WorkloadName, list[GithubOidcConfig]],
) -> None:
    # create OIDC here
    workload_name = "elifine-com"
    all_oidc[workload_name].extend(
        create_oidc_for_standard_workload(
            workload_info=workloads_info[workload_name],
            repo_org=CENTRAL_INFRA_GITHUB_ORG_NAME,
            repo_name="elifine-com",
        )
    )
    workload_name = "rytermedia-com"
    all_oidc[workload_name].extend(
        create_oidc_for_standard_workload(
            workload_info=workloads_info[workload_name],
            repo_org=CENTRAL_INFRA_GITHUB_ORG_NAME,
            repo_name="rytermedia-com",
        )
    )
