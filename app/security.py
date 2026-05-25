from functools import wraps
from flask import abort
from flask_login import current_user


def roles_required(*roles):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(403)

            if current_user.role not in roles:
                abort(403)

            return function(*args, **kwargs)
        return wrapper
    return decorator


def same_org_or_404(model, object_id):
    obj = model.query.filter_by(id=object_id, organizacao_id=current_user.organizacao_id).first_or_404()
    return obj
