import faiss
import numpy as np
import pickle
import os


class VectorStore:

    def __init__(self, dimension=None):

        self.dimension = dimension
        self.index = None
        self.documents = []

    # ==========================================
    # ADD DOCUMENTS
    # ==========================================

    def add(self, embeddings, texts):

        embeddings = np.array(
            embeddings,
            dtype=np.float32
        )

        # Normalize for cosine similarity
        faiss.normalize_L2(embeddings)

        # Create FAISS index automatically
        if self.index is None:

            dimension = embeddings.shape[1]

            self.dimension = dimension

            self.index = faiss.IndexFlatIP(
                dimension
            )

        # Safety check
        if embeddings.shape[1] != self.index.d:

            raise ValueError(
                f"Embedding dimension mismatch: "
                f"FAISS expects {self.index.d}, "
                f"received {embeddings.shape[1]}"
            )

        # Add embeddings
        self.index.add(embeddings)

        # Store corresponding text
        self.documents.extend(texts)

    # ==========================================
    # NORMAL SEARCH
    # ==========================================

    def search(
        self,
        query_embedding,
        k=3,
        threshold=0.60,
        debug=False
    ):

        if self.index is None or self.index.ntotal == 0:
            return []

        query_embedding = np.asarray(
            [query_embedding],
            dtype=np.float32
        )

        # Normalize query for cosine similarity
        faiss.normalize_L2(query_embedding)

        # Don't request more documents than available
        search_k = min(k, self.index.ntotal)

        scores, indices = self.index.search(
            query_embedding,
            search_k
        )

        results = []

        for rank, (score, idx) in enumerate(
            zip(scores[0], indices[0]),
            start=1
        ):

            if idx < 0:
                continue

            if idx >= len(self.documents):
                continue

            result = {
                "rank": rank,
                "text": self.documents[idx],
                "score": float(score),
                "passed_threshold": float(score) >= threshold
            }

            results.append(result)

        # ==========================================
        # DEBUG OUTPUT
        # ==========================================

        if debug:

            print(
                "\n========== FAISS RETRIEVAL DEBUG =========="
            )

            for result in results:

                print(
                    f"\nRank: {result['rank']}"
                )

                print(
                    f"Score: {result['score']:.4f}"
                )

                print(
                    f"Passed threshold: "
                    f"{result['passed_threshold']}"
                )

                print("Text:")

                print(
                    result["text"][:500]
                )

            print(
                "\n============================================\n"
            )

        # Keep every retrieved chunk, ranked by similarity score.
        # `passed_threshold` is left on each result purely as a label
        # for display (e.g. a "Relevant" badge) -- it no longer removes
        # anything from the returned list.
        return results

    # ==========================================
    # DEBUG SEARCH
    #
    # Returns ALL top results,
    # including results below threshold.
    # ==========================================

    def search_debug(
        self,
        query_embedding,
        k=5
    ):

        if self.index is None or self.index.ntotal == 0:
            return []

        query_embedding = np.asarray(
            [query_embedding],
            dtype=np.float32
        )

        # Normalize query
        faiss.normalize_L2(query_embedding)

        # Don't request more documents than available
        search_k = min(k, self.index.ntotal)

        scores, indices = self.index.search(
            query_embedding,
            search_k
        )

        results = []

        for rank, (score, idx) in enumerate(
            zip(scores[0], indices[0]),
            start=1
        ):

            if idx < 0:
                continue

            if idx >= len(self.documents):
                continue

            results.append(
                {
                    "rank": rank,
                    "text": self.documents[idx],
                    "score": float(score)
                }
            )

        return results

    # ==========================================
    # SAVE
    # ==========================================

    def save(
        self,
        path="vector_db"
    ):

        # Make directory
        os.makedirs(
            path,
            exist_ok=True
        )

        # Save FAISS index
        faiss.write_index(
            self.index,
            f"{path}/index.faiss"
        )

        # Save documents
        with open(
            f"{path}/documents.pkl",
            "wb"
        ) as f:

            pickle.dump(
                self.documents,
                f
            )

    # ==========================================
    # LOAD
    # ==========================================

    def load(
        self,
        path="vector_db"
    ):

        # Load FAISS index
        self.index = faiss.read_index(
            f"{path}/index.faiss"
        )

        self.dimension = self.index.d

        # Load documents
        with open(
            f"{path}/documents.pkl",
            "rb"
        ) as f:

            self.documents = pickle.load(
                f
            )