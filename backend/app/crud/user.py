import os

from fastapi.encoders import jsonable_encoder

from core.security import verify_password, get_password_hash
from core.config import USER_COLLECTION_NAME
from db.mongodb import AsyncIOMotorDatabase
from models.user import UserCreate, UserInDB


async def get_user(db: AsyncIOMotorDatabase, username: str) -> UserInDB:
    row = await db[USER_COLLECTION_NAME].find_one({"username": username})
    if row:
        return UserInDB(**row)


async def authenticate_user(
    db: AsyncIOMotorDatabase, username: str, password: str
) -> UserInDB:
    user = await get_user(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


async def create_in_db(db: AsyncIOMotorDatabase, *, user_in: UserCreate):
    user_doc_id = await get_user(db, user_in.username)
    passwordhash = get_password_hash(user_in.password)
    user = UserInDB(**user_in.dict(), hashed_password=passwordhash)
    doc_data = jsonable_encoder(user)

    res = await db[USER_COLLECTION_NAME].insert_one(doc_data)
    return res
