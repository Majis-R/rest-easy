from pydantic import BaseModel, Field
from datetime import datetime

class MessageCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=500)

class MessageResponse(BaseModel):
    id: int
    sender_username: str
    content: str
    timestamp: datetime

    class Config:
        from_attributes = True