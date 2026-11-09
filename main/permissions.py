from rest_framework.permissions import BasePermission, SAFE_METHODS


def is_editor(user):
    """True if the user belongs to the 'Editor' group (assigned via Django Admin)."""
    return user.is_authenticated and user.groups.filter(name="Editor").exists()


class IsPortfolioOwnerOrReadOnly(BasePermission):
    message = "Only the portfolio owner can change projects."

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_superuser
        )

class IsPortfolioOwnerOrEditorOrReadOnly(BasePermission):
    message = "You do not have permission to perform this action."
    
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return (
            request.method in ("PUT", "PATCH")
            and is_editor(request.user)
        )