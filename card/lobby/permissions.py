from rest_framework import permissions
from rest_framework.throttling import UserRateThrottle

class IsPlayer(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user and not request.user.is_staff and request.user.is_authenticated():
            return True
        return False

class IsIdentifiedPlayer(permissions.BasePermission):

    def has_permission(self, request, view):
        if (request.user 
            and not request.user.is_staff 
            and request.user.is_authenticated()
            and request.session["is_identified"]):
            return True
        return False

class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user and request.user.is_staff and request.user.is_authenticated():
            return True
        return False

class IsSuperuser(permissions.BasePermission):

    def has_permission(self, request, view):
        if (request.user and request.user.is_superuser and
            request.user.is_authenticated()):
            return True
        return False

class AuthenticatedPlayer(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated()


class User3SecRateThrottle(UserRateThrottle):
    rate = '3/sec'
    scope = 'seconds'

class User5SecRateThrottle(UserRateThrottle):
    rate = '5/sec'
    scope = 'seconds'

class User1SecRateThrottle(UserRateThrottle):
    rate = '1/sec'
    scope = 'seconds'

class User3MinRateThrottle(UserRateThrottle):
    rate = '3/min'
    scope = 'minutes'
