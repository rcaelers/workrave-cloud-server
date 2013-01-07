from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view, obj=None):
        if obj is None:
            return True

        return obj.owner == request.user
        
