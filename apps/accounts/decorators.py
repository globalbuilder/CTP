# apps/accounts/decorators.py

from django.core.exceptions import PermissionDenied
from functools import wraps

def user_is_role(user_role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.user_type == user_role:
                return view_func(request, *args, **kwargs)
            else:
                raise PermissionDenied
        return _wrapped_view
    return decorator

student_required = user_is_role('student')
supervisor_required = user_is_role('supervisor')
training_unit_head_required = user_is_role('head')
