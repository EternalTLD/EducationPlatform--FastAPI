from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt


from config.settings import JWTSettings
from db.models import User
from db.session import get_db_session
from db.dals import UserDAL
from api.schemas.auth import Token, SingUp
from api.schemas.users import UserResponse
from .utils import Hasher, create_access_token

auth_router = APIRouter()


async def authenticate_user(
    email: str, password: str, session: AsyncSession
) -> User | None:
    user_dal = UserDAL(session)
    user = await user_dal.get_user_by_email(email)
    if user is None or not Hasher.verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    return user


@auth_router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_db_session),
) -> Token:
    user = await authenticate_user(form_data.username, form_data.password, session)
    access_token = create_access_token(user.email)
    return Token(access_token=access_token, token_type="bearer")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_db_session),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    try:
        payload = jwt.decode(
            token, JWTSettings().SECRET_KEY, algorithms=[JWTSettings().ALGORITHM]
        )
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user_dal = UserDAL(session)
    user = await user_dal.get_user_by_email(email)
    if user is None:
        raise credentials_exception

    return user


@auth_router.post("/signup", response_model=UserResponse)
async def sing_up(
    data: SingUp, session: AsyncSession = Depends(get_db_session)
) -> UserResponse:
    user = await UserDAL(session).get_user_by_email(data.email)
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email {data.email} has already exists.",
        )

    new_user = await UserDAL(session).create_user(
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        password=Hasher.get_hash_password(data.password),
    )
    return new_user
