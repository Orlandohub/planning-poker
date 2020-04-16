import pytest
import nest_asyncio
from slugify import slugify
from fastapi import status
from starlette.testclient import TestClient

import crud
from main import app
from models.poll import Poll
from tests.utils import MOCK_POLL_NAME, create_user_and_get_token


nest_asyncio.apply()

client = TestClient(app)


@pytest.mark.asyncio
async def test_get_poll(init_db):
    db = init_db

    # Get Token headers
    headers = await create_user_and_get_token(db, client)

    # Create poll
    await crud.poll.create_in_db(db, poll=Poll(name=MOCK_POLL_NAME))

    # Get poll
    res = client.get(f"http://localhost:8000/poll/{slugify(MOCK_POLL_NAME)}", headers=headers)

    assert res.status_code is 200
    assert res.json()["name"] == MOCK_POLL_NAME
    assert res.json()["slug"] == slugify(MOCK_POLL_NAME)


@pytest.mark.asyncio
async def test_get_poll_404(init_db):
    db = init_db

    # Get Token headers
    headers = await create_user_and_get_token(db, client)

    # Get poll
    res = client.get(f"http://localhost:8000/poll/{slugify(MOCK_POLL_NAME)}", headers=headers)

    assert res.status_code is status.HTTP_400_BAD_REQUEST
    assert res.json() == {"detail": "Poll does not exist!"}


@pytest.mark.asyncio
async def test_create_poll(init_db):
    db = init_db

    # Get Token headers
    headers = await create_user_and_get_token(db, client)

    res = client.post(
        "http://localhost:8000/poll/create",
        json={"name": MOCK_POLL_NAME},
        headers=headers
    )

    assert res.json()["status"] == "success"
    assert res.json()["message"] == "Poll Created"


@pytest.mark.asyncio
async def test_create_poll_400_if_poll_already_exists(init_db):
    db = init_db
    res = None

    # Get Token headers
    headers = await create_user_and_get_token(db, client)

    for c in range(2):
        res = client.post(
            "http://localhost:8000/poll/create",
            json={"name": MOCK_POLL_NAME},
            headers=headers
        )

    assert res.status_code is status.HTTP_400_BAD_REQUEST
    assert res.json() == {"detail": "This poll already exists!"}

