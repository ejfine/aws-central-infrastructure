# ============== WARNING ==============================================================================
# File is managed by copier template: gh:LabAutomationAndScreening/copier-aws-central-infrastructure.git
# See .config/.copier-managed-files.json for details.
#
# You are welcome to make changes to this file in your repo if they are custom to your project,
# but if the change should be shared with other projects, please backport it to the template repo.
# =====================================================================================================
from .lib import EcrConfig


def define_container_registries(container_registries: list[EcrConfig]) -> None:
    """Create container registries (e.g. ECRs) to share across the organization or within a workload.

    Example:
    container_registries.append(
        EcrConfig(
            git_repo_name="cool-repo",
            ecr_repo_name="backend",
            ecr_repo_namespace="my-project",
        )
    )
    """
