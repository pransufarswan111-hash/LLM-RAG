import time
from ddgs import DDGS, results


class SearchEngine:

    def __init__(self):
        # Reuse a single DDGS session across all searches
        self.ddgs = DDGS(timeout=5)

    def search(self, query, max_results=8):

        t0 = time.perf_counter()

        try:
            results = list(
                self.ddgs.text(
                    query,
                    max_results=max_results,
                    region="wt-wt",
                    safesearch="off",
                )
            )

            print(
                f"[SearchEngine] query={query!r} "
                f"took {time.perf_counter() - t0:.3f}s "
                f"-> {len(results)} results"
            )

            for i, r in enumerate(results, 1):
                print(f"  [{i}] {r.get('title', '')} -> {r.get('href', '')}")

            return [
                {
                    "title": r.get("title", ""),
                    "url": r.get("href", ""),
                    "body": r.get("body", ""),
                }
                for r in results
            ]

        except Exception as e:
            print(f"[SearchEngine] failed after {time.perf_counter() - t0:.3f}s: {e}")
            return []