from rest_framework.permissions import BasePermission

class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return request.user.is_superuser
        else:
            return False
    
class IsPartner(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        elif request.user.is_partner:
            return request.user.is_partner
        else:
            return False
        
class IsUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        elif not request.user.is_partner:
            return True
        else:
            return False