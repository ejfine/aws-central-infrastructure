from lab_auto_pulumi import AwsLogicalWorkload
from lab_auto_pulumi import all_created_users

from .lib import LOW_RISK_ADMIN_PERM_SET_CONTAINER
from .lib import MANUAL_ARTIFACTS_UPLOAD_PERM_SET_CONTAINER
from .lib import AwsSsoPermissionSetAccountAssignments
from .lib import DefaultWorkloadPermissionAssignments
from .lib import create_org_admin_permissions


def create_permissions(workloads_dict: dict[str, AwsLogicalWorkload]) -> None:
    admin_permission_set = LOW_RISK_ADMIN_PERM_SET_CONTAINER.permission_set

    _ = AwsSsoPermissionSetAccountAssignments(
        account_info=workloads_dict["central-infra"].prod_accounts[0],
        permission_set=admin_permission_set,
        users=[all_created_users["eli.fine"]],
    )
    _ = AwsSsoPermissionSetAccountAssignments(
        account_info=workloads_dict["biotasker"].dev_accounts[0],
        permission_set=admin_permission_set,
        users=[all_created_users["eli.fine"]],
    )
    _ = AwsSsoPermissionSetAccountAssignments(
        account_info=workloads_dict["identity-center"].prod_accounts[0],
        permission_set=admin_permission_set,
        users=[all_created_users["eli.fine"]],
    )

    create_org_admin_permissions(workloads_dict=workloads_dict, users=[all_created_users["eli.fine"]])

    _ = DefaultWorkloadPermissionAssignments(
        workload_info=workloads_dict["elifine-com"],
        users=[all_created_users["eli.fine"]],
    )
    _ = AwsSsoPermissionSetAccountAssignments(
        account_info=workloads_dict["elifine-com"].prod_accounts[0],
        permission_set=admin_permission_set,
        users=[all_created_users["eli.fine"]],
    )

    _ = DefaultWorkloadPermissionAssignments(
        workload_info=workloads_dict["rytermedia-com"],
        users=[all_created_users["eli.fine"]],
    )
    _ = AwsSsoPermissionSetAccountAssignments(
        account_info=workloads_dict["rytermedia-com"].prod_accounts[0],
        permission_set=admin_permission_set,
        users=[all_created_users["eli.fine"]],
    )
    _ = AwsSsoPermissionSetAccountAssignments(
        account_info=workloads_dict["rytermedia-com"].prod_accounts[0],
        permission_set=MANUAL_ARTIFACTS_UPLOAD_PERM_SET_CONTAINER.permission_set,
        users=[all_created_users["eli.fine"], all_created_users["ethanryter3@gmail.com"]],
    )
