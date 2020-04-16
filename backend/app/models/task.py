from typing import List, Optional
from pydantic import BaseModel
from enum import Enum


class StateEnum(str, Enum):
    vote_session = "vote_session"
    discussion_session = "discussion_session"
    closed = "closed"


class Vote(BaseModel):
    username: str
    vote: str


class Task(BaseModel):
    _id: str
    description: str
    votes: Optional[List[Vote]] = None
    state: StateEnum = StateEnum.vote_session
