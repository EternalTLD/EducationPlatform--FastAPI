from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

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


pwd_context = CryptContext(schemes=["bcrypt"])


class Hasher:
    @staticmethod
    def get_hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
