import os

from core.security import get_password_hash
from core.config import (
    USER_COLLECTION_NAME,
    MONGO_DB_NAME,
)

MOCK_USERNAME = "john"
MOCK_PASSWORD = "secret"


async def insert_user(conn):
    res = await conn[str(os.getenv("MONGO_DB_NAME"))][USER_COLLECTION_NAME].insert_one({
        "username": MOCK_USERNAME,
        "hashed_password": get_password_hash(MOCK_PASSWORD)
    })

    return res


def db_cleanup_and_close(conn):
    conn[str(os.getenv("MONGO_DB_NAME"))][USER_COLLECTION_NAME].delete_many({})
    conn.close()


def user_authentication_headers(client, username, password):
    data = {"username": "john", "password": "secret"}

    r = client.post(
        "http://localhost:8000/login/access-token",
        headers={"accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"},
        data=data
    )
    response = r.json()

    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers

