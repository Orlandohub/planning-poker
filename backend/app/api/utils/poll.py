import crud
from models.chat import Message
from core.config import POLL_COLLECTION_NAME, BROADCAST


async def change_stream(websocket, room, db):
    pipeline = [{"$match": {"operationType": "update"}}]
    async with db[POLL_COLLECTION_NAME].watch(pipeline) as stream:
        async for insert_change in stream:
            # Don't send updates related to chat
            if not insert_change["updateDescription"]["updatedFields"].get("chat"):
                poll = await crud.poll.get_poll(db, slug=room)
                # Only send updates from current room
                if poll.slug == room:
                    await websocket.send_json(poll.dict())


async def chatroom_ws_receiver(websocket, room, db):
    async for message in websocket.iter_json():
        try:
            msg = Message(**message)
            await BROADCAST.publish(channel=room, message=message["message"])
            # Save received message on Poll Chat
            poll = await crud.poll.get_poll(db, slug=room)
            poll.chat.messages.append(msg)
            await crud.poll.update_poll(db, poll=poll)
        except Exception as e:
            pass



async def chatroom_ws_sender(websocket, room):
    async with BROADCAST.subscribe(channel=room) as subscriber:
        async for event in subscriber:
            # Send message to all connected websockets
            await websocket.send_json({"message": event.message})
