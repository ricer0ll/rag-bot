from ddgs import DDGS
import re

class DDGSClient:
    """
    The class that handles all websearch related tasks
    """
    def __init__(self):
        self.ddgs = DDGS()
    
    def search(self, query: str) -> list:
        results = self.ddgs.text(query, max_results=3, page=5, backend="auto")

        pattern = r"\[\d+\]"
        body = []
        for result in results:
            cleaned_body = re.sub(pattern, '', result["body"])
            if any(cleaned_body == entry["body"] for entry in body):
                continue

            title = result['title']
            link = result['href']
            body.append({
                "title": title,
                "link": link,
                "body": cleaned_body
            })

        return body