    # import uuid
    # from fastapi import APIRouter, Depends, Request
    # from sqlalchemy.orm import Session
    # from slowapi import Limiter
    # from slowapi.util import get_remote_address

    # from app.schemas.chat import ChatRequest, ChatResponse
    # from app.services.ai_service import ai_service
    # from app.knowledge.retriever import retriever
    # from app.database.database import get_db
    # from app.models.chat import Conversation, Message
    # from app.services.context_engine import ctx_role, ctx_kiosk_id, ctx_mobile_number

    # router = APIRouter()
    # limiter = Limiter(key_func=get_remote_address)

    # @router.post("/", response_model=ChatResponse)
    # @limiter.limit("5/minute")
    # async def handle_chat(request_data: ChatRequest, request: Request, db: Session = Depends(get_db)):
    #     """
    #     Main endpoint for the AI Chatbot.
    #     Accepts a user query, fetches context using RAG, injects chat history, and returns the Gemini response.
    #     """
        
    #     # 0. Set context variables for implicit state injection
    #     ctx_role.set(request_data.role)
    #     ctx_kiosk_id.set(request_data.kiosk_id)
    #     ctx_mobile_number.set(request_data.mobile_number)
        
    #     # 1. Manage Conversation Session
    #     session_id = request_data.session_id
    #     if not session_id:
    #         session_id = str(uuid.uuid4())
    #         new_conv = Conversation(session_id=session_id, title=request_data.query[:50])
    #         db.add(new_conv)
    #         db.commit()
    #         db.refresh(new_conv)
    #         conversation = new_conv
    #     else:
    #         conversation = db.query(Conversation).filter(Conversation.session_id == session_id).first()
    #         if not conversation:
    #             # Fallback if somehow they send an invalid session
    #             conversation = Conversation(session_id=session_id, title=request_data.query[:50])
    #             db.add(conversation)
    #             db.commit()

    #     # 2. Save User Message
    #     user_msg = Message(conversation_id=conversation.id, sender_type="user", content=request_data.query)
    #     db.add(user_msg)
    #     db.commit()

    #     # 3. Retrieve Chat History & Map to Groq Format
    #     recent_messages = db.query(Message).filter(Message.conversation_id == conversation.id).order_by(Message.timestamp.asc()).limit(10).all()
        
    #     formatted_history = []
    #     # We skip the very last message in the DB because it's the current user query!
    #     for m in recent_messages[:-1]:
    #         role = "user" if m.sender_type == "user" else "assistant"
    #         formatted_history.append({"role": role, "content": m.content})

    #     # 4. RAG Retrieval
    #     knowledge_context = retriever.search(request_data.query, top_k=3)
        
    #     # 5. Generate AI Response (Async)
    #     answer = await ai_service.generate_response_async(
    #         query=request_data.query, 
    #         context=knowledge_context,
    #         history=formatted_history
    #     )
        
    #     # 6. Save AI Message
    #     ai_msg = Message(conversation_id=conversation.id, sender_type="ai", content=answer)
    #     db.add(ai_msg)
    #     db.commit()
        
    #     return {"response": answer, "session_id": session_id}


import uuid
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.ai_service import ai_service
from app.knowledge.retriever import retriever
from app.database.database import get_db
from app.models.chat import Conversation, Message
from app.services.context_engine import ctx_role, ctx_kiosk_id, ctx_mobile_number

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.post("/", response_model=ChatResponse)
@limiter.limit("5/minute")
async def handle_chat(request_data: ChatRequest, request: Request, db: Session = Depends(get_db)):
    """
    Main endpoint for the AI Chatbot.
    Accepts a user query, fetches context using RAG, injects chat history, and returns the Gemini response.
    """
    
    # 0. Set context variables for implicit state injection
    ctx_role.set(request_data.role)
    ctx_kiosk_id.set(request_data.kiosk_id)
    ctx_mobile_number.set(request_data.mobile_number)
    
    # 1. Manage Conversation Session
    session_id = request_data.session_id
    if not session_id:
        session_id = str(uuid.uuid4())
        new_conv = Conversation(session_id=session_id, title=request_data.query[:50])
        db.add(new_conv)
        db.commit()
        db.refresh(new_conv)
        conversation = new_conv
    else:
        conversation = db.query(Conversation).filter(Conversation.session_id == session_id).first()
        if not conversation:
            # Fallback if somehow they send an invalid session
            conversation = Conversation(session_id=session_id, title=request_data.query[:50])
            db.add(conversation)
            db.commit()

    # 2. Save User Message
    user_msg = Message(conversation_id=conversation.id, sender_type="user", content=request_data.query)
    db.add(user_msg)
    db.commit()

    # 3. Retrieve Chat History & Map to Groq Format
    recent_messages = db.query(Message).filter(Message.conversation_id == conversation.id).order_by(Message.timestamp.asc()).limit(10).all()
    
    formatted_history = []
    # We skip the very last message in the DB because it's the current user query!
    for m in recent_messages[:-1]:
        role = "user" if m.sender_type == "user" else "assistant"
        formatted_history.append({"role": role, "content": m.content})

    # 4. RAG Retrieval
    knowledge_context = retriever.search(request_data.query, top_k=3)
    
    # 5. Generate AI Response (Async)
    answer = await ai_service.generate_response_async(
        query=request_data.query, 
        context=knowledge_context,
        history=formatted_history
    )
    
    # 6. Save AI Message
    ai_msg = Message(conversation_id=conversation.id, sender_type="ai", content=answer)
    db.add(ai_msg)
    db.commit()
    
    return {"response": answer, "session_id": session_id}