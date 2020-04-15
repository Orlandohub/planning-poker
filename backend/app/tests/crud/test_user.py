import pytest

from crud.user import get_user, authenticate_user, create_in_db
from models.user import UserCreate

from tests.utils import MOCK_USERNAME, MOCK_PASSWORD


@pytest.mark.asyncio
async def test_get_user(init_db):
    db = init_db
    user_in = UserCreate(username=MOCK_USERNAME, password=MOCK_PASSWORD)
    await create_in_db(db, user_in=user_in)
    res = await get_user(db, MOCK_USERNAME)

    assert MOCK_USERNAME == res.username


@pytest.mark.asyncio
async def test_get_user_returns_none_if_user_does_not_exist(init_db):
    db = init_db
    user_in = UserCreate(username=MOCK_USERNAME, password=MOCK_PASSWORD)
    await create_in_db(db, user_in=user_in)
    res = await get_user(db, "ghost")

    assert res == None


@pytest.mark.asyncio
async def test_authenticate_user(init_db):
    db = init_db
    user_in = UserCreate(username=MOCK_USERNAME, password=MOCK_PASSWORD)
    await create_in_db(db, user_in=user_in)
    res = await authenticate_user(db, MOCK_USERNAME, MOCK_PASSWORD)

    assert MOCK_USERNAME == res.username


@pytest.mark.asyncio
async def test_authenticate_user_returns_none_if_pass_does_not_match(init_db):
    db = init_db
    user_in = UserCreate(username=MOCK_USERNAME, password=MOCK_PASSWORD)
    await create_in_db(db, user_in=user_in)
    res = await authenticate_user(db, MOCK_USERNAME, "nope")

    assert res == None
