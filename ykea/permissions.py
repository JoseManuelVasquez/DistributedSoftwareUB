from rest_framework import permissions

# This permission allow commercial group to POST, PUT and DELETE
class IsCommercialOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True

        perm_group = False
        for group in request.user.groups.all():
            perm_group = group.name == "Commercial"
            if perm_group:
                break

        return (
                request.user and
                request.user.is_authenticated and
                perm_group
        )