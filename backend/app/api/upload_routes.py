from fastapi import APIRouter, UploadFile, File

import os




router = APIRouter()


UPLOAD_FOLDER = "app/storage/uploads"




@router.post("/upload")

async def upload_pdf(file: UploadFile = File(...)):


    os.makedirs(

        UPLOAD_FOLDER,

        exist_ok=True

    )


    file_path = os.path.join(

        UPLOAD_FOLDER,

        file.filename

    )


    with open(file_path, "wb") as buffer:


        content = await file.read()


        buffer.write(content)


    return {

        "message": "File uploaded successfully",

        "filename": file.filename

    }