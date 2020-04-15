from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: Optional[str] = None
    disabled: Optional[bool] = None


# Shared properties in Mongodb
class UserBaseInDB(UserBase):
    full_name: Optional[str] = None


# Additional properties stored in DB
class UserInDB(UserBaseInDB):
    hashed_password: str


# Properties to receive via API on creation
class UserCreate(UserBaseInDB):
    password: str
    disabled: bool = False


# Properties to receive via API on update
class UserUpdate(UserBaseInDB):
    password: Optional[str] = None


# Additional properties to return via API
class User(UserBaseInDB):
    pass
