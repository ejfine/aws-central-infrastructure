from aws_central_infrastructure.iac_management.lib import AwsLogicalWorkload

from .lib import all_created_users
from .lib.cloud_courier_permissions import create_cloud_courier_permissions


def configure_cloud_courier_permissions(*, workload_info: AwsLogicalWorkload) -> None:
    create_cloud_courier_permissions(
        workload_info=workload_info,
        end_users=[all_created_users["eli.fine"]],
        administrators=[all_created_users["eli.fine"]],
    )
