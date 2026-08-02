import time

from sentence_transformers import SentenceTransformer
 
 
class EmbeddingService:
 
    def __init__(self):
 
        print("Loading embedding model...")
 
        self.model = SentenceTransformer(
            "BAAI/bge-small-en-v1.5"
        )
 
        print("Model Loaded Successfully")
 
    def embed_texts(self, texts):
 
        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            convert_to_numpy=True
        )
 
        return embeddings
 
    def embed_query(self, query):
 
        embedding = self.model.encode(
            [query],
            normalize_embeddings=True,
            convert_to_numpy=True
        )

        print(
            f"[EMBED_QUERY_ACTUAL] {time.time() - start_time:.2f} sec"
        )
 
        return embedding