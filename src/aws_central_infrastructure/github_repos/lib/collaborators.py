# ============== WARNING ==============================================================================
# File is managed by copier template: gh:LabAutomationAndScreening/copier-aws-central-infrastructure.git
# See .config/.copier-managed-files.json for details.
#
# You are welcome to make changes to this file in your repo if they are custom to your project,
# but if the change should be shared with other projects, please backport it to the template repo.
# =====================================================================================================
from pulumi import ResourceOptions
from pulumi_github import Provider
from pulumi_github import RepositoryCollaborator
from pydantic import BaseModel
from pydantic import Field

from .teams import GithubRepositoryPermission
from .teams import RepositoryName


class RepositoryCollaboratorConfig(BaseModel):
    username: str
    description: str
    repo_permissions: dict[RepositoryName, GithubRepositoryPermission] = Field(default_factory=dict)


def create_repository_collaborators(*, configs: list[RepositoryCollaboratorConfig], provider: Provider) -> None:
    for config in configs:
        for repo_name, permission in config.repo_permissions.items():
            _ = RepositoryCollaborator(
                f"{config.username}-{repo_name}",
                repository=repo_name,
                username=config.username,
                permission=permission,
                opts=ResourceOptions(provider=provider),
            )
