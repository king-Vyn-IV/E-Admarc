from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def superuser_required(user):
    """Return True if the user is a superuser, otherwise raise PermissionDenied."""
    if not user.is_authenticated:
        return False
    if not user.is_superuser:
        raise PermissionDenied
    return True
