# ============== WARNING ==============================================================================
# File is managed by copier template: gh:LabAutomationAndScreening/copier-aws-central-infrastructure.git
# See .config/.copier-managed-files.json for details.
#
# You are welcome to make changes to this file in your repo if they are custom to your project,
# but if the change should be shared with other projects, please backport it to the template repo.
# =====================================================================================================
from .code_artifact import RepoPackageClaims
from .ecr import EcrConfig
from .external_creds import EXTERNAL_CREDS_SECRET_PREFIX
from .external_creds import EcrRepo
from .external_creds import ExternalCredConfig
from .image_builder import ImageBuilderConfig
from .image_builder import ImageShareConfig
from .image_builder import NewImageConfig
