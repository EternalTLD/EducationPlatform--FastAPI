import re

from pydantic import EmailStr

from base.schemas import BaseSchema

from ..users.validators import UserFieldsValidator

LETTERS_PATTERN = re.compile(r"[a-zA-Zа-яА-Я\-]+$")


class TokenSchema(BaseSchema):
    access_token: str
    token_type: str


class SingUpSchema(UserFieldsValidator, BaseSchema):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
