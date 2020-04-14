import pytest
from main import app


from starlette.testclient import TestClient
from tests.utils import (
    user_authentication_headers,
    insert_user,
    MOCK_USERNAME,
    MOCK_PASSWORD
)

import nest_asyncio
nest_asyncio.apply()


client = TestClient(app)


@pytest.mark.asyncio
async def test_get_user_me(init_db):
    
    conn = init_db
    res = await insert_user(conn)

    headers = user_authentication_headers(client, MOCK_USERNAME, MOCK_PASSWORD)

    r = client.get(
        f"http://localhost:8000/users/me", headers=headers
    )
    current_user = r.json()

    assert current_user["disabled"] is None
    assert current_user["email"] is None
    assert current_user["username"] == MOCK_USERNAME


