from .lib import GithubRepoConfig


def create_repo_configs(configs: list[GithubRepoConfig]):
    """Create the configurations for the repositories.

    example: `configs.append(GithubRepoConfig(name="test-pulumi-repo", description="blah"))`
    """
    # Append repos to the list here
    configs.append(
        GithubRepoConfig(
            name=".github",
            description="Public information about the Organization",
            org_admin_rule_bypass=True,
            visibility="public",
        )
    )
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
            name="nuxt-ui-test-utils",
            description="Helper functions for test suites involving @nuxt/ui components",
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
    configs.append(
        GithubRepoConfig(
            name="pyalab",
            description="Library for generating Integra ViaLab files",
            org_admin_rule_bypass=True,
            visibility="public",
        )
    )
    configs.append(
        GithubRepoConfig(
            name="cloud-courier",
            description="The executable agent that uploads files from a computer to the cloud",
            org_admin_rule_bypass=True,
            visibility="public",
        )
    )
    configs.append(
        GithubRepoConfig(
            name="copier-aws-central-infrastructure",
            description="Template for creating central shared infrastructure for an AWS Organization",
            org_admin_rule_bypass=True,
            delete_branch_on_merge=False,
            visibility="public",
        )
    )
    configs.append(
        GithubRepoConfig(
            name="copier-nuxt-python-intranet-app",
            description="A web app that is hosted within a local intranet. Nuxt frontend, python backend, docker-compose",
            org_admin_rule_bypass=True,
            delete_branch_on_merge=False,
            visibility="public",
        )
    )
    configs.append(
        GithubRepoConfig(
            name="copier-python-package-template",
            description="A copier template for Python libraries or executables",
            org_admin_rule_bypass=True,
            delete_branch_on_merge=False,
            visibility="public",
        )
    )
    configs.append(
        GithubRepoConfig(
            name="copier-vue-package-template",
            description="A copier template for TS/VueJS/Nuxt libraries",
            org_admin_rule_bypass=True,
            delete_branch_on_merge=False,
            visibility="public",
        )
    )
    configs.append(
        GithubRepoConfig(
            name="copier-base-template",
            description="A copier template used to create other copier templates",
            org_admin_rule_bypass=True,
            delete_branch_on_merge=False,
            visibility="public",
        )
    )
    configs.append(
        GithubRepoConfig(
            name="copier-aws-organization",
            description="A template to create a repo to manage an AWS Organization",
            org_admin_rule_bypass=True,
            delete_branch_on_merge=False,
            visibility="public",
        )
    )
    configs.append(
        GithubRepoConfig(
            name="copier-pulumi-project",
            description="Template for a Pulumi Project that is just creating infrastructure (no application code / Lambdas)",
            org_admin_rule_bypass=True,
            delete_branch_on_merge=False,
            visibility="public",
        )
    )
    configs.append(
        GithubRepoConfig(
            name="copier-nuxt-static-aws",
            description="Template for creating a Static Website using Nuxt frontend hosted on AWS",
            org_admin_rule_bypass=True,
            delete_branch_on_merge=False,
            visibility="public",
        )
    )
    configs.append(
        GithubRepoConfig(
            name="copier-cloud-courier-infrastructure",
            description="Template for creating the Infrastructure to deploy and configure Cloud Courier",
            org_admin_rule_bypass=True,
            delete_branch_on_merge=False,
            visibility="public",
        )
    )
    configs.append(
        GithubRepoConfig(
            name="biotasker",
            description="Track tasks for biological experiments with non-deterministic timelines",
            org_admin_rule_bypass=True,
            visibility="public",
        )
    )
