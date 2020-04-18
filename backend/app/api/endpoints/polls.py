import json
from bson.json_util import dumps
from fastapi import (
    Depends,
    APIRouter,
    status,
    HTTPException,
    Body,
    Header,
    WebSocket
)
from starlette.endpoints import WebSocketEndpoint
from starlette.concurrency import run_until_first_complete

import crud
from core.config import POLL_COLLECTION_NAME, BROADCAST
from models.user import User
from models.poll import Poll
from models.task import Task
from models.chat import Chat, Message
from db.mongodb import get_database, get_connection
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


async def change_stream(websocket, db):
    pipeline = [{'$match': {'operationType': 'update'}}]
    async with db[POLL_COLLECTION_NAME].watch(pipeline) as stream:
        async for insert_change in stream:
            await websocket.send_text("DA UPDATED")


async def chatroom_ws_receiver(websocket, room):
    async for message in websocket.iter_json():
        print("MESSAGE", message)
        await BROADCAST.publish(channel=room, message=message["hey"])


async def chatroom_ws_sender(websocket, room):
    print("ROOM", room)
    async with BROADCAST.subscribe(channel=room) as subscriber:
        async for event in subscriber:
            print("EVENT", event)
            await websocket.send_json({"message": event.message})


@router.websocket("/{slug}/chat")
async def chatroom_ws(
    slug: str,
    websocket: WebSocket,
    *,
    token: str = Header(...)
):
    print("SLUG", slug)
    # Init Websocket connection
    await websocket.accept()

    # Get Poll Object
    db = await get_database()
    poll = await crud.poll.get_poll(db, slug=slug)

    # Close connection if no poll available
    if not poll:
        await websocket.send_text("No Poll Available With This Name")
        await websocket.close(code=1000)
        print("NO POLL CLOSE")
        return

    # Check if user is auth
    try:
        user = await get_current_user(token)
        active_user = await get_current_active_user(user)
    except Exception as e:
        await websocket.send_text("Not authenticated")
        await websocket.close(code=1000)
        print("NO AUTH CLOSE")
        return

    await run_until_first_complete(
        (change_stream, {"websocket": websocket, "db": db}),
        (chatroom_ws_receiver, {"websocket": websocket, "room": slug}),
        (chatroom_ws_sender, {"websocket": websocket, "room": slug})
    )

    print("CLOSE")

