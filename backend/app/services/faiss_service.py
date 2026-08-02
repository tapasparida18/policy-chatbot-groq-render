import os
import pickle
 
import faiss
import numpy as np
 
 
class FAISSService:
 
    def __init__(self):
        self.index = None
        self.metadata = []
 
    def create_index(self, embeddings):
 
        vectors = np.array(embeddings).astype("float32")
 
        dimension = vectors.shape[1]
 
        self.index = faiss.IndexFlatIP(dimension)
 
        self.index.add(vectors)
 
        print(f"FAISS index created with {self.index.ntotal} vectors")
 
    def add_metadata(self, chunks):
        self.metadata = chunks
 
    def save_index(self, index_path, metadata_path):
 
        os.makedirs(os.path.dirname(index_path), exist_ok=True)
        os.makedirs(os.path.dirname(metadata_path), exist_ok=True)
 
        faiss.write_index(self.index, index_path)
 
        with open(metadata_path, "wb") as file:
            pickle.dump(self.metadata, file)
 
        print("FAISS index and metadata saved successfully")
 
    def load_index(self, index_path, metadata_path):
 
        if not os.path.exists(index_path):
            raise FileNotFoundError(
                f"FAISS index not found at {index_path}"
            )
 
        if not os.path.exists(metadata_path):
            raise FileNotFoundError(
                f"Metadata file not found at {metadata_path}"
            )
 
        self.index = faiss.read_index(index_path)
 
        with open(metadata_path, "rb") as file:
            self.metadata = pickle.load(file)
 
        print("FAISS index and metadata loaded successfully")
 
    def search(
        self,
        query_embedding,
        top_k=20,
        min_score=0.35
    ):
 
        if self.index is None:
            raise ValueError("FAISS index is not loaded")
 
        query_vector = np.array(query_embedding).astype("float32")
 
        scores, indices = self.index.search(
            query_vector,
            top_k
        )
 
        results = []
 
        for score, index in zip(scores[0], indices[0]):
 
            if index == -1:
                continue
 
            score = float(score)
 
            if score < min_score:
                continue
 
            chunk = self.metadata[index]
 
            results.append(
                {
                    "score": score,
                    "chunk_id": chunk["chunk_id"],
                    "page": chunk["page"],
                    "section_title": chunk.get(
                        "section_title",
                        "General Policy Section"
                    ),
                    "text": chunk["text"]
                }
            )
 
        return results