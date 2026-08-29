class Router:

    def __init__(self):

        self.search_keywords = {

            "latest",
            "today",
            "news",
            "current",
            "recent",
            "yesterday",
            "live",
            "2025",
            "2026",
            "price",
            "stock",
            "weather",
            "score",
            "winner",
            "breaking",
            "update",
            "released",
            "launch",
            "election"

        }

    def should_search(self, question):

        question = question.lower()

        for keyword in self.search_keywords:

            if keyword in question:
                return True

        return False