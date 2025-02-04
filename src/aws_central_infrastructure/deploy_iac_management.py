import logging
from typing import Any

from ephemeral_pulumi_deploy import run_cli
from pulumi.automation import ConfigValue

from .iac_management.program import pulumi_program

logger = logging.getLogger(__name__)


def generate_stack_config() -> dict[str, Any]:
    """Generate the stack configuration."""
    stack_config: dict[str, Any] = {}
    stack_config["proj:pulumi_project_name"] = "iac-management"
    github_repo_name = "aws-central-infrastructure"
    stack_config["proj:github_repo_name"] = github_repo_name

    stack_config["proj:git_repository_url"] = ConfigValue(value=f"https://github.com/ejfine/{github_repo_name}")
    return stack_config


def main() -> None:
    run_cli(stack_config=generate_stack_config(), pulumi_program=pulumi_program)


if __name__ == "__main__":
    main()
