from pymongo.results import InsertOneResult, UpdateResult
from fastapi import Depends, HTTPException, status
from slugify import slugify
from typing import List


from core.config import POLL_COLLECTION_NAME
from db.mongodb import AsyncIOMotorDatabase
from models.poll import Poll

from models.user import User


def get_all(db) -> List:
    results = db[POLL_COLLECTION_NAME].find({}, { "_id": 0, "name": 1, "slug": 1 })
    return results


async def get_poll(db: AsyncIOMotorDatabase, *, slug: str) -> Poll:
    row = await db[POLL_COLLECTION_NAME].find_one({"slug": slug})
    if row:
        return Poll(**row)


async def create_in_db(db: AsyncIOMotorDatabase, *, poll: Poll) -> InsertOneResult:

    existing_poll = await get_poll(db, slug=slugify(poll.name))

    if existing_poll:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="This poll already exists!"
        )

    poll_in_db = Poll(name=poll.name, slug=slugify(poll.name)).dict()
    db_response = await db[POLL_COLLECTION_NAME].insert_one(poll_in_db)
    return db_response


async def update_poll(db: AsyncIOMotorDatabase, *, poll: Poll) -> UpdateResult:
    updated_poll = await db[POLL_COLLECTION_NAME].update_one(
        {"slug": poll.slug}, {"$set": {**poll.dict()}}
    )
    return updated_poll
