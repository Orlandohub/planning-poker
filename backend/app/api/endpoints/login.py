from datetime import timedelta

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from models.token import Token
from crud.user import authenticate_user
from core.jwt import create_access_token
from db.mongodb import get_database


router = APIRouter()


@router.post("/access-token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    print("form data", form_data)
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    db = await get_database()
    user = await authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
