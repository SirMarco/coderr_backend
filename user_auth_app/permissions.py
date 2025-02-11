from rest_framework import permissions
from rest_framework.permissions import BasePermission

class OrderPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if request.method == "POST":
            return getattr(request.user.profile, "type", None) == "customer"

        return True


    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if request.method == 'PATCH':
            return getattr(request.user.profile, "type", None) == 'business'
        
        if request.method == 'DELETE':
            return request.user.is_staff or obj.customer_user == request.user
        
        return False
    
class IsBusinessUser(BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        profile = getattr(request.user, 'profile', None)
        return bool(profile and profile.type == "business")

class IsCustomerUser(BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        profile = getattr(request.user, 'profile', None)
        return bool(profile and profile.type == "customer") 