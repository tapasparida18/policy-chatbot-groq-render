from app.services.rag_service import RAGService
 
rag = RAGService()
 
question = "What are the working hours?"
 
query_embedding = rag.embedding_service.embed_query(
    question
)
 
retrieved = rag.faiss_service.search(
    query_embedding=query_embedding,
    top_k=20,
    min_score=0.35
)
 
reranked = rag.reranker_service.rerank(
    question=question,
    retrieved_chunks=retrieved,
    top_n=3
)
 
context = rag.llm_service._build_context(
    reranked
)
 
print("\nContext Length:")
print(len(context))
 
print("\nContext:\n")
print(context)