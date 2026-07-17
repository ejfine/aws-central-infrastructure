# ============== WARNING ==============================================================================
# File is managed by copier template: gh:LabAutomationAndScreening/copier-aws-central-infrastructure.git
# See .config/.copier-managed-files.json for details.
#
# You are welcome to make changes to this file in your repo if they are custom to your project,
# but if the change should be shared with other projects, please backport it to the template repo.
# =====================================================================================================
from .lib import ROOT_GITHUB_ADMIN_USERNAME
from .lib import GithubOrgMembers
from .lib import GithubTeamConfig


def define_team_configs(
    *,
    configs: list[GithubTeamConfig],  # noqa: ARG001 # temp
    dev_sec_ops_team_config: GithubTeamConfig,
) -> GithubOrgMembers:
    """Create the configurations for the repositories.

    example: `configs.append(GithubTeamConfig(name="Manhattan Project Team", description="Working on something big"))`
    """
    _ = dev_sec_ops_team_config  # this line can be removed once any adjustments have been made to the DevSecOps team config
    org_members = GithubOrgMembers(org_admins=[ROOT_GITHUB_ADMIN_USERNAME])
    org_members.everyone.extend(["zendern", "idonaldson"])

    return org_members
