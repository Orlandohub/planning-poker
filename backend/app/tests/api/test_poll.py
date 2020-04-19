import pytest
import nest_asyncio
from slugify import slugify
from fastapi import status
from starlette.testclient import TestClient

import crud
from main import app
from models.poll import Poll, Task
from tests.utils import (
    MOCK_POLL_NAME,
    MOCK_TASK,
    MOCK_USERNAME,
    create_user_and_get_token,
)


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
    res = client.get(
        f"http://localhost:8000/poll/{slugify(MOCK_POLL_NAME)}", headers=headers
    )

    assert res.status_code is 200
    assert res.json()["name"] == MOCK_POLL_NAME
    assert res.json()["slug"] == slugify(MOCK_POLL_NAME)


@pytest.mark.asyncio
async def test_get_poll_404(init_db):
    db = init_db

    # Get Token headers
    headers = await create_user_and_get_token(db, client)

    # Get poll
    res = client.get(
        f"http://localhost:8000/poll/{slugify(MOCK_POLL_NAME)}", headers=headers
    )

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
        headers=headers,
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
            headers=headers,
        )

    assert res.status_code is status.HTTP_400_BAD_REQUEST
    assert res.json() == {"detail": "This poll already exists!"}


#########
# TASKS #
#########
@pytest.mark.asyncio
async def test_create_task(init_db):
    db = init_db

    # Create poll
    await crud.poll.create_in_db(db, poll=Poll(name=MOCK_POLL_NAME))

    # Get Token headers
    headers = await create_user_and_get_token(db, client)

    # Create task
    res = client.post(
        "http://localhost:8000/poll/create-task",
        headers=headers,
        json={"task": MOCK_TASK, "slug": slugify(MOCK_POLL_NAME)},
    )

    data = res.json()

    assert data["status"] == "success"
    assert data["message"] == "Task Created"


@pytest.mark.asyncio
async def test_create_400_if_no_poll(init_db):
    db = init_db

    # Get Token headers
    headers = await create_user_and_get_token(db, client)

    # Create task
    res = client.post(
        "http://localhost:8000/poll/create-task",
        headers=headers,
        json={"task": MOCK_TASK, "slug": slugify(MOCK_POLL_NAME)},
    )

    assert res.status_code is status.HTTP_400_BAD_REQUEST
    assert res.json() == {"detail": "Poll does not exist!"}


@pytest.mark.asyncio
async def test_create_400_if_current_task_exists(init_db):
    db = init_db

    # Get Token headers
    headers = await create_user_and_get_token(db, client)

    # Create poll
    await crud.poll.create_in_db(db, poll=Poll(name=MOCK_POLL_NAME))

    for c in range(2):
        # Create task
        res = client.post(
            "http://localhost:8000/poll/create-task",
            headers=headers,
            json={"task": MOCK_TASK, "slug": slugify(MOCK_POLL_NAME)},
        )

    assert res.status_code is status.HTTP_400_BAD_REQUEST
    assert res.json() == {"detail": "Only one task, at a time, can be open!"}


@pytest.mark.asyncio
async def test_update_task(init_db):
    db = init_db
    task = Task(**MOCK_TASK)

    # Get Token headers
    headers = await create_user_and_get_token(db, client)

    # Create poll
    await crud.poll.create_in_db(db, poll=Poll(name=MOCK_POLL_NAME))

    # Get poll
    poll = await crud.poll.get_poll(db, slug=slugify(MOCK_POLL_NAME))

    # create task
    poll.current_task = task
    res = await crud.poll.update_poll(db, poll=poll)

    # Get poll
    poll = await crud.poll.get_poll(db, slug=slugify(MOCK_POLL_NAME))

    assert poll.current_task.description == "Implement unit tests!"

    # update task
    task.description = "Refactor"
    res = client.post(
        "http://localhost:8000/poll/update-task",
        headers=headers,
        json={"task": task.dict(), "slug": slugify(MOCK_POLL_NAME)},
    )

    data = res.json()

    assert data["status"] == "success"
    assert data["message"] == "Task Updated"

    # Get poll
    poll = await crud.poll.get_poll(db, slug=slugify(MOCK_POLL_NAME))
    assert poll.current_task.description == "Refactor"


