from .lib import ROOT_GITHUB_ADMIN_USERNAME
from .lib import GithubOrgMembers
from .lib import GithubTeamConfig


def define_team_configs(
    *, configs: list[GithubTeamConfig], dev_sec_ops_team_config: GithubTeamConfig
) -> GithubOrgMembers:
    """Create the configurations for the repositories.

    example: `configs.append(GithubTeamConfig(name="Manhattan Project Team", description="Working on something big"))`
    """
    _ = dev_sec_ops_team_config  # this line can be removed once any adjustments have been made to the DevSecOps team config
    org_members = GithubOrgMembers(org_admins=[ROOT_GITHUB_ADMIN_USERNAME])
    org_members.everyone.extend(["zendern"])
    configs.append(
        GithubTeamConfig(
            name="Copier Templates",
            description="Copier Templates Team",
            members=["ejfine", "zendern"],
            repo_permissions={
                "copier-base-template": "push",
                "copier-aws-organization": "push",
                "copier-aws-central-infrastructure": "push",
                "copier-python-package-template": "push",
                "copier-pulumi-project": "push",
                "copier-nuxt-python-intranet-app": "push",
                "copier-nuxt-static-aws": "push",
            },
        )
    )
    configs.append(
        GithubTeamConfig(
            name="Pulumi Libraries",
            description="Copier Templates Team",
            members=["ejfine", "zendern"],
            repo_permissions={
                "ephemeral-pulumi-deploy": "push",
                "lab-auto-pulumi": "push",
            },
        )
    )
    return org_members
