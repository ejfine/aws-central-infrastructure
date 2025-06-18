from lab_auto_pulumi import AwsLogicalWorkload

from .lib import LOW_RISK_ADMIN_PERM_SET_CONTAINER
from .lib import AwsSsoPermissionSetAccountAssignments
from .lib import DefaultWorkloadPermissionAssignments
from .lib import all_created_users
from .lib import create_org_admin_permissions


def create_permissions(workloads_dict: dict[str, AwsLogicalWorkload]) -> None:
    admin_permission_set = LOW_RISK_ADMIN_PERM_SET_CONTAINER.permission_set

    _ = AwsSsoPermissionSetAccountAssignments(
        account_info=workloads_dict["central-infra"].prod_accounts[0],
        permission_set=admin_permission_set,
        users=[all_created_users["ejfine@gmail.com"]],
    )
    _ = AwsSsoPermissionSetAccountAssignments(
        account_info=workloads_dict["biotasker"].dev_accounts[0],
        permission_set=admin_permission_set,
        users=[all_created_users["ejfine@gmail.com"]],
    )
    _ = AwsSsoPermissionSetAccountAssignments(
        account_info=workloads_dict["identity-center"].prod_accounts[0],
        permission_set=admin_permission_set,
        users=[all_created_users["ejfine@gmail.com"]],
    )

    create_org_admin_permissions(workloads_dict=workloads_dict, users=[all_created_users["ejfine@gmail.com"]])

    _ = DefaultWorkloadPermissionAssignments(
        workload_info=workloads_dict["elifine-com"],
        users=[all_created_users["ejfine@gmail.com"]],
    )
    _ = AwsSsoPermissionSetAccountAssignments(
        account_info=workloads_dict["elifine-com"].prod_accounts[0],
        permission_set=admin_permission_set,
        users=[all_created_users["ejfine@gmail.com"]],
    )
