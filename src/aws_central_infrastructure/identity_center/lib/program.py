import logging

from ephemeral_pulumi_deploy import get_aws_account_id
from ephemeral_pulumi_deploy import get_config
from pulumi import export

from aws_central_infrastructure.iac_management.lib.workload_params import load_workload_info

from ..cloud_courier_permissions import configure_cloud_courier_permissions
from ..permissions import create_permissions
from ..users import create_users
from .permissions import LOW_RISK_ADMIN_PERM_SET_CONTAINER
from .permissions import MANUAL_SECRETS_ENTRY_PERM_SET_CONTAINER
from .permissions import VIEW_ONLY_PERM_SET_CONTAINER

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
    _ = LOW_RISK_ADMIN_PERM_SET_CONTAINER.create_permission_set()
    _ = MANUAL_SECRETS_ENTRY_PERM_SET_CONTAINER.create_permission_set()
    _ = VIEW_ONLY_PERM_SET_CONTAINER.create_permission_set()
    create_permissions(workloads_dict)

    # Application-specific permissions managed by copier template
    configure_cloud_courier_permissions(workload_info=workloads_dict["cloud-courier"])
