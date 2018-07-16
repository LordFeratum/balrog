class RoleNotFoundException(Exception):
    pass


class ResourceNotFoundException(Exception):
    pass


class OperationNotFoundException(Exception):
    pass


class PermissionDenied(Exception):
    def __init__(self, message="Permission Denied!"):
        super().__init__(message)
