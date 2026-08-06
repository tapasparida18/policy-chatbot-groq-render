import time

from difflib import get_close_matches




from app.services.embedding_service import EmbeddingService


from app.services.faiss_service import FAISSService


from app.services.llm_service import LLMService


# from app.services.reranker_service import RerankerService




def normalize_question_text(question: str) -> str:

    """

    Performs lightweight typo correction before embedding generation.

    This improves retrieval quality for common spelling mistakes and

    abbreviations without changing the RAG architecture.

    """


    correction_dictionary = {

        "stndard": "standard",

        "standrd": "standard",

        "std": "standard",


        "wrokng": "working",

        "wrkng": "working",

        "workng": "working",

        "wrking": "working",


        "hsr": "hours",

        "hrs": "hours",

        "hr": "hour",


        "polcy": "policy",

        "polic": "policy",

        "plcy": "policy",


        "leav": "leave",

        "lev": "leave",


        "emplyee": "employee",

        "employe": "employee",

        "emp": "employee",


        "documnt": "document",

        "documnet": "document",

        "docs": "documents",


        "reimbursment": "reimbursement",

        "reimbrsmnt": "reimbursement",


        "attendence": "attendance",

        "attndance": "attendance",


        "timng": "timing",

        "ofice": "office",

        "aproval": "approval",

        "apprval": "approval"

    }


    vocabulary = [

        "standard",

        "working",

        "hours",

        "hour",

        "policy",

        "leave",

        "employee",

        "document",

        "documents",

        "attendance",

        "reimbursement",

        "holiday",

        "salary",

        "benefits",

        "office",

        "timing",

        "probation",

        "notice",

        "conduct",

        "training",

        "manager",

        "approval",

        "remote",

        "work",

        "lunch",

        "break",

        "core"

    ]


    words = question.split()

    corrected_words = []


    for word in words:

        prefix = ""

        suffix = ""

        actual_word = word


        while actual_word and not actual_word[0].isalnum():

            prefix += actual_word[0]

            actual_word = actual_word[1:]


        while actual_word and not actual_word[-1].isalnum():

            suffix = actual_word[-1] + suffix

            actual_word = actual_word[:-1]


        clean_word = actual_word.lower()


        if not clean_word:

            corrected_words.append(word)

            continue


        if clean_word in correction_dictionary:

            corrected_word = correction_dictionary[clean_word]

            corrected_words.append(

                f"{prefix}{corrected_word}{suffix}"

            )

            continue


        if len(clean_word) >= 4:

            close_matches = get_close_matches(

                clean_word,

                vocabulary,

                n=1,

                cutoff=0.82

            )


            if close_matches:

                corrected_words.append(

                    f"{prefix}{close_matches[0]}{suffix}"

                )

            else:

                corrected_words.append(word)

        else:

            corrected_words.append(word)


    corrected_question = " ".join(corrected_words)


    if corrected_question != question:

        print(f"[QUERY_NORMALIZATION] Original: {question}")

        print(f"[QUERY_NORMALIZATION] Corrected: {corrected_question}")


    return corrected_question




class RAGService:


    def __init__(self):


        self.embedding_service = EmbeddingService()


        self.faiss_service = FAISSService()


        # self.reranker_service = RerankerService()


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


        question = normalize_question_text(

            question.strip()

        )


        question_lower = question.lower()


        if question_lower in [

            "hi",

            "hello",

            "hey",

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

                top_k=3,

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


            # Keep strongest chunks

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
 