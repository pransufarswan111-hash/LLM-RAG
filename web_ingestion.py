import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from search import SearchEngine
from scraper import WebScraper
from cleaner import TextCleaner
from retriever import Retriever
from embedding_retriever import EmbeddingRetriever
from vector_store import VectorStore


class WebIngestion:

    def __init__(self):

        self.search = SearchEngine()
        self.scraper = WebScraper()
        self.cleaner = TextCleaner()
        self.chunker = Retriever()
        self.embedder = EmbeddingRetriever()

        # nomic-embed-text embedding dimension
        self.vector_store = VectorStore(
            dimension=768
        )

    # ===================================
    # Process a single URL (instrumented)
    # ===================================
    def process_url(self, result, query):

        url = result["url"]
        t0 = time.perf_counter()

        text = self.scraper.scrape(url)
        t_scrape = time.perf_counter() - t0

        if not text:
            print(f"[{url}] scrape={t_scrape:.3f}s -> empty, skipped")
            return [], {"scrape": t_scrape, "clean": 0.0, "chunk": 0.0, "url": url}

        t1 = time.perf_counter()
        clean_text = self.cleaner.clean_text(text)
        t_clean = time.perf_counter() - t1

        t2 = time.perf_counter()
        chunks = self.chunker.split_into_chunks(clean_text)
        chunks = [chunk for chunk in chunks if len(chunk) > 100]

        # Rank by relevance to the query instead of just keeping
        # the first few chunks in page order (page order tends to
        # surface intro/marketing text ahead of actual content).
        chunks = self.chunker.rank_chunks(query, chunks, top_k=3)

        t_chunk = time.perf_counter() - t2

        print(
            f"[{url}] scrape={t_scrape:.3f}s clean={t_clean:.3f}s "
            f"chunk={t_chunk:.3f}s -> {len(chunks)} chunks"
        )

        return chunks, {"scrape": t_scrape, "clean": t_clean, "chunk": t_chunk, "url": url}

    # ===================================
    # Main Ingestion Pipeline (instrumented)
    # ===================================
    def ingest(self, query):

        stage_times = {}
        total_t0 = time.perf_counter()

        # Fresh vector store every search
        self.vector_store = VectorStore(dimension=768)

        # ---- Search ----
        t0 = time.perf_counter()
        results = self.search.search(query, max_results=3)
        stage_times["search"] = time.perf_counter() - t0
        print(f"[TIMING] search: {stage_times['search']:.3f}s -> {len(results)} results")

        if len(results) == 0:
            print("No search results found.")
            return self.vector_store

        all_chunks = []
        per_url_timings = []

        # ---- Parallel Scraping / Clean / Chunk ----
        t0 = time.perf_counter()
        with ThreadPoolExecutor(max_workers=max(3, len(results))) as executor:
            futures = [
                executor.submit(self.process_url, result, query)
                for result in results
            ]

            for future in as_completed(futures):
                try:
                    chunks, timing = future.result()
                    all_chunks.extend(chunks)
                    per_url_timings.append(timing)
                except Exception as e:
                    print("Thread Error:", e)

        stage_times["scrape_clean_chunk_parallel_wall_time"] = time.perf_counter() - t0

        all_chunks = all_chunks[:12]
        print("Total chunks:", len(all_chunks))

        if len(all_chunks) == 0:
            print("No useful content found.")
            return self.vector_store

        # ---- Embedding ----
        t0 = time.perf_counter()
        embeddings = self.embedder.create_embeddings(all_chunks)
        stage_times["embedding"] = time.perf_counter() - t0
        print(f"[TIMING] embedding ({len(all_chunks)} chunks): {stage_times['embedding']:.3f}s")

        # ---- Vector store add ----
        t0 = time.perf_counter()
        self.vector_store.add(embeddings, all_chunks)
        stage_times["vector_store_add"] = time.perf_counter() - t0

        stage_times["ingest_total"] = time.perf_counter() - total_t0

        print("Knowledge base ready!")
        print(f"[TIMING BREAKDOWN] {stage_times}")
        print(f"[PER-URL TIMING] {per_url_timings}")

        return self.vector_store