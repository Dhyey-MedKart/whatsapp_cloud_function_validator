from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import datetime

app = FastAPI(title="WhatsApp Data Validator")

class JID(BaseModel):
    Device: int
    IsEmpty: bool
    Server: str
    RawAgent: int
    User: str
    Integrator: int

class Media(BaseModel):
    filename: Optional[str] = None
    media_key: Optional[List[int]] = None
    mime_type: Optional[str] = None
    url: Optional[str] = None

class Message(BaseModel):
    message_id: str
    conversation_type: str
    type: str
    body: Optional[str] = None
    delivered_at: Optional[int] = None
    direction: str
    edited_at: Optional[int] = None
    is_deleted: bool
    media: Optional[Media] = None
    status: str
    read_at: Optional[int] = None
    sent_at: int
    mention: Optional[List[Any]] = []
    sent_by: Optional[str] = None

class Chat(BaseModel):
    id: str
    JID: JID
    is_group: bool
    business_name: Optional[str] = None
    full_name: Optional[str] = None
    push_name: Optional[str] = None
    phone_number: Optional[str]
    messages: List[Message]

class DataField(BaseModel):
    chats: List[Chat]

class StoreData(BaseModel):
    store_id: str
    wa_account: str
    wa_jid: JID
    chunk_index: int
    connected_at: datetime
    phone_number: str
    is_active: bool
    disconnect_reason: Optional[str] = None
    status: str
    last_seen: datetime
    data: DataField
    last_sync_at: Optional[datetime] = None
    total_chunks:int

@app.post("/validate")
async def validate_data(data: StoreData, x_api_key: str = Header(..., alias="x-api-key")):
    """
    Validates a list of StoreData objects and checks the x-api-key header.
    FastAPI handles dtype and structure validation using the defined Pydantic models.
    """
    # Simply replace this with your actual secure API key or an environment variable check
    VALID_API_KEY = "my_secure_api_key_123"
    
    if x_api_key != VALID_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid x-api-key")

    return {"status": "success", "message": "Data validated successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
