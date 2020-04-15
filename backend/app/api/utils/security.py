import jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from db.mongodb import get_database
from models.user import User
from models.token import TokenPayload
from crud.user import get_user
from core.config import SECRET_KEY
from core.jwt import ALGORITHM

"""
If you are a very strict "Pythonista" you might dislike the style
of the parameter name tokenUrl instead of token_url.

That's because it is using the same name as in the OpenAPI spec.
So that if you need to investigate more about any of these security
schemes you can just copy and paste it to find more information about it.
"""
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/access-token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
        token_data = TokenPayload(username=username)

    except jwt.PyJWTError:
        raise credentials_exception

    db = await get_database()
    user = await get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user
