from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Faqat post egasi tahrirlash va o'chirish huquqiga ega.
    Boshqalar faqat o'qishi mumkin.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user



class IsCommentOwnerOrReadOnly(permissions.BasePermission):
    """
    Faqat comment egasi tahrirlashi va o'chirishi mumkin.
    Boshqalar faqat o'qishi mumkin.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user