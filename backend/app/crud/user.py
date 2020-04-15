import os

from fastapi.encoders import jsonable_encoder

from core.security import verify_password, get_password_hash
from core.config import MONGO_DB_NAME, USER_COLLECTION_NAME
from db.mongodb import AsyncIOMotorClient
from models.user import UserCreate, UserInDB


async def get_user(conn: AsyncIOMotorClient, username: str) -> UserInDB:
    row = await conn[USER_COLLECTION_NAME].find_one({"username": username})
    if row:
        return UserInDB(**row)


async def authenticate_user(conn: AsyncIOMotorClient, username: str, password: str) -> UserInDB:
    user = await get_user(conn, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


async def create_in_db(conn: AsyncIOMotorClient, *, user_in: UserCreate):
    user_doc_id = await get_user(conn, user_in.username)
    passwordhash = get_password_hash(user_in.password)
    user = UserInDB(**user_in.dict(), hashed_password=passwordhash)
    doc_data = jsonable_encoder(user)

    res = await conn[USER_COLLECTION_NAME].insert_one(doc_data)
    return res