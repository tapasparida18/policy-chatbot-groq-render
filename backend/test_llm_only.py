from app.services.llm_service import LLMService
 
llm = LLMService()
 
chunks = [
    {
        "page": 7,
        "text": """
Standard working hours are 9:00 AM to 6:00 PM.
Employees must follow attendance requirements.
"""
    }
]
 
answer = llm.generate_answer(
    "What are the working hours?",
    chunks
)
 
print(answer)