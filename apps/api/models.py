from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    assistant_message: str
    urgency: str
    safety_flags: List[str]
    citations: List[str]
    recommendations: List[str]
