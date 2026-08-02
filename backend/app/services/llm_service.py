import os

import re


from groq import Groq

from dotenv import load_dotenv


from app.prompts.system_prompt import SYSTEM_PROMPT


load_dotenv()




class LLMService:


    def __init__(self):


        self.model_name = os.getenv(

            "GROQ_MODEL",

            "llama-3.1-8b-instant"

        )


        self.client = Groq(

            api_key=os.getenv(

                "GROQ_API_KEY"

            )

        )


    def generate_answer(

        self,

        question,

        retrieved_chunks

    ):


        context = self._build_context(

            retrieved_chunks

        )


        prompt = f"""

{SYSTEM_PROMPT}


You are an Enterprise Policy Assistant.


Employee Question:

{question}


Policy Context:

{context}


IMPORTANT RESPONSE RULES:


- Answer ONLY using the provided policy context.

- Give the final answer directly.

- Do not write the label "Answer:".

- Do not start with:

  "According to the policy"

  "According to the context"

  "Based on the policy"

  "The provided policy states"

- Do not repeat the question.

- Do not dump policy text.

- Do not give two alternative answers.

- Do not include an explanation in brackets.

- If an exact number, time, deadline, amount, or limit appears in the context, use that exact value in the answer.

- If the question asks for a number but the context mentions the topic without giving a number, say:

  "The document mentions this policy topic, but it does not specify the exact number."

- Keep the answer concise and professional.

- Keep the answer under 5 sentences.

- End with source page numbers in this format:

  Source: Page X


Generate only the final response now.

"""


        raw_answer = self._generate_with_groq(

            prompt

        )


        return self._clean_answer(

            raw_answer

        )


    def _generate_with_groq(

        self,

        prompt

    ):


        try:


            response = self.client.chat.completions.create(

                model=self.model_name,

                temperature=0.03,

                messages=[

                    {

                        "role": "user",

                        "content": prompt

                    }

                ]

            )


            return (

                response

                .choices[0]

                .message

                .content

                .strip()

            )


        except Exception as error:


            print(

                "\n========== GROQ ERROR =========="

            )


            print(error)


            return (

                f"Groq Error: {error}"

            )


    def _build_context(

        self,

        chunks

    ):


        context_blocks = []


        for chunk in chunks:


            page = chunk.get(

                "page",

                "Unknown"

            )


            section = chunk.get(

                "section_title",

                "General Policy Section"

            )


            text = chunk.get(

                "text",

                ""

            )[:350]


            context_blocks.append(

                f"""

Page: {page}


Section:

{section}


Content:

{text}

"""

            )


        return "\n".join(

            context_blocks

        )


    def _clean_answer(

        self,

        answer

    ):


        if not answer:

            return (

                "The requested information is not available "

                "in the uploaded policy documents."

            )


        cleaned = answer.strip()


        cleaned = re.sub(

            r"^\s*Answer\s*:\s*",

            "",

            cleaned,

            flags=re.IGNORECASE

        )


        cleaned = re.sub(

            r"\n\s*Answer\s*:\s*",

            "\n",

            cleaned,

            flags=re.IGNORECASE

        )


        cleaned = cleaned.replace(

            "According to the policy context, ",

            ""

        )


        cleaned = cleaned.replace(

            "According to the provided policy context, ",

            ""

        )


        cleaned = cleaned.replace(

            "According to the policy, ",

            ""

        )


        cleaned = cleaned.replace(

            "Based on the policy, ",

            ""

        )


        cleaned = cleaned.replace(

            "The provided policy states that ",

            ""

        )


        cleaned = re.sub(

            r"\n{3,}",

            "\n\n",

            cleaned

        )


        return cleaned.strip()