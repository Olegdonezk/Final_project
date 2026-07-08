from rest_framework.permissions import BasePermission


class IsLandlord(BasePermission):
    """
    Доступ только для арендодателей.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "landlord"
        )


class IsTenant(BasePermission):
    """
    Доступ только для арендаторов.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "tenant"
        )