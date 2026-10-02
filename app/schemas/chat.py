from pydantic import BaseModel

class ChatRequest(BaseModel):
    query: str
    session_id: str | None = None # Used later for conversation memory
    role: str = "consumer" # admin, customer, consumer
    kiosk_id: str | None = None
    mobile_number: str | None = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
