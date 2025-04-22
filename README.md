[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Checked with pyright](https://microsoft.github.io/pyright/img/pyright_badge.svg)](https://microsoft.github.io/pyright/)
[![Actions status](https://www.github.com/ejfine/aws-central-infrastructure/actions/workflows/ci.yaml/badge.svg?branch=main)](https://www.github.com/ejfine/aws-central-infrastructure/actions)
[![Open in Dev Containers](https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://www.github.com/ejfine/aws-central-infrastructure)


# Usage

## Allowing a git repository to publish a package to AWS CodeArtifact
The file `src/aws_central_infrastructure/artifact_stores/internal_packages.py` contains a list of repositories that are allowed to publish packages to the AWS CodeArtifact registry. To enable a new repository to do so, add a new entry to the `repo_package_claims` list. This ensures that only one git repo has permission to publish that package, and there's no conflicts of two repos overwriting each other's packages.
At the moment, only Python packages are supported. See https://github.com/LabAutomationAndScreening/copier-aws-central-infrastructure/issues/22 and https://github.com/LabAutomationAndScreening/copier-aws-central-infrastructure/issues/21

## Allowing a git repository to publish a docker image to AWS Elastic Container Registry
The file `src/aws_central_infrastructure/artifact_stores/container_registries.py` contains a list of repositories that are allowed to publish images to an AWS ECR. To create a new ECR that a repository can publish to, add a new entry to the `container_registries` list. This ensures that only one git repo has permission to publish to that ECR, and there's no conflicts of two repos overwriting each other's images.


# Development

## Using Pulumi
Run a Pulumi Preview for the IaC Management project:
```bash
uv run python -m aws_central_infrastructure.iac_management.lib.pulumi_deploy --stack=prod
```

Run a Pulumi Preview for the Artifact Stores project:
```bash
uv run python -m aws_central_infrastructure.artifact_stores.lib.pulumi_deploy --stack=prod
```

Run a Pulumi Preview for the Central Networking project:
```bash
uv run python -m aws_central_infrastructure.central_networking.lib.pulumi_deploy --stack=prod
```

Run a Pulumi Preview for the Identity Center project:
```bash
uv run python -m aws_central_infrastructure.identity_center.lib.pulumi_deploy --stack=prod
```


## Updating from the template
This repository uses a copier template. To pull in the latest updates from the template, use the command:
`copier update --trust --conflict rej --defaults`
