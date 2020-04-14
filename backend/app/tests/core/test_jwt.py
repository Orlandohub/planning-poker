from datetime import timedelta

from core.jwt import create_access_token
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES


def test_create_access_token():
  access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  access_token = create_access_token(
      data={"username": str("john")}, expires_delta=access_token_expires
  )

  assert access_token is not None
