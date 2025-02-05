from ..iac_management.shared_lib import AwsLogicalWorkload
from .lib import AwsSsoPermissionSet
from .lib import AwsSsoPermissionSetAccountAssignments


def create_permissions(workloads_dict: dict[str, AwsLogicalWorkload]) -> None:
    admin_permission_set = AwsSsoPermissionSet(
        name="LowRiskAccountAdminAccess",
        description="Low Risk Account Admin Access",
        managed_policies=["AdministratorAccess"],
    )

    _ = AwsSsoPermissionSetAccountAssignments(
        account_info=workloads_dict["central-infra"].prod_accounts[0],
        permission_set=admin_permission_set,
        users=["eli.fine"],
    )
    _ = AwsSsoPermissionSetAccountAssignments(
        account_info=workloads_dict["biotasker"].dev_accounts[0],
        permission_set=admin_permission_set,
        users=["eli.fine"],
    )
    _ = AwsSsoPermissionSetAccountAssignments(
        account_info=workloads_dict["identity-center"].prod_accounts[0],
        permission_set=admin_permission_set,
        users=["eli.fine"],
    )
