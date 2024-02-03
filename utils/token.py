from datetime import datetime, timedelta

from jose import jwt

from config.settings import JWTSettings


def create_access_token(subject: str, expire_delta_minutes: int = None) -> str:
    if expire_delta_minutes is None:
        expire_at = datetime.utcnow() + timedelta(
            minutes=JWTSettings().ACCESS_TOKEN_EXPIRE_MINUTES
        )
    else:
        expire_at = datetime.utcnow() + timedelta(minutes=expire_delta_minutes)

    to_encode = {"exp": expire_at, "sub": subject}
    encoded_jwt = jwt.encode(
        to_encode,
        JWTSettings().SECRET_KEY,
        JWTSettings().ALGORITHM,
    )
    return encoded_jwt
