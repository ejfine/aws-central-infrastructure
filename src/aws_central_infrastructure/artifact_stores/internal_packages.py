from .lib import RepoPackageClaims


def create_internal_packages_configs(repo_package_claims: list[RepoPackageClaims]) -> None:
    """Create the internal packages configurations.

    Example: repo_package_claims.append(RepoPackageClaims(repo_name="cloud-courier", pypi_package_names={"cloud-courier"}))
    """
    repo_package_claims.append(
        RepoPackageClaims(
            repo_name="lab-auto-pulumi", pypi_package_names={"lab-auto-pulumi"}, publish_to_public_registry=True
        )
    )
    repo_package_claims.append(
        RepoPackageClaims(
            repo_name="ephemeral-pulumi-deploy",
            pypi_package_names={"ephemeral-pulumi-deploy"},
            publish_to_public_registry=True,
        )
    )
    repo_package_claims.append(
        RepoPackageClaims(repo_name="pyalab", pypi_package_names={"pyalab"}, publish_to_public_registry=True)
    )
    repo_package_claims.append(
        RepoPackageClaims(
            repo_name="local-files-fastapi", pypi_package_names={"local-files-fastapi"}, publish_to_public_registry=True
        )
    )
