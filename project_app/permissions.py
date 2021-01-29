from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, AllowAny


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff==True:
            return True


class IsOwn(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class UserPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action in ['create','update','destroy']:
            return request.user.is_authenticated and request.user.is_staff
        if view.action in ['retrieve', 'list']:
            return True
        else:
            return True

