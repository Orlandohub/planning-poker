from fastapi import Depends, APIRouter, status, Body, HTTPException
from pydantic.networks import EmailStr

import crud
from api.utils.security import get_current_active_user
from models.user import User, UserCreate, UserInDB
from db.mongodb import get_database

router = APIRouter()


@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.post("/signup", response_model=User)
async def create_user(
    *,
    username: str = Body(...),
    password: str = Body(...),
    email: EmailStr = Body(None),
    full_name: str = Body(None)
):
    """
    Create new user.
    """
    conn = await get_database()
    user = await crud.user.get_user(conn, username=username)

    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this username already exists in the system.",
        )

    user_in = UserCreate(
        username=username, password=password, email=email, full_name=full_name
    )
    user = await crud.user.create_in_db(conn, user_in=user_in)

    return user_in