from rest_framework.permissions import BasePermission


class IsManager(BasePermission):
    message = "No authority to make this action"

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated() and request.user.is_manager


class IsCrew(BasePermission):
    message = "No authority to make this action"

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated() and request.user.is_crew
