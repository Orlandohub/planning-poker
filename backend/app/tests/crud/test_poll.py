import pytest
from slugify import slugify
from crud.poll import create_in_db, get_poll
from models.poll import Poll
from tests.utils import MOCK_POLL_NAME, MOCK_USERNAME


async def create_poll(db):
    poll = Poll(name=MOCK_POLL_NAME, slug=slugify(MOCK_POLL_NAME))
    return await create_in_db(db, poll=poll)


@pytest.mark.asyncio
async def test_get_poll(init_db):
    db = init_db
    db_response = await create_poll(db)

    poll = await get_poll(db, slug=slugify(MOCK_POLL_NAME))

    assert poll is not None
    assert poll.name == MOCK_POLL_NAME
    assert poll.slug == slugify(MOCK_POLL_NAME)


@pytest.mark.asyncio
async def test_get_poll_returns_none_if_no_poll(init_db):
    db = init_db
    poll = await get_poll(db, slug=slugify(MOCK_POLL_NAME))

    assert poll is None


@pytest.mark.asyncio
async def test_create_poll_in_db(init_db):
    db = init_db
    db_response = await create_poll(db)

    assert db_response is not None
    assert db_response.inserted_id is not None


@pytest.mark.asyncio
async def test_create_poll_in_db_fails_if_poll_already_exists(init_db):
    db = init_db
    db_response = None
    try:
        for c in range(2):
            db_response = await create_poll(db)
    except Exception as e:
        assert e.status_code == 400
        assert e.detail == "This poll already exists!"




