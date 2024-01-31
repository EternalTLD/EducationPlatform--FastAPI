"""Project models"""
import re
import uuid
import datetime
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, field_validator, constr


LETTERS_PATTERN = re.compile(r"[a-zA-Zа-яА-Я\-]+$")


class TunedModel(BaseModel):
    class Config:
        from_attributes = True


class ShowUser(TunedModel):
    id: uuid.UUID
    first_name: str
    last_name: str
    email: EmailStr
    is_active: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime


class DeleteUser(TunedModel):
    id: uuid.UUID
    is_active: bool


class CreateUser(TunedModel):
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


class UpdateUser(TunedModel):
    first_name: Optional[constr(min_length=1)] = None
    last_name: Optional[constr(min_length=1)] = None
    email: Optional[EmailStr] = None

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
