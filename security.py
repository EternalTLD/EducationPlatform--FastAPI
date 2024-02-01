import datetime

from jose import jwt

import settings


def create_access_token(data: dict, expire_delta: datetime.timedelta) -> str:
    to_encode = data.copy()
    expire_at = datetime.datetime.utcnow() + expire_delta
    to_encode.update({"exp": expire_at})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt
