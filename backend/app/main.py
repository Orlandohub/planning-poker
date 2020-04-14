from fastapi import FastAPI

from api.api import api_router
from core.config import PROJECT_NAME
from db.mongodb_utils import connect_to_mongo, close_mongo_connection

app = FastAPI(title=PROJECT_NAME)


@app.get("/")
def root():
    return {"message": "Hello World"}


app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

app.include_router(api_router)