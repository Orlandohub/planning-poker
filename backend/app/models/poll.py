from typing import Optional, List

from pydantic import BaseModel
from slugify import slugify

from models.task import Task
from models.chat import Chat


class Poll(BaseModel):
    name: str
    slug: Optional[str]
    chat: Optional[Chat] = {}
    current_task: Optional[Task] = None
    active_users: List[str] = []
