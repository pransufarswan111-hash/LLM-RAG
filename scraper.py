import time
import requests
from bs4 import BeautifulSoup


class WebScraper:

    # Stop downloading once we have this many bytes — plenty for a lead
    # section + several sections of an article, no need for the whole page.
    MAX_BYTES = 300_000

    # Stop collecting paragraphs once we have this many — you only keep
    # the first 15 chunks downstream anyway, so there's no point walking
    # through hundreds of <p> tags on a long article.
    MAX_PARAGRAPHS = 40

    def __init__(self):

        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/138.0.0.0 Safari/537.36"
            )
        })

    def scrape(self, url):

        t0 = time.perf_counter()

        try:
            # Stream the response so we can stop reading once we have
            # enough bytes, instead of always downloading the full page.
            response = self.session.get(
                url,
                timeout=5,
                stream=True
            )
            response.raise_for_status()

            chunks = []
            downloaded = 0

            for chunk in response.iter_content(chunk_size=8192, decode_unicode=False):
                if not chunk:
                    break
                chunks.append(chunk)
                downloaded += len(chunk)
                if downloaded >= self.MAX_BYTES:
                    break

            response.close()

            raw_bytes = b"".join(chunks)
            html = raw_bytes.decode(response.encoding or "utf-8", errors="ignore")

            t_download = time.perf_counter() - t0

            t1 = time.perf_counter()

            soup = BeautifulSoup(html, "lxml")

            # Wikipedia-specific fast path: parse only the article body,
            # skipping sidebar/infobox/nav DOM nodes entirely instead of
            # decomposing them out of the full page tree.
            content_root = soup.select_one("#mw-content-text") or soup

            for tag in content_root([
                "script",
                "style",
                "noscript",
                "header",
                "footer",
                "nav",
                "aside",
                "svg",
                "img",
                "table",
                "form"
            ]):
                tag.decompose()

            paragraphs = []

            for p in content_root.find_all("p"):
                text = p.get_text(" ", strip=True)

                if len(text) > 50:
                    paragraphs.append(text)

                if len(paragraphs) >= self.MAX_PARAGRAPHS:
                    break

            t_parse = time.perf_counter() - t1

            print(
                f"[WebScraper] {url} download={t_download:.3f}s "
                f"({downloaded / 1024:.0f}KB, truncated={downloaded >= self.MAX_BYTES}) "
                f"parse={t_parse:.3f}s -> {len(paragraphs)} paragraphs"
            )

            return "\n\n".join(paragraphs)

        except Exception as e:

            print(f"Scraping Error ({url}):", e)

            return None