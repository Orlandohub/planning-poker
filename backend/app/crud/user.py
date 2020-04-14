import os

from models.user import UserInDB
from core.security import verify_password
from core.config import MONGO_DB_NAME, USER_COLLECTION_NAME
from db.mongodb import AsyncIOMotorClient


async def get_user(conn: AsyncIOMotorClient, username: str) -> UserInDB:
    row = await conn[str(os.getenv("MONGO_DB_NAME"))][USER_COLLECTION_NAME].find_one({"username": username})
    if row:
        return UserInDB(**row)


async def authenticate_user(conn: AsyncIOMotorClient, username: str, password: str) -> UserInDB:
    user = await get_user(conn, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
