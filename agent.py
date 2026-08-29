from llm import LLM


class Agent:

    def __init__(self):
        self.llm = LLM()

    def should_search(self, question):

        prompt = f"""
You are an AI assistant.

Decide if answering the user's question requires searching the internet.

Reply with ONLY one word.

YES
or
NO

Question:
{question}
"""

        answer = self.llm.generate(prompt)

        answer = answer.strip().upper()

        return answer.startswith("YES")