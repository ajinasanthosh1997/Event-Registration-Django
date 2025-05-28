from django.core.exceptions import PermissionDenied

def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def jeweler_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not hasattr(request.user, 'jewelerprofile'):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view
