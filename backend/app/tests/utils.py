from fastapi import status, HTTPException

from core.config import USER_COLLECTION_NAME

MOCK_USERNAME = "john"
MOCK_PASSWORD = "secret"


def db_users_cleanup(db):
    db[USER_COLLECTION_NAME].delete_many({})


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
