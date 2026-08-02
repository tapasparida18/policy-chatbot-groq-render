from app.services.pdf_service import extract_text_from_pdf
from app.services.chunk_service import create_chunks
from app.services.embedding_service import EmbeddingService
from app.services.faiss_service import FAISSService
 
 
PDF_PATH = "app/storage/uploads/PolicyDetails.pdf"
 
pages = extract_text_from_pdf(PDF_PATH)
 
chunks = create_chunks(
    pages,
    chunk_size=500,
    overlap=100
)
 
print("Total chunks created:", len(chunks))
 
texts = [
    chunk["text"]
    for chunk in chunks
]
 
embedding_service = EmbeddingService()
 
embeddings = embedding_service.embed_texts(texts)
 
print("Embedding shape:", embeddings.shape)
 
faiss_service = FAISSService()
 
faiss_service.create_index(embeddings)
 
faiss_service.add_metadata(chunks)
 
faiss_service.save_index(
    "app/storage/faiss_index/policy_index.faiss",
    "app/storage/metadata/chunks.pkl"
)
 
print("FAISS index rebuilt successfully")
 