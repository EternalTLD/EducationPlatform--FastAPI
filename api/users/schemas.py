import uuid
from typing import Optional

from pydantic import EmailStr

from base.schemas import BaseSchema

from .validators import UserFieldsValidator


class UserResponseSchema(BaseSchema):
    id: uuid.UUID
    first_name: str
    last_name: str
    email: EmailStr
    is_active: bool


class UserUpdateSchema(UserFieldsValidator, BaseSchema):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
