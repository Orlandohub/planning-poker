import pytest
import nest_asyncio
from fastapi import status
from starlette.testclient import TestClient

from main import app
from crud.user import create_in_db
from models.user import UserCreate
from tests.utils import MOCK_USERNAME, MOCK_PASSWORD


nest_asyncio.apply()

client = TestClient(app)


@pytest.mark.asyncio
async def test_login(init_db):
    db = init_db
    user_in = UserCreate(username=MOCK_USERNAME, password=MOCK_PASSWORD)
    res = await create_in_db(db, user_in=user_in)

    res = client.post(
        "https://localhost:8000/login/access-token",
        data={"username": MOCK_USERNAME, "password": MOCK_PASSWORD},
    )

    data = res.json()
    assert data["token_type"] == "bearer"
    assert res.status_code == 200


@pytest.mark.asyncio
async def test_login_no_user_exception(init_db):

    res = client.post(
        "https://localhost:8000/login/access-token",
        data={"username": MOCK_USERNAME, "password": MOCK_PASSWORD},
    )

    assert res.json() == {"detail": "Incorrect username or password"}
    assert res.status_code == status.HTTP_401_UNAUTHORIZED
