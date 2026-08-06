from fastapi import APIRouter

from pydantic import BaseModel

from pathlib import Path

import pickle


from app.services.rag_service import RAGService




router = APIRouter()


rag_service = RAGService()




class ChatRequest(BaseModel):

    question: str




CHUNKS_PATH = Path("app/storage/metadata/chunks.pkl")




def is_page_count_question(question: str) -> bool:

    question_lower = question.lower().strip()


    page_count_keywords = [

        "how many pages",

        "number of pages",

        "total pages",

        "pages are there",

        "page count",

        "how many page",

        "total number of pages"

    ]


    return any(keyword in question_lower for keyword in page_count_keywords)




def get_page_count_from_chunks() -> int | None:

    try:

        if not CHUNKS_PATH.exists():

            print("[PAGE_COUNT_ERROR] chunks.pkl file not found")

            return None


        with open(CHUNKS_PATH, "rb") as file:

            chunks = pickle.load(file)


        page_numbers = []


        for chunk in chunks:

            if isinstance(chunk, dict) and "page" in chunk:

                page_numbers.append(int(chunk["page"]))


        if not page_numbers:

            print("[PAGE_COUNT_ERROR] No page numbers found in chunks.pkl")

            return None


        return max(page_numbers)


    except Exception as error:

        print(f"[PAGE_COUNT_ERROR] Could not calculate page count: {error}")

        return None




@router.post("/chat")

def chat(request: ChatRequest):


    question = request.question.strip()


    if is_page_count_question(question):

        total_pages = get_page_count_from_chunks()


        if total_pages is not None:

            return {

                "answer": f"The uploaded policy document contains {total_pages} pages.",

                "sources": [],

                "confidence_score": 1.0

            }


        return {

            "answer": "I could not read the document page count right now.",

            "sources": [],

            "confidence_score": 0.0

        }


    result = rag_service.answer_question(

        question

    )


    return result