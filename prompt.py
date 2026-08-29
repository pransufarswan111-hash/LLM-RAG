class PromptBuilder:


    def build_prompt(self, question, context):

        prompt = f"""
You are a helpful AI assistant.

Answer the user's question using only the provided context.

If the context does not contain the answer, say:
"I don't have enough information."

Provide a clear and well-structured answer.

Context:
{context}


Question:
{question}


Answer:
"""

        return prompt