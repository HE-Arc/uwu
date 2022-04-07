from pickle import FALSE
from rest_framework.permissions import BasePermission, SAFE_METHODS

class ChapterPermission(BasePermission):
    
    def has_permission(self, request, view):
        if request.user.is_staff: 
            return True
        
        if view.action == "add_remove_to_read" and request.user.is_authenticated:
            return True
        
            
        return request.method in SAFE_METHODS
        
class FriendRequestPermission(BasePermission):
    
    def has_permission(self, request, view):
        is_auth = request.user.is_authenticated
        if request.user.is_staff: 
            return True
        
        if is_auth:
            if view.action == "get_active_friend_request" or view.action == "accept" or view.action == "cancel" or view.action == "decline" or request.method in SAFE_METHODS:
                return True
        
            
        return False