import os

from broadcaster import Broadcast
from starlette.datastructures import Secret
from dotenv import load_dotenv

load_dotenv()

PROJECT_NAME = "Planning Poker - Collaborative Planning"

# JWT
SECRET_KEY = str(Secret(os.getenv("SECRET_KEY", "precious")))
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 8  # 60 minutes * 24 hours * 8 days = 8 days

# Redis with Broadcaster
BROADCAST_URL = os.getenv("BROADCAST_URL", "redis://redis:6379")
BROADCAST = Broadcast(BROADCAST_URL)

# MongoDB
MONGO_USER = os.getenv("MONGO_USER", "admin")
MONGO_PASS = os.getenv("MONGO_PASS")
MONGODB_URL = f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}@cluster0-swdos.mongodb.net/test?retryWrites=true&w=majority"

MONGO_DB_NAME = os.getenv("MONGO_DB", "planning_poker")
TEST_MONGO_DB_NAME = "planning_poker_test"

MAX_CONNECTIONS_COUNT = 10
MIN_CONNECTIONS_COUNT = 10

USER_COLLECTION_NAME = "users"
POLL_COLLECTION_NAME = "polls"

COLLECTIONS = [USER_COLLECTION_NAME, POLL_COLLECTION_NAME]
