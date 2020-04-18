from datetime import datetime
from typing import List, Optional, Dict

from pydantic import BaseModel


class Message(BaseModel):
    username: str
    message: str
    sent_date: datetime = datetime.now()
    

class Chat(BaseModel):
    subscriptions: Optional[Dict] = {}
    messages: Optional[List[Message]] = []