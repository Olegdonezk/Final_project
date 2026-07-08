from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """
    Разрешает просмотр всем.
    Изменение и удаление только владельцу объявления.
    """

    def has_object_permission(self, request, view, obj):

        # GET, HEAD, OPTIONS доступны всем
        if request.method in SAFE_METHODS:
            return True

        # PATCH, PUT, DELETE только владельцу
        return obj.owner == request.user