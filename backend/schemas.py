from pydantic import BaseModel
from datetime import datetime

class MessageInput(BaseModel):
    message: str

class MessageResponse(BaseModel):
    response: str
    timestamp: datetime