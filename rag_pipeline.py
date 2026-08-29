from embedding_retriever import EmbeddingRetriever
from vector_store import VectorStore
from prompt import PromptBuilder
from llm import LLM
import os


class RAGPipeline:


    def __init__(self, documents):

        self.embedder = EmbeddingRetriever()

        self.vector_store = VectorStore(
        dimension=768
        )


        if os.path.exists("vector_db/index.faiss"):

            print("Loading existing vector database...")

            self.vector_store.load()


        else:

            print("Creating new vector database...")


            embeddings = self.embedder.create_embeddings(
                documents
            )


            self.vector_store.add(
                embeddings,
                documents
            )


            self.vector_store.save()


    def ask(self, question):


        query_embedding = self.embedder.create_embeddings(
            [question]
        )[0]


        results = self.vector_store.search(
            query_embedding
        )


        context = "\n".join(
            results
        )


        prompt = self.prompt_builder.build(
            question,
            context
        )


        answer = self.llm.generate(
            prompt
        )


        return answer