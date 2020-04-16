import pytest
import nest_asyncio
from starlette.testclient import TestClient

from main import app
from crud.user import create_in_db
from models.user import UserCreate
from tests.utils import (
    user_authentication_headers,
    create_user_and_get_token,
    MOCK_USERNAME,
    MOCK_PASSWORD
)


nest_asyncio.apply()


client = TestClient(app)


@pytest.mark.asyncio
async def test_get_user_me(init_db):
    db = init_db

    headers = await create_user_and_get_token(db, client)

    r = client.get("http://localhost:8000/users/me", headers=headers)
    current_user = r.json()

    assert r.status_code == 200
    assert current_user["disabled"] is False
    assert current_user["email"] is None
    assert current_user["username"] == MOCK_USERNAME


def test_get_user_me_returns_401_for_unexisting_user(init_db):
    try:
        user_authentication_headers(client, MOCK_USERNAME, MOCK_PASSWORD)
    except Exception as a:
        assert a.status_code == 401


def test_create_user(init_db):
    res = client.post(
        "http://127.0.0.1:8000/users/signup",
        headers={"accept": "application/json", "Content-Type": "application/json"},
        json={
            "username": "string",
            "password": "string",
            "email": "user@example.com",
            "full_name": "string",
        },
    )

    data = res.json()
    assert res.status_code == 200, res.text
    assert data["username"] == "string"
