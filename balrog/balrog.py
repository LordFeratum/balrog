from functools import update_wrapper, partial
from itertools import chain

from balrog.repositories import OnMemoryRepository
from balrog.exceptions import PermissionDenied



class Balrog:
    def __init__(self, repository=None, default=None):
        self._default = default
        self._repository = repository or OnMemoryRepository()

    def add_role(self, role, inheritance=None):
        self._repository.add_role(role, inheritance=inheritance)

    def add_resource(self, resource):
        self._repository.add_resource(resource)

    def allow(self, role, operation, resource, allowance=True):
        self._repository.add_policy(role, operation, resource, allowance)

    def deny(self, role, operation, resource, allowance=False):
        self._repository.add_policy(role, operation, resource, allowance)

    def is_allowed(self, role, operation, resource):
        repeated = []
        queue = []
        queue.append(role)
        repeated.append(role)
        
        while len(queue) > 0:
            _role = queue.pop(0)
            policy = self._repository.get_policy(_role, operation, resource)
            if policy is None:
                for inherited in self._repository.get_role_inheritance(_role):
                    if inherited not in repeated:
                        queue.append(inherited)

            else:
                return policy

        return self._default


class IdentityContext:
    def __init__(self, balrog, role_loaders=None):
        self._balrog = balrog
        self._role_loaders = role_loaders or []

    def role_loader(self, loader):
        self._role_loaders.append(loader())

    def get_roles(self):
        return chain.from_iterable(self._role_loaders)

    def check(self, operation, resource, exception=None, **exc_kwargs):
        exception = exception or PermissionDenied
        checker = partial(self._check, operation, resource)
        return Context(checker, exception=exception, **exc_kwargs)

    def _check(self, operation, resource):
        for role in self.get_roles():
            value = self._balrog.is_allowed(role, operation, resource)
            if value is not None:
                return value

        return self._balrog._default


class Context:
    def __init__(self, checker, exception=Exception, **exc_kwargs):
        self._exception = exception
        self._in_context = False
        self._checker = checker
        self._exc_kwargs = exc_kwargs

    def __call__(self, wrapped):
        def wrapper(*args, **kwargs):
            with self:
                return wrapped(*args, **kwargs)

        return update_wrapper(wrapper, wrapped)

    def __enter__(self):
        self._in_context = True
        self.check()
        return self

    def __exit__(self, exception_type, exception, traceback):
        self._in_context = False

    def __bool__(self):
        return bool(self._checker())

    def check(self):
        if self._checker():
            return True

        raise self._exception(**self._exc_kwargs)
