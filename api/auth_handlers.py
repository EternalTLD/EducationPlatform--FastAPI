from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt

from api.models import Token
from api.utils import Hasher
from db.models import User
from db.session import get_db_session
from db.dals import UserDAL
from security import create_access_token
import settings

auth_router = APIRouter()


async def authenticate_user(
    email: str, password: str, db_session: AsyncSession
) -> User | None:
    user_dal = UserDAL(db_session)
    user = await user_dal.get_user_by_email(email)
    if user is None:
        return
    if not Hasher.verify_password(password, user.hashed_password):
        return
    return user


@auth_router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db_session: AsyncSession = Depends(get_db_session),
) -> Token:
    user = await authenticate_user(form_data.username, form_data.password, db_session)
    if user is None:
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    access_token_expire = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        {"sub": user.email}, expire_delta=access_token_expire
    )
    return Token(access_token=access_token, token_type="bearer")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def get_user_credentials(
    token: str = Depends(oauth2_scheme),
    db_session: AsyncSession = Depends(get_db_session),
):
    credentials_exception = HTTPException(
        status_code=401, detail="Could not validate credentials"
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user_dal = UserDAL(db_session)
    user = await user_dal.get_user_by_email(email)
    if user is None:
        raise credentials_exception

    return user
