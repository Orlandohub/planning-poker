import json

from fastapi import (
    Depends,
    APIRouter,
    status,
    HTTPException,
    Body,
    Header,
    WebSocket
)

import crud
from models.user import User
from models.poll import Poll
from models.task import Task
from db.mongodb import get_database
from api.utils.security import get_current_active_user, get_current_user

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


CHAT_USERS = {}

@router.websocket("/{slug}/chat")
async def chat(
    slug: str,
    websocket: WebSocket,
    *,
    token: str = Header(...)
):
    # Init Websocket connection
    await websocket.accept()

    # Get Poll Object
    db = await get_database()
    poll = await crud.poll.get_poll(db, slug=slug)

    # Close connection if no poll available
    if not poll:
        await websocket.send_text("No Poll Available With This Name")
        await websocket.close(code=1000)

    # If user auth register on chat subscriptions
    try:
        user = await get_current_user(token)
        active_user = await get_current_active_user(user)
        CHAT_USERS[f"{active_user.username}_{slug}"] = websocket
    except Exception as e:
        await websocket.send_text("Not authenticated")
        await websocket.close()

    else:
        # Receive / Send messages
        try:
            while True:
                data = await websocket.receive_json()
                for key, socket in CHAT_USERS.items():
                    await socket.send_json(data)

        except Exception as e:
            del CHAT_USERS[f"{active_user.username}_{slug}"]