@pytest.mark.asyncio
async def test_close_task(init_db):
    db = init_db
    task = Task(**MOCK_TASK)

    # Get Token headers
    headers = await create_user_and_get_token(db, client)

    # Create poll
    await crud.poll.create_in_db(db, poll=Poll(name=MOCK_POLL_NAME))

    # Get poll
    poll = await crud.poll.get_poll(db, slug=slugify(MOCK_POLL_NAME))

    # Create task
    poll.current_task = task
    res = await crud.poll.update_poll(db, poll=poll)

    # Get poll
    poll = await crud.poll.get_poll(db, slug=slugify(MOCK_POLL_NAME))

    assert poll.current_task.description == "Implement unit tests!"

    res = client.post(
        "http://localhost:8000/poll/close-task",
        headers=headers,
        json={"slug": slugify(MOCK_POLL_NAME)},
    )

    data = res.json()

    assert data["status"] == "success"
    assert data["message"] == "Task Closed"

    # Get poll
    poll = await crud.poll.get_poll(db, slug=slugify(MOCK_POLL_NAME))

    assert poll.current_task == None


@pytest.mark.asyncio
async def test_vote(init_db):
    db = init_db
    task = Task(**{**MOCK_TASK, "allow_votes": True})

    # Get Token headers
    headers = await create_user_and_get_token(db, client)

    # Create poll
    await crud.poll.create_in_db(db, poll=Poll(name=MOCK_POLL_NAME))

    # Get poll
    poll = await crud.poll.get_poll(db, slug=slugify(MOCK_POLL_NAME))

    # Create task
    poll.current_task = task
    res = await crud.poll.update_poll(db, poll=poll)

    # Get poll
    poll = await crud.poll.get_poll(db, slug=slugify(MOCK_POLL_NAME))

    assert poll.current_task.allow_votes == True

    res = client.post(
        "http://localhost:8000/poll/vote",
        headers=headers,
        json={"vote": "1/2", "slug": slugify(MOCK_POLL_NAME)},
    )

    data = res.json()

    assert data["status"] == "success"
    assert data["message"] == "Vote submitted"

    # Get poll
    poll = await crud.poll.get_poll(db, slug=slugify(MOCK_POLL_NAME))

    assert poll.current_task.votes[MOCK_USERNAME] == "1/2"


@pytest.mark.asyncio
async def test_vote_400_if_no_task_available(init_db):
    db = init_db

    # Get Token headers
    headers = await create_user_and_get_token(db, client)

    # Create poll
    await crud.poll.create_in_db(db, poll=Poll(name=MOCK_POLL_NAME))

    # Get poll
    poll = await crud.poll.get_poll(db, slug=slugify(MOCK_POLL_NAME))

    assert poll.current_task == None

    res = client.post(
        "http://localhost:8000/poll/vote",
        headers=headers,
        json={"vote": "1/2", "slug": slugify(MOCK_POLL_NAME)},
    )

    data = res.json()

    assert res.status_code is status.HTTP_400_BAD_REQUEST
    assert data == {"detail": "No task available to vote on!"}


@pytest.mark.asyncio
async def test_vote_400_if_votes_not_allowed(init_db):
    db = init_db
    task = Task(**{**MOCK_TASK, "allow_votes": False})

    # Get Token headers
    headers = await create_user_and_get_token(db, client)

    # Create poll
    await crud.poll.create_in_db(db, poll=Poll(name=MOCK_POLL_NAME))

    # Get poll
    poll = await crud.poll.get_poll(db, slug=slugify(MOCK_POLL_NAME))

    # Create task
    poll.current_task = task
    res = await crud.poll.update_poll(db, poll=poll)

    # Get poll
    poll = await crud.poll.get_poll(db, slug=slugify(MOCK_POLL_NAME))

    assert poll.current_task.allow_votes == False

    res = client.post(
        "http://localhost:8000/poll/vote",
        headers=headers,
        json={"vote": "1/2", "slug": slugify(MOCK_POLL_NAME)},
    )

    data = res.json()

    assert res.status_code is status.HTTP_400_BAD_REQUEST
    assert data == {"detail": "Votes not allowed at the moment!"}
