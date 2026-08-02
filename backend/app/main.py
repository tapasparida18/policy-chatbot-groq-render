from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import FileResponse


from app.api.upload_routes import router as upload_router

from app.api.chat_routes import router as chat_router


app = FastAPI(

    title="Enterprise Policy Chatbot",

    description="RAG-based chatbot for company policy documents",

    version="1.0.0"

)


app.add_middleware(

    CORSMiddleware,

    allow_origins=[

        "https://policy-chatbot-groq-render.vercel.app"
        

    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)


app.include_router(

    upload_router,

    prefix="/api",

    tags=["Upload"]

)


app.include_router(

    chat_router,

    prefix="/api",

    tags=["Chat"]

)




@app.get("/")

def home():

    return {

        "message": "Enterprise Policy Chatbot Backend Running"

    }




@app.get("/health")

def health():

    return {

        "status": "healthy"

    }




@app.get("/pdf")

def get_pdf():


    return FileResponse(

        "app/storage/uploads/PolicyDetails.pdf",

        media_type="application/pdf"

    )