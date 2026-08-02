from app.services.pdf_service import extract_text_from_pdf
from app.services.chunk_service import create_chunks
from app.services.embedding_service import EmbeddingService
 
# Load PDF
 
pages = extract_text_from_pdf(
    "app/storage/uploads/PolicyDetails.pdf"
)
 
# Create Chunks
 
chunks = create_chunks(pages)
 
print("Chunks Created:", len(chunks))
 
# Extract chunk texts
 
texts = [chunk["text"] for chunk in chunks]
 
# Load model
 
embedding_service = EmbeddingService()
 
# Generate embeddings
 
embeddings = embedding_service.embed_texts(
    texts
)
 
print("\nEmbedding Shape:")
print(embeddings.shape)


 