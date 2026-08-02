from fastapi import APIRouter
from pydantic import BaseModel
from app.services.rag_service import RAGService
 
router = APIRouter()
 
rag_service = RAGService()
 
 
class ChatRequest(BaseModel):
    question: str
 
 
@router.post("/chat")
def chat(request: ChatRequest):
 
    result = rag_service.answer_question(
        request.question
    )
 
    return result