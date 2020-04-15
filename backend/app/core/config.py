import os

from starlette.datastructures import Secret
from dotenv import load_dotenv

load_dotenv()

PROJECT_NAME = "Planning Poker - Collaborative Planning"

# JWT
SECRET_KEY = str(Secret(os.getenv("SECRET_KEY", "precious")))
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 8  # 60 minutes * 24 hours * 8 days = 8 days

# MongoDB
MAX_CONNECTIONS_COUNT = 10
MIN_CONNECTIONS_COUNT = 10

MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
MONGODB_URL = f"mongodb://{MONGO_HOST}:{MONGO_PORT}"

MONGO_DB_NAME = os.getenv("MONGO_DB", "planning_poker")
TEST_MONGO_DB_NAME = "planning_poker_test"

USER_COLLECTION_NAME = "users"
