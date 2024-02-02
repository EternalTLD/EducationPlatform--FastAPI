import uuid
from typing import Optional

from pydantic import EmailStr, constr

from .base import BaseScheme
from .validators import UserFieldsValidator


class UserResponse(BaseScheme):
    id: uuid.UUID
    first_name: str
    last_name: str
    email: EmailStr
    is_active: bool


class UserUpdate(UserFieldsValidator, BaseScheme):
    first_name: Optional[constr(min_length=1)] = None
    last_name: Optional[constr(min_length=1)] = None
    email: Optional[EmailStr] = None
