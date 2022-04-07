from pickle import FALSE
from rest_framework.permissions import BasePermission, SAFE_METHODS

class ChapterPermission(BasePermission):
    
    def has_permission(self, request, view):
        if request.user.is_staff: 
            return True
        
        if view.action == 'add_remove_to_read' and request.user.is_authenticated:
            return True
        
            
        return request.method in SAFE_METHODS
        
class FriendRequestPermission(BasePermission):
    
    def has_permission(self, request, view):
        is_auth = request.user.is_authenticated
        if not is_auth:
            return False
        
        if request.user.is_staff: 
            return True
        
        return view.action in ['get_active_friend_request', 'accept', 'cancel', 'decline'] or request.method in SAFE_METHODS
    
    def has_object_permission(self, request, view, obj):
        pass
    
class MangaPermission(BasePermission):
    
    def has_permission(self, request, view):
        is_admin = request.user.is_staff
        is_auth = request.user.is_authenticated
        
        if is_admin:
            return True
        
        if view.action == 'add_remove_fav':
            return is_auth
        
        if view.action == 'get_chapters' or request.method in SAFE_METHODS:
            return True
        
        return False
    
class UserPermission(BasePermission):
    
    def has_permission(self, request, view):
        is_admin = request.user.is_staff
        is_auth = request.user.is_authenticated
        
        if is_admin:
            return True
        
        if view.action in ['list', 
                           'create', 
                           'retrieve', 
                           'get_favorites', 
                           'get_friends', 
                           'get_readed', 
                           'get_readed_mangas',
                           'total_pages_readed',]:
            return True
        
        return view.action in ['is_admin', 'my_user', 'ask_friend', 'is_friend', 'unfriend'] and is_auth
        