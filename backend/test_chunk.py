from app.services.pdf_service import extract_text_from_pdf
from app.services.chunk_service import create_chunks
 
pages = extract_text_from_pdf(
    "app/storage/uploads/PolicyDetails.pdf"
)
 
chunks = create_chunks(pages)
 
print("Total Chunks:", len(chunks))
 
print("\nFirst Chunk:\n")
print(chunks[0]["text"][:500])