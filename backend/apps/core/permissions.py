from rest_framework.permissions import BasePermission

class IsLandlord(BasePermission):
    """
    Allows access only to authenticated users with the LANDLORD role.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            getattr(request.user, 'role', None) == 'LANDLORD'
        )

class IsTenant(BasePermission):
    """
    Allows access only to authenticated users with the TENANT role.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            getattr(request.user, 'role', None) == 'TENANT'
        )