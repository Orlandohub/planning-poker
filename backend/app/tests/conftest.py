import pytest

from db.mongodb_utils import connect_to_mongo
from db.mongodb import get_database, get_connection
from core.config import TEST_MONGO_DB_NAME
from tests.utils import db_users_cleanup, close_conn


@pytest.fixture(scope="function")
async def init_db():
    await connect_to_mongo(TEST_MONGO_DB_NAME)
    db = await get_database()
    conn = await get_connection()
    yield db
    db_users_cleanup(db)
    close_conn(conn)
