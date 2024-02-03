from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt


from config.settings import JWTSettings
from models.users import User
from crud.users import UserCRUD
from schemas.auth import Token, SingUp
from schemas.users import UserResponse
from utils.token import create_access_token
from utils.hasher import Hasher

auth_router = APIRouter()


@auth_router.post("/login", response_model=Token)
async def login(
    user_crud: UserCRUD, form_data: OAuth2PasswordRequestForm = Depends()
) -> Token:
    user = await user_crud.authenticate(form_data.username, form_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    access_token = create_access_token(user.email)
    return Token(access_token=access_token, token_type="bearer")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    user_crud: UserCRUD, token: str = Depends(oauth2_scheme)
) -> User:
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

    user = await user_crud.get_by_email(email)
    if user is None:
        raise credentials_exception

    return user


@auth_router.post("/signup", response_model=UserResponse)
async def sing_up(data: SingUp, user_crud: UserCRUD) -> UserResponse:
    user = await user_crud.get_by_email(data.email)
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email {data.email} has already exists.",
        )

    new_user = await user_crud.create(
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        hashed_password=Hasher.get_hash_password(data.password),
    )
    return new_user
