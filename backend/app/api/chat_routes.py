from fastapi import APIRouter

from pydantic import BaseModel

from pathlib import Path


from app.services.rag_service import RAGService




router = APIRouter()


rag_service = RAGService()




class ChatRequest(BaseModel):

    question: str




PDF_PATH = Path("app/storage/uploads/PolicyDetails.pdf")




def is_page_count_question(question: str) -> bool:

    """

    Detects questions asking about total number of pages in the uploaded PDF.

    This avoids sending metadata questions to the RAG pipeline.

    """


    question_lower = question.lower().strip()


    page_count_keywords = [

        "how many pages",

        "number of pages",

        "total pages",

        "pages are there",

        "page count",

        "how many pages does the document have",

        "how many pages are in the document",

        "total number of pages"

        "How many pages are there in the document?",

    ]


    return any(keyword in question_lower for keyword in page_count_keywords)




def get_pdf_page_count() -> int | None:

    """

    Reads the uploaded policy PDF and returns the total number of pages.

    Uses the installed PDF library available in the project environment.

    """


    if not PDF_PATH.exists():

        return None


    try:

        try:

            from pypdf import PdfReader

        except ImportError:

            from PyPDF2 import PdfReader


        reader = PdfReader(str(PDF_PATH))

        return len(reader.pages)


    except Exception as error:

        print(f"[PAGE_COUNT_ERROR] Could not read PDF page count: {error}")

        return None




@router.post("/chat")

def chat(request: ChatRequest):


    question = request.question.strip()


    if is_page_count_question(question):

        total_pages = get_pdf_page_count()


        if total_pages is not None:

            return {

                "answer": f"The uploaded policy document contains {total_pages} pages.",

                "sources": [],

                "source_pages": []

            }


        return {

            "answer": "I could not read the PDF page count right now. Please make sure the policy PDF is available in the upload folder.",

            "sources": [],

            "source_pages": []

        }


    result = rag_service.answer_question(

        question

    )


    return result