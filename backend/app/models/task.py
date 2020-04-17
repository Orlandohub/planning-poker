from typing import List, Optional, Dict
from pydantic import BaseModel


class Task(BaseModel):
    description: str
    votes: Optional[Dict] = {}
    allow_votes: bool = False
