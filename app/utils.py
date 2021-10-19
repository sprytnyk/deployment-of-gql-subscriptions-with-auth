import jwt
from django.conf import settings
from jwt.exceptions import PyJWTError


def decode_jwt_token(token: str) -> dict:
    """Decodes a JWT token and returns its data."""

    try:
        data = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=settings.SIMPLE_JWT['ALGORITHM']
        )

        return data
    except PyJWTError:
        return {}
