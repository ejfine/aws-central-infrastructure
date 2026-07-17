# ============== WARNING ==============================================================================
# File is managed by copier template: gh:LabAutomationAndScreening/copier-aws-central-infrastructure.git
# See .config/.copier-managed-files.json for details.
#
# You are welcome to make changes to this file in your repo if they are custom to your project,
# but if the change should be shared with other projects, please backport it to the template repo.
# =====================================================================================================
from lab_auto_pulumi import AwsLogicalWorkload
from lab_auto_pulumi import all_created_users

from .lib.cloud_courier_permissions import create_cloud_courier_permissions


def configure_cloud_courier_permissions(*, workload_info: AwsLogicalWorkload) -> None:
    create_cloud_courier_permissions(
        workload_info=workload_info,
        end_users=[all_created_users["eli.fine"]],
        administrators=[all_created_users["eli.fine"]],
    )
