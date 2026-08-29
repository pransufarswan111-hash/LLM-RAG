from sentence_transformers import SentenceTransformer
import numpy as np


class EmbeddingRetriever:

    def __init__(self):
        # 768-dimensional embeddings
        self.model = SentenceTransformer("BAAI/bge-small-en-v1.5")

    def create_embeddings(self, texts):

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            convert_to_numpy=True
        )

        return np.asarray(
            embeddings,
            dtype=np.float32
        )