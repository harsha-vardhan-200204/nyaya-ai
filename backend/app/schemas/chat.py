from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    source: str
    context: Dict[str, Any]

class ChatHistoryItem(BaseModel):
    id: int
    user_id: int
    role: str  # "user" or "assistant"
    message: str
    timestamp: datetime

    class Config:
        from_attributes = True
