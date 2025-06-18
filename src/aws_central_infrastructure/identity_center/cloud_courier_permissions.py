from lab_auto_pulumi import AwsLogicalWorkload

from .lib import all_created_users
from .lib.cloud_courier_permissions import create_cloud_courier_permissions


def configure_cloud_courier_permissions(*, workload_info: AwsLogicalWorkload) -> None:
    create_cloud_courier_permissions(
        workload_info=workload_info,
        end_users=[all_created_users["ejfine@gmail.com"]],
        administrators=[all_created_users["ejfine@gmail.com"]],
    )
