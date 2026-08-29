import math
import re
from collections import Counter


class Retriever:

    def __init__(self):
        pass

    # -------------------------------
    # Tokenize text
    # -------------------------------
    def tokenize(self, text):

        text = text.lower()

        words = re.findall(r"\b[a-zA-Z0-9]+\b", text)

        return words

    # -------------------------------
    # Split webpage into chunks
    # -------------------------------
    def split_into_chunks(self, text):

        # Split on blank lines
        chunks = re.split(r"\n\s*\n", text)

        # Remove very small chunks
        chunks = [chunk.strip() for chunk in chunks if len(chunk.strip()) > 80]

        # If everything became one chunk,
        # split into fixed-size chunks.
        if len(chunks) <= 1:

            words = text.split()

            chunks = []

            chunk_size = 250

            for i in range(0, len(words), chunk_size):

                chunk = " ".join(words[i:i + chunk_size])

                if len(chunk) > 80:
                    chunks.append(chunk)

        return chunks

    # -------------------------------
    # Term Frequency
    # -------------------------------
    def compute_tf(self, words):

        total = len(words)

        if total == 0:
            return {}

        counts = Counter(words)

        tf = {}

        for word, count in counts.items():
            tf[word] = count / total

        return tf

    # -------------------------------
    # Inverse Document Frequency
    # -------------------------------
    def compute_idf(self, documents):

        N = len(documents)

        vocabulary = set()

        for doc in documents:
            vocabulary.update(doc)

        idf = {}

        for word in vocabulary:

            containing = 0

            for doc in documents:

                if word in doc:
                    containing += 1

            idf[word] = math.log((N + 1) / (containing + 1)) + 1

        return idf

    # -------------------------------
    # TF-IDF Vector
    # -------------------------------
    def compute_vector(self, tf, idf):

        vector = {}

        for word, value in tf.items():

            vector[word] = value * idf.get(word, 1.0)

        return vector

    # -------------------------------
    # Cosine Similarity
    # -------------------------------
    def cosine_similarity(self, vec1, vec2):

        dot = 0

        for word in vec1:

            if word in vec2:
                dot += vec1[word] * vec2[word]

        mag1 = math.sqrt(sum(v * v for v in vec1.values()))
        mag2 = math.sqrt(sum(v * v for v in vec2.values()))

        if mag1 == 0 or mag2 == 0:
            return 0

        return dot / (mag1 * mag2)

    # -------------------------------
    # Main Retrieval Function
    # -------------------------------
    def retrieve(self, question, text, top_k=5):

        chunks = self.split_into_chunks(text)

        if not chunks:
            return []

        # Tokenize every chunk
        documents = [self.tokenize(chunk) for chunk in chunks]

        # Include question in IDF calculation
        question_tokens = self.tokenize(question)

        all_documents = documents + [question_tokens]

        idf = self.compute_idf(all_documents)

        question_tf = self.compute_tf(question_tokens)

        question_vector = self.compute_vector(question_tf, idf)

        scored_chunks = []

        for chunk, tokens in zip(chunks, documents):

            chunk_tf = self.compute_tf(tokens)

            chunk_vector = self.compute_vector(chunk_tf, idf)

            score = self.cosine_similarity(question_vector, chunk_vector)

            scored_chunks.append((score, chunk))

        scored_chunks.sort(key=lambda x: x[0], reverse=True)

        return [chunk for score, chunk in scored_chunks[:top_k]]
    