import pytest

from crud.user import get_user, authenticate_user

from tests.utils import (
    insert_user,
    MOCK_USERNAME,
    MOCK_PASSWORD
)


@pytest.mark.asyncio
async def test_get_user(init_db):
    conn = init_db
    await insert_user(conn)

    res = await get_user(conn, MOCK_USERNAME)
    assert MOCK_USERNAME == res.username


@pytest.mark.asyncio
async def test_get_user_returns_none_if_user_does_not_exist(init_db):
    conn = init_db
    await insert_user(conn)

    res = await get_user(conn, "ghost")
    assert res == None


@pytest.mark.asyncio
async def test_authenticate_user(init_db):
    conn = init_db
    await insert_user(conn)

    res = await authenticate_user(conn, MOCK_USERNAME, MOCK_PASSWORD)
    assert MOCK_USERNAME == res.username


@pytest.mark.asyncio
async def test_authenticate_user_returns_none_if_pass_does_not_match(init_db):
    conn = init_db
    await insert_user(conn)

    res = await authenticate_user(conn, MOCK_USERNAME, "nope")
    assert res == None

