from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from rest_framework.permissions import BasePermission, SAFE_METHODS


def is_editor(user):
    """True if the user belongs to the 'Editor' group (assigned via Django Admin)."""
    return user.is_authenticated and user.groups.filter(name="Editor").exists()


def owner_required(view_func):
    """Not logged in -> redirect to login. Logged in but not superuser -> 403."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return login_required(login_url="/login/")(wrapper)


def editor_or_owner_required(view_func):
    """Superuser or Editor may pass. Everyone else logged in gets 403."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not (request.user.is_superuser or is_editor(request.user)):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return login_required(login_url="/login/")(wrapper)

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