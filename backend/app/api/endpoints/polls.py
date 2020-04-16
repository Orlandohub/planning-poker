from fastapi import Depends, APIRouter, status, HTTPException

import crud
from models.user import User
from models.poll import Poll
from db.mongodb import get_database
from api.utils.security import get_current_active_user

router = APIRouter()


@router.get("/{slug}")
async def get_poll(
    slug: str,
    *,
    current_user: User = Depends(get_current_active_user)
):
    db = await get_database()
    poll = await crud.poll.get_poll(db, slug=slug)

    if not poll:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Poll does not exist!"
        )

    return poll.dict()


@router.post("/create")
async def create_poll(
    poll: Poll,
    *,
    current_user: User = Depends(get_current_active_user)
):
    db = await get_database()
    await crud.poll.create_in_db(db, poll=poll)

    return {"status": "success", "message": "Poll Created"}

