import re

from pydantic import EmailStr

from .base import BaseScheme
from .validators import UserFieldsValidator


LETTERS_PATTERN = re.compile(r"[a-zA-Zа-яА-Я\-]+$")


class Token(BaseScheme):
    access_token: str
    token_type: str


class SingUp(UserFieldsValidator, BaseScheme):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
