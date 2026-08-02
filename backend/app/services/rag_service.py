import time


from app.services.embedding_service import EmbeddingService

from app.services.faiss_service import FAISSService

from app.services.llm_service import LLMService

#from app.services.reranker_service import RerankerService




class RAGService:


    def __init__(self):


        self.embedding_service = EmbeddingService()


        self.faiss_service = FAISSService()


        #self.reranker_service = RerankerService()


        self.llm_service = LLMService()


        self.faiss_service.load_index(

            "app/storage/faiss_index/policy_index.faiss",

            "app/storage/metadata/chunks.pkl"

        )


    def answer_question(

        self,

        question

    ):


        total_start = time.time()
        question_lower = question.strip().lower()

        if question_lower in [
            "hi",
            "hello", 
            "hey"
            "good morning",
            "good afternoon",
            "good evening",
            "how are you",
            "what's up",
            "how's it going",
            "greetings",
            "salutations",
            "hey there",
            "hi there",
            "hello there",
            "good day",
            ]:
            return {

                "answer": (

                    "Hello! How can I assist you with your policy? "

                ),

                "sources": [],

                "confidence_score": 1.0

            }
        if question_lower in [
            "thank you",
            "thanks",
            "much appreciated",
            "thanks a lot",
            "thanks so much",
            "thanks a ton",
            "thanks a million",
            "thanks a bunch",
            "thanks a heap",
            "thanks a load",
            "thanks a ton",
            "thanks a lot",
            "thanks a million",
            "thanks a bunch",
            "thanks a heap",
            "thanks a load",
        ]:
            return {

                "answer": (

                    "You're welcome! If you have any more questions "

                    "about the policy documents, feel free to ask."

                ),

                "sources": [],

                "confidence_score": 1.0

            }

        try:


            # =============================

            # Embedding Time

            # =============================


            embedding_start = time.time()


            query_embedding = self.embedding_service.embed_query(

                question

            )


            embedding_end = time.time()


            print(

                f"[TIMING] Embedding: "

                f"{embedding_end - embedding_start:.2f} sec"

            )


            # =============================

            # FAISS Search Time

            # =============================


            faiss_start = time.time()


            retrieved_chunks = self.faiss_service.search(

                query_embedding=query_embedding,

                top_k=20,

                min_score=0.50

            )


            faiss_end = time.time()


            print(

                f"[TIMING] FAISS Search: "

                f"{faiss_end - faiss_start:.2f} sec"

            )


            if not retrieved_chunks:


                total_end = time.time()


                print(

                    f"[TIMING] TOTAL: "

                    f"{total_end - total_start:.2f} sec"

                )


                return {

                    "answer": (

                        "The requested information is not available "

                        "in the uploaded policy documents."

                    ),

                    "sources": [],

                    "confidence_score": 0.0

                }


            # =============================

            # Reranker Time

            # =============================


            rerank_start = time.time()


            reranked_chunks = retrieved_chunks[:3]

            rerank_end = time.time()


            print(

                f"[TIMING] Reranker: "

                f"{rerank_end - rerank_start:.2f} sec"

            )


            # Prefer positive rerank scores


            reranked_chunks = reranked_chunks[:3]



            if not reranked_chunks:


                total_end = time.time()


                print(

                    f"[TIMING] TOTAL: "

                    f"{total_end - total_start:.2f} sec"

                )


                return {

                    "answer": (

                        "The requested information is not available "

                        "in the uploaded policy documents."

                    ),

                    "sources": [],

                    "confidence_score": 0.0

                }


            # Keep strongest chunks


            reranked_chunks = reranked_chunks[:3]


            # =============================

            # LLM Generation Time

            # =============================


            llm_start = time.time()


            answer = self.llm_service.generate_answer(

                question=question,

                retrieved_chunks=reranked_chunks

            )


            llm_end = time.time()


            print(

                f"[TIMING] LLM: "

                f"{llm_end - llm_start:.2f} sec"

            )


            # =============================

            # Sources

            # =============================


            sources = []


            for chunk in reranked_chunks:


                sources.append(

                    {

                        "page": chunk["page"],

                        "chunk_id": chunk["chunk_id"],

                        "section_title": chunk.get(

                            "section_title",

                            "General Policy Section"

                        ),

                        "faiss_score": round(

                            float(chunk.get("score", 0)),

                            4

                        ),

                        "rerank_score": 0,

                        

                        "preview": chunk["text"][:250]

                    }

                )


            confidence_score = round(

                float(

                    reranked_chunks[0].get(

                        "score",

                        0

                    )

                ),

                4

            )


            total_end = time.time()


            print(

                f"[TIMING] TOTAL: "

                f"{total_end - total_start:.2f} sec"

            )


            return {

                "answer": answer,

                "sources": sources,

                "confidence_score": confidence_score

            }


        except Exception as error:


            print("\n========== RAG ERROR ==========")


            print(error)


            return {

                "answer": (

                    "An error occurred while processing "

                    "the question."

                ),

                "sources": [],

                "confidence_score": 0.0

            }