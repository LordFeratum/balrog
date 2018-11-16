import re

from balrog.exceptions import (
    RoleNotFoundException,
    ResourceNotFoundException,
    OperationNotFoundException,
)


def get_resource_regex(resource):
    return '^{}$'.format(resource)


class OnMemoryRepository:
    def __init__(self):
        self._roles = {}
        self._resources = set()

        self._policies = {}

    def add_role(self, role, inheritance=None):
        inheritance = inheritance or []
        if role not in self._roles.keys():
            self._roles[role] = []

        for inherint_role in inheritance:
            if inherint_role not in self._roles:
                msg = "Role '{}' not found.".format(inherint_role)
                raise RoleNotFoundException(msg)

            self._roles[role].append(inherint_role)

    def add_resource(self, resource):
        self._resources.add(resource)

    def add_policy(self, role, operation, resource, allowance):
        if role not in self._roles:
            raise RoleNotFoundException("Role '{}' not found.".format(role))

        if resource not in self._resources:
            msg = "Resource '{}' not found.".format(resource)
            raise ResourceNotFoundException(msg)

        self._policies.setdefault((role, operation), [])
        self._policies[(role, operation)].append((resource, allowance))

    def get_roles(self):
        return self._roles.keys()

    def get_role_inheritance(self, role):
        if role not in self._roles:
            raise RoleNotFoundException("Role '{}' not found.".format(role))

        return self._roles[role]

    def get_resources(self):
        return self._resources

    def get_policy(self, role, operation, resource):
        found = False
        resources = self._policies.get((role, operation), [])
        for resource_regex, allowance in resources:
            p = re.compile(get_resource_regex(resource_regex), re.IGNORECASE)
            if p.match(resource) is not None:
                found = True
                if allowance is False:
                    return False
        
        if found:
            return True

        return None
