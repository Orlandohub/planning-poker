from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


class DataBase:
    client: AsyncIOMotorClient = None
    db_name: str = ""


db = DataBase()


async def get_database() -> AsyncIOMotorDatabase:
    return db.client[db.db_name]


async def get_connection() -> AsyncIOMotorClient:
    return db.client
