
import logging

from motor.motor_asyncio import AsyncIOMotorClient
from core.config import (
  MONGODB_URL,
  MAX_CONNECTIONS_COUNT,
  MIN_CONNECTIONS_COUNT,
  MONGO_DB_NAME
)
from .mongodb import db


async def connect_to_mongo(db_name=MONGO_DB_NAME):
    logging.info("Connecting to database...")
    db.db_name = db_name
    db.client = AsyncIOMotorClient(MONGODB_URL,
                                   maxPoolSize=MAX_CONNECTIONS_COUNT,
                                   minPoolSize=MIN_CONNECTIONS_COUNT)
    logging.info("Successfully connected to the database")


async def close_mongo_connection():
    logging.info("Closing database connection...")
    db.client.close()
    logging.info("Database connection closed")
