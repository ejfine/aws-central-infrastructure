from .lib import GithubRepoConfig


def create_repo_configs(configs: list[GithubRepoConfig]):
    """Create the configurations for the repositories.

    example: `configs.append(GithubRepoConfig(name="test-pulumi-repo", description="blah"))`
    """
    # Append repos to the list here
    configs.append(
        GithubRepoConfig(
            name="lab-auto-pulumi",
            description="Pulumi helper functions and other resources for use with Cloud Infrastructure created using tooling within this Organization",
            org_admin_rule_bypass=True,
            visibility="public",
        )
    )
    configs.append(
        GithubRepoConfig(
            name="ephemeral-pulumi-deploy",
            description="Be able to easy spin up and down ephemeral Pulumi stacks",
            org_admin_rule_bypass=True,
            visibility="public",
        )
    )
