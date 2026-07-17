# ============== WARNING ==============================================================================
# File is managed by copier template: gh:LabAutomationAndScreening/copier-aws-central-infrastructure.git
# See .config/.copier-managed-files.json for details.
#
# You are welcome to make changes to this file in your repo if they are custom to your project,
# but if the change should be shared with other projects, please backport it to the template repo.
# =====================================================================================================
from .constants import CENTRAL_INFRA_GITHUB_ORG_NAME
from .constants import CENTRAL_INFRA_REPO_NAME
from .github_oidc_lib import CODE_ARTIFACT_SERVICE_BEARER_STATEMENT
from .github_oidc_lib import ECR_AUTH_STATEMENT
from .github_oidc_lib import ECR_PULL_STATEMENT
from .github_oidc_lib import GITHUB_OIDC_URL
from .github_oidc_lib import PULL_FROM_CENTRAL_ECRS_STATEMENTS
from .github_oidc_lib import GithubOidcConfig
from .github_oidc_lib import create_oidc_assume_role_policy
from .github_oidc_lib import create_oidc_for_single_account_workload
from .github_oidc_lib import create_oidc_for_standard_workload
from .github_oidc_lib import infra_deploy_role_name
from .github_oidc_lib import infra_preview_role_name
from .github_oidc_lib import principal_in_org_condition
from .pulumi_bootstrap import create_classic_providers
from .pulumi_bootstrap import create_providers
from .workload_params import get_management_account_id
from .workload_params import load_workload_info
