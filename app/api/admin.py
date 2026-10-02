from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.chat import Conversation, Message
from app.models.user import User
from app.api.deps import get_current_active_admin

router = APIRouter()

@router.get("/conversations")
def get_all_conversations(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_active_admin)
):
    """
    Retrieve all conversations (Admin only).
    """
    conversations = db.query(Conversation).order_by(Conversation.started_at.desc()).all()
    
    # We serialize manually for simplicity, though Pydantic is better in production
    results = []
    for c in conversations:
        results.append({
            "id": c.id,
            "session_id": c.session_id,
            "title": c.title,
            "started_at": c.started_at,
            "message_count": len(c.messages)
        })
    return results

@router.get("/conversations/{session_id}")
def get_conversation_details(
    session_id: str,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_active_admin)
):
    """
    Retrieve specific conversation messages (Admin only).
    """
    conversation = db.query(Conversation).filter(Conversation.session_id == session_id).first()
    if not conversation:
        return {"error": "Conversation not found"}
        
    messages = db.query(Message).filter(Message.conversation_id == conversation.id).order_by(Message.timestamp.asc()).all()
    
    return {
        "conversation": {
            "title": conversation.title,
            "session_id": conversation.session_id
        },
        "messages": [{"sender": m.sender_type, "content": m.content, "timestamp": m.timestamp} for m in messages]
    }
