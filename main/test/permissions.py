from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

def is_admin(user):
    """True if user is an admin"""
    return user.is_authenticated and user.groups.filter(name="Editor").exists()

def admin_required(view_func):
    """Admin may pass. Everyone else logged in gets 403."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not (request.user.is_superuser):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return login_required(login_url="/login/")(wrapper)