from fastapi import APIRouter

from .endpoints import login, users, polls


api_router = APIRouter()

api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(polls.router, prefix="/poll", tags=["polls"])
