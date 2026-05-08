from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MessageInput(BaseModel):
    message: str

class MessageResponse(BaseModel):
    response: str
    timestamp: datetime

class PackageSchema(BaseModel):
    id: int
    name: str
    description: str
    price: float
    location: str

    class Config:
        from_attributes = True

class FAQSchema(BaseModel):
    id: int
    question: str
    answer: str

    class Config:
        from_attributes = True