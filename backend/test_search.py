from app.services.embedding_service import EmbeddingService
from app.services.faiss_service import FAISSService
 
embedding_service = EmbeddingService()
 
faiss_service = FAISSService()
 
faiss_service.load_index(
    "app/storage/faiss_index/policy_index.faiss",
    "app/storage/metadata/chunks.pkl"
)
 
query = "How many casual leaves are allowed?"
 
query_vector = embedding_service.embed_query(
    query
)
 
results = faiss_service.search(
    query_vector,
    top_k=3
)
 
for result in results:
 
    print("\n")
    print("Page:", result["page"])
    print("Score:", result["score"])
    print(result["text"][:500])