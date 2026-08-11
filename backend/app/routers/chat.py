from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.chat import ChatHistory
from app.models.auth import User
from app.schemas.chat import ChatRequest, ChatResponse, ChatHistoryItem
from app.routers.auth import get_current_user
from app.services.rag_chatbot import generate_rag_response

router = APIRouter(prefix="/api/chat", tags=["chat"])

@router.post("", response_model=ChatResponse)
async def ask_chatbot(req: ChatRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Ask a legal research question. Generates source-grounded answers (RAG)."""
    # Generate response
    rag_result = await generate_rag_response(db, req.message)
    
    # Save user message to history
    user_msg = ChatHistory(
        user_id=current_user.id,
        role="user",
        message=req.message
    )
    db.add(user_msg)
    
    # Save assistant message to history
    assistant_msg = ChatHistory(
        user_id=current_user.id,
        role="assistant",
        message=rag_result["response"]
    )
    db.add(assistant_msg)
    
    db.commit()
    
    return {
        "response": rag_result["response"],
        "source": rag_result["source"],
        "context": rag_result["context"]
    }

@router.get("/history", response_model=list[ChatHistoryItem])
def get_chat_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Retrieve chat history transcripts for the logged-in client."""
    history = db.query(ChatHistory).filter(ChatHistory.user_id == current_user.id).order_by(ChatHistory.timestamp.asc()).all()
    return history
