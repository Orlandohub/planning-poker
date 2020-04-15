import os

from fastapi import status, HTTPException

from core.security import get_password_hash
from core.config import (
    USER_COLLECTION_NAME,
    MONGO_DB_NAME,
)

MOCK_USERNAME = "john"
MOCK_PASSWORD = "secret"


async def insert_user(conn):
    res = await conn[USER_COLLECTION_NAME].insert_one({
        "username": MOCK_USERNAME,
        "hashed_password": get_password_hash(MOCK_PASSWORD)
    })

    return res


def db_users_cleanup(conn):
    conn[USER_COLLECTION_NAME].delete_many({})
    # conn.close()


def user_authentication_headers(client, username, password):
    data = {"username": "john", "password": "secret"}

    r = client.post(
        "http://localhost:8000/login/access-token",
        headers={"accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"},
        data=data
    )

    if r.status_code == 401:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    response = r.json()

    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers

