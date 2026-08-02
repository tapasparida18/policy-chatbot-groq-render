from app.services.pdf_service import extract_text_from_pdf
 
result = extract_text_from_pdf(
    "app/storage/uploads/PolicyDetails.pdf"
)
 
print(result[0])
