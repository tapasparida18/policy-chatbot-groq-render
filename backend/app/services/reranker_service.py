from sentence_transformers import CrossEncoder
 
 
class RerankerService:
 
    def __init__(self):
 
        print("Loading reranker model...")
 
        self.model = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )
 
        print("Reranker model loaded successfully")
 
    def rerank(
        self,
        question,
        retrieved_chunks,
        top_n=3
    ):
 
        if not retrieved_chunks:
            return []
 
        pairs = []
 
        for chunk in retrieved_chunks:
            pairs.append(
                [
                    question,
                    chunk["text"]
                ]
            )
 
        scores = self.model.predict(pairs)
 
        reranked_results = []
 
        for chunk, rerank_score in zip(retrieved_chunks, scores):
 
            updated_chunk = chunk.copy()
 
            updated_chunk["rerank_score"] = float(rerank_score)
 
            reranked_results.append(updated_chunk)
 
        reranked_results = sorted(
            reranked_results,
            key=lambda item: item["rerank_score"],
            reverse=True
        )
 
        return reranked_results[:top_n]
 