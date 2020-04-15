from motor.motor_asyncio import AsyncIOMotorClient


class DataBase:
    client: AsyncIOMotorClient = None
    db_name: str = ""


db = DataBase()


async def get_database() -> AsyncIOMotorClient:
    return db.client[db.db_name]
