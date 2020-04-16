from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class Message(BaseModel):
    username: str
    message: str
    sent_date: datetime = datetime.now()
    

class Chat(BaseModel):
    messages: Optional[List[Message]] = None