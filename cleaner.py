import re


class TextCleaner:


    def clean_text(self, text):

        # remove extra spaces
        text = re.sub(
            r'\s+',
            ' ',
            text
        )


        # remove common web noise
        noise = [
            "privacy policy",
            "cookie policy",
            "sign in",
            "create account",
            "subscribe",
            "login"
        ]


        for item in noise:
            text = re.sub(
                item,
                "",
                text,
                flags=re.IGNORECASE
            )


        return text.strip()