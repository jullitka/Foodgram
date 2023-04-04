from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user.is_staff)
    

class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, serializer):
        return (request.method in SAFE_METHODS
                or serializer.author == request.user)