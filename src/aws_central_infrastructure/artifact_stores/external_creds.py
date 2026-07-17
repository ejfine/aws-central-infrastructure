# ============== WARNING ==============================================================================
# File is managed by copier template: gh:LabAutomationAndScreening/copier-aws-central-infrastructure.git
# See .config/.copier-managed-files.json for details.
#
# You are welcome to make changes to this file in your repo if they are custom to your project,
# but if the change should be shared with other projects, please backport it to the template repo.
# =====================================================================================================
from .lib import EcrRepo  # noqa: F401  # used in docstring example
from .lib import ExternalCredConfig


def define_external_creds(external_creds: list[ExternalCredConfig]) -> None:
    """Define IAM users with static credentials for external organizations.

    Example:
    external_creds.append(
        ExternalCredConfig(
            organization="acme-corp",
            description="Acme Corp Jenkins CI — pulls images for on-prem deployment pipeline",
            ecr_repos=[
                EcrRepo(name="orchestrator-health-app/backend"),
            ],
        )
    )
    """
