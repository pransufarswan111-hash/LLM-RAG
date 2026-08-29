from search import SearchEngine
from scraper import WebScraper
from prompt import PromptBuilder
from llm import LLM
from retriever import Retriever
from router import Router


def main():

    search = SearchEngine()
    scraper = WebScraper()
    prompt_builder = PromptBuilder()
    llm = LLM()
    retriever = Retriever()
    router = Router()

    while True:

        question = input("\nYou : ")

        if question.lower() == "exit":
            break

        # Ask the agent if web search is required
        need_search = router.should_search(question)
        if not need_search:

            print("\nUsing model knowledge...\n")

            answer = llm.generate(question)

            print("=" * 70)
            print(answer)
            print("=" * 70)

            continue

        print("\nSearching...")

        results = search.search(question)

        if not results:
            print("No search results found.")
            continue

        context = ""

        print("\nCollecting information...\n")

        for index, result in enumerate(results[:3], start=1):

            print(f"[{index}] Scraping: {result['url']}")

            text = scraper.scrape(result["url"])

            if not text:
                continue

            top_chunks = retriever.retrieve(question, text)

            print(f"Retrieved {len(top_chunks)} relevant chunks")

            context += f"\n========== SOURCE {index} ==========\n"
            context += f"Title : {result['title']}\n"
            context += f"URL   : {result['url']}\n\n"

            for chunk in top_chunks:
                context += chunk + "\n\n"

        print("\nThinking...\n")

        prompt = prompt_builder.build(question, context)

        answer = llm.generate(prompt)

        print("=" * 70)
        print(answer)
        print("=" * 70)

        print("\nSources Used:\n")

        for result in results[:3]:
            print(result["title"])
            print(result["url"])
            print()


if __name__ == "__main__":
    main()