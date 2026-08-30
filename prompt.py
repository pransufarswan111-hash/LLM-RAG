class PromptBuilder:


    def build_prompt(self, question, context, history_text=""):

        history_section = ""

        if history_text:

            history_section = f"""
Recent conversation (for context only -- the user's new question may be
a short follow-up that refers back to this, e.g. "and of uk" after
"capital of india" means "what is the capital of uk"):
{history_text}
"""

        prompt = f"""
You are a helpful AI assistant.
{history_section}
Answer the user's new question using only the provided context below.
Use the recent conversation above only to understand what the user is
referring to -- do not answer from it directly if the context has the
real answer.

If the context does not contain the answer, say:
"I don't have enough information."

Provide a clear and well-structured answer.

Context:
{context}


New Question:
{question}


Answer:
"""

        return prompt


    def build_direct_prompt(self, question, history_text=""):

        history_section = ""

        if history_text:

            history_section = f"""
Recent conversation (for context only -- the user's new question may be
a short follow-up that refers back to this):
{history_text}
"""

        prompt = f"""
You are a helpful, knowledgeable AI assistant.
{history_section}
Answer the user's question thoroughly and directly using your own
knowledge. Be concrete and specific -- if asked to teach a topic
(e.g. a language, a skill, a concept), give real, usable content
(actual vocabulary, real examples, concrete steps), not a general
description of where one could learn it.

Question:
{question}


Answer:
"""

        return prompt