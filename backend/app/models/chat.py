from datetime import datetime
from typing import List, Optional, Dict

from pydantic import BaseModel


class Message(BaseModel):
    username: str
    message: str
    sent_date: datetime = datetime.now()

    def dict(self, **kwargs):
        return {
            "username": self.username,
            "message": self.message,
            "sent_date": str(self.sent_date),
        }


class Chat(BaseModel):
    messages: Optional[List[Message]] = []
