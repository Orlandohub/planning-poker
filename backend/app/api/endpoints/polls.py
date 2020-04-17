from fastapi import Depends, APIRouter, status, HTTPException, Body

import crud
from models.user import User
from models.poll import Poll
from models.task import Task
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


@router.post("/create-task")
async def create_task(
    task: Task,
    *,
    slug: str = Body(...),
    current_user: User = Depends(get_current_active_user)
):
    db = await get_database()
    poll = await crud.poll.get_poll(db, slug=slug)

    if not poll:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Poll does not exist!"
        )

    if poll.current_task:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only one task, at a time, can be open!"
        )

    poll.current_task = Task(**task.dict())
    await crud.poll.update_poll(db, poll=poll)

    return {"status": "success", "message": "Task Created"}


@router.post("/update-task")
async def update_task(
    task: Task,
    *,
    slug: str = Body(...),
    current_user: User = Depends(get_current_active_user)
):
    db = await get_database()
    poll = await crud.poll.get_poll(db, slug=slug)

    if not poll:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Poll does not exist!"
        )

    poll.current_task = Task(**task.dict())
    await crud.poll.update_poll(db, poll=poll)

    return {"status": "success", "message": "Task Updated"}


@router.post("/close-task")
async def close_task(
    *,
    slug: str = Body(..., embed=True),
    current_user: User = Depends(get_current_active_user)
):
    db = await get_database()
    poll = await crud.poll.get_poll(db, slug=slug)

    if not poll:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Poll does not exist!"
        )

    poll.current_task = None
    await crud.poll.update_poll(db, poll=poll)

    return {"status": "success", "message": "Task Closed"}


@router.post("/vote")
async def vote(
    *,
    vote: str = Body(...),
    slug: str = Body(...),
    current_user: User = Depends(get_current_active_user)
):
    db = await get_database()
    poll = await crud.poll.get_poll(db, slug=slug)

    if not poll:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Poll does not exist!"
        )

    if not poll.current_task:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No task available to vote on!"
        )

    if not poll.current_task.allow_votes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Votes not allowed at the moment!"
        )

    poll.current_task.votes[current_user.username] = vote
    await crud.poll.update_poll(db, poll=poll)
    return {"status": "success", "message": "Vote submitted"}




