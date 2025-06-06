import logging

from ephemeral_pulumi_deploy import get_aws_account_id
from ephemeral_pulumi_deploy import get_config
from pulumi import export

from aws_central_infrastructure.iac_management.lib.workload_params import load_workload_info

from ..cloud_courier_permissions import configure_cloud_courier_permissions
from ..users import create_users
from .create_permissions import create_all_permissions
from .permissions import ALL_PERM_SET_CONTAINERS

logger = logging.getLogger(__name__)


def pulumi_program() -> None:
    """Execute creating the stack."""
    env = get_config("proj:env")
    export("env", env)
    aws_account_id = get_aws_account_id()
    export("aws-account-id", aws_account_id)

    # Create Resources Here
    workloads_dict, _ = load_workload_info(exclude_central_infra_workload=False)
    # Note: If you are directly creating users (and not using your external SSO Identity Provider), you must create any new users and deploy them before you can assign any permissions to them (otherwise the Preview will fail)
    create_users()
    for perm_set_container in ALL_PERM_SET_CONTAINERS:
        _ = perm_set_container.create_permission_set()

    create_all_permissions(workloads_dict)

    # Application-specific permissions managed by copier template
    configure_cloud_courier_permissions(workload_info=workloads_dict["cloud-courier"])
