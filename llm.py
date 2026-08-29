from google import genai
import streamlit as st


class LLM:

    def __init__(self):

        self.client = genai.Client(
            api_key=st.secrets["GEMINI_API_KEY"]
        )

        self.model = "gemini-3.5-flash-lite"


    def stream(self, prompt):

        try:

            response = self.client.models.generate_content_stream(
                model=self.model,
                contents=prompt
            )


            for chunk in response:

                if chunk.text:

                    yield {
                        "message": {
                            "content": chunk.text
                        }
                    }


        except Exception as e:

            error = str(e)

            print("Gemini Error:", error)


            if "429" in error or "RESOURCE_EXHAUSTED" in error:

                message = (
                    "⚠️ Gemini API quota exceeded. "
                    "Please try again later."
                )

            elif "401" in error or "API key" in error:

                message = (
                    "🔑 Invalid Gemini API key."
                )

            elif "500" in error or "503" in error:

                message = (
                    "⚠️ Gemini service is temporarily unavailable."
                )

            else:

                message = (
                    "❌ Unable to generate response."
                )


            yield {
                "message": {
                    "content": message
                }
            }