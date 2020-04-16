from fastapi import status, HTTPException

import crud
from core.config import USER_COLLECTION_NAME, COLLECTIONS
from models.user import UserCreate

MOCK_USERNAME = "john"
MOCK_PASSWORD = "secret"

MOCK_POLL_NAME = "Cool Pool"


async def db_cleanup(db):
    for collection_name in COLLECTIONS:
        await db[collection_name].delete_many({})


def close_conn(conn):
    conn.close()


def user_authentication_headers(client, username, password):
    data = {"username": MOCK_USERNAME, "password": MOCK_PASSWORD}

    r = client.post(
        "http://localhost:8000/login/access-token",
        headers={
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data=data,
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


async def create_user_and_get_token(db, client):
    # Create User and get token
    user_in = UserCreate(username=MOCK_USERNAME, password=MOCK_PASSWORD)
    res = await crud.user.create_in_db(db, user_in=user_in)
    headers = user_authentication_headers(client, MOCK_USERNAME, MOCK_PASSWORD)
    return headers
