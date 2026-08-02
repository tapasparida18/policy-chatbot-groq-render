from app.services.rag_service import RAGService





rag_service = RAGService()



questions = [

"What are the working hours?",

"What is the dress code policy?",

"How many casual leaves are allowed?",

"What is the travel reimbursement process?",

"What happens if an employee violates security policy?"

]



for question in questions:



 print("\n" + "=" * 80)



 print("Question:")

 print(question)



 result = rag_service.answer_question(question)



 print("\nAnswer:")

 print(result["answer"])



 print("\nConfidence Score:")

 print(result["confidence_score"])



 print("\nSources:")



 for source in result["sources"]:



  print("-" * 50)

  print("Page:", source["page"])

  print("Section:", source["section_title"])

  print("FAISS Score:", source["faiss_score"])

  print("Rerank Score:", source["rerank_score"])

  print("Preview:", source["preview"])