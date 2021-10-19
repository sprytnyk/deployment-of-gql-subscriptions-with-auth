from functools import wraps

from django.http import JsonResponse

from app.utils import decode_jwt_token


def jwt_auth(view_func):
    """Wraps a view with required JWT authentication and tries to get auth
    header from a request."""

    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        request = args[0]
        auth_token = request.headers.get('Authorization', '').split(' ')[-1]
        valid_token = decode_jwt_token(auth_token)
        if valid_token:
            return view_func(*args, **kwargs)

        return JsonResponse(
            data={'Authorization': 'Invalid or wrong token.'},
            status=403
        )

    return wrapped_view
