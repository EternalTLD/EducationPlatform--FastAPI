"""Project models"""
import re
import uuid

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, field_validator


LETTERS_PATTERN = re.compile(r"[a-zA-Zа-яА-Я\-]+$")


class TunedModel(BaseModel):
    class Config:
        orm_mode = True


class ShowUser(TunedModel):
    id: uuid.UUID
    first_name: str
    last_name: str
    email: EmailStr
    is_active: bool


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

    @field_validator("first_name")
    def validate_first_name(value):
        if not LETTERS_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="First name should contains only letters"
            )
        return value

    @field_validator("last_name")
    def validate_last_name(value):
        if not LETTERS_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Last name should contains only letters"
            )
        return value
