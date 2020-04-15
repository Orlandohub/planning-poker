import os

import pytest

from db.mongodb_utils import connect_to_mongo
from db.mongodb import get_database
from core.config import MONGO_DB_NAME, TEST_MONGO_DB_NAME
from tests.utils import db_users_cleanup



@pytest.fixture(scope="function")
async def init_db():
    await connect_to_mongo(TEST_MONGO_DB_NAME)
    conn = await get_database()
    yield conn
    db_users_cleanup(conn)

