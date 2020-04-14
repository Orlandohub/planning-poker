import os

import pytest

from db.mongodb_utils import connect_to_mongo
from db.mongodb import get_database
from core.config import MONGO_DB_NAME, TEST_MONGO_DB_NAME
from tests.utils import db_cleanup_and_close


def pytest_configure(config):
    """
    Allows plugins and conftest files to perform initial configuration.
    This hook is called for every plugin and initial conftest
    file after command line options have been parsed.
    """
    os.environ["MONGO_DB_NAME"] = str(TEST_MONGO_DB_NAME)


def pytest_unconfigure(config):
    """
    called before test process is exited.
    """
    os.environ["MONGO_DB_NAME"] = str(MONGO_DB_NAME)



@pytest.fixture(scope="function")
async def init_db():
    await connect_to_mongo()
    conn = await get_database()
    yield conn
    db_cleanup_and_close(conn)

