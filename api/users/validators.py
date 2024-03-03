import re

from fastapi import HTTPException, status
from pydantic import field_validator

LETTERS_PATTERN = re.compile(r"[a-zA-Zа-яА-Я\-]+$")


class UserFieldsValidator:
    @field_validator("first_name")
    def validate_first_name(value):
        if not LETTERS_PATTERN.match(value):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="First name should contains only letters",
            )
        return value

    @field_validator("last_name")
    def validate_last_name(value):
        if not LETTERS_PATTERN.match(value):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Last name should contains only letters",
            )
        return value
