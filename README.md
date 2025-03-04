[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Checked with pyright](https://microsoft.github.io/pyright/img/pyright_badge.svg)](https://microsoft.github.io/pyright/)
[![Actions status](https://www.github.com/ejfine/aws-central-infrastructure/actions/workflows/ci.yaml/badge.svg?branch=main)](https://www.github.com/ejfine/aws-central-infrastructure/actions)
[![Open in Dev Containers](https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://www.github.com/ejfine/aws-central-infrastructure)


# Usage
To create a new repository using this template:
1. Install `copier` and `copier-templates-extensions`. An easy way to do that is to copy the `.devcontainer/install-ci-tooling.sh` script in this repository into your new repo and then run it.
2. Run copier to instantiate the template: `copier copy --trust gh:LabAutomationAndScreening/copier-aws-central-infrastructure.git`
3. Run `uv lock` to generate the lock file
4. Commit the changes
5. Rebuild your new devcontainer



# Development

## Using Pulumi
Run a Pulumi Preview for the IaC Management project: `uv run python -m aws_central_infrastructure.deploy_iac_management --stack=prod`
Run a Pulumi Preview for the Artifact Stores project: `uv run python -m aws_central_infrastructure.deploy_artifact_stores --stack=prod`
Run a Pulumi Preview for the Identity Center project: `uv run python -m aws_central_infrastructure.deploy_identity_center --stack=prod`


## Updating from the template
This repository uses a copier template. To pull in the latest updates from the template, use the command:
`copier update --trust --conflict rej --defaults`
