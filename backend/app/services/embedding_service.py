import time

import torch


from sentence_transformers import SentenceTransformer




# Reduce CPU thread overhead on Railway

torch.set_num_threads(1)




class EmbeddingService:


    def __init__(self):


        print("Loading embedding model...")


        self.model = SentenceTransformer(

            "BAAI/bge-small-en-v1.5",

            device="cpu"

        )


        # Warmup once during startup

        self.model.encode(

            ["warmup query"],

            normalize_embeddings=True,

            convert_to_numpy=True,

            show_progress_bar=False

        )


        print("Model Loaded Successfully")


    def embed_texts(self, texts):


        with torch.inference_mode():


            embeddings = self.model.encode(

                texts,

                normalize_embeddings=True,

                convert_to_numpy=True,

                show_progress_bar=False

            )


        return embeddings


    def embed_query(self, query):


        start_time = time.time()


        with torch.inference_mode():


            embedding = self.model.encode(

                [query],

                normalize_embeddings=True,

                convert_to_numpy=True,

                show_progress_bar=False

            )


        print(

            f"[EMBED_QUERY_ACTUAL] {time.time() - start_time:.2f} sec"

        )


        return embedding