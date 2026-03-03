from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsClient(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (request.user and request.user.is_authenticated and request.user.role == 'client')
    
class IsFreelancer(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (request.user and request.user.is_authenticated and request.user.role == 'freelancer')
    
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (request.user and request.user.is_authenticated and request.user.role == 'admin')