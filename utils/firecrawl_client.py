import requests
from config.env_config import config

class FirecrawlClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or config.firecrawl_api_key

    def scrape(self, url):
        try:
            headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
            response = requests.post("https://api.firecrawl.dev/v1/scrape", headers=headers, json={"url": url, "formats": ["markdown"]}, timeout=15)
            response.raise_for_status()
            data = response.json()
            if data.get("success"):
                return data.get("data", {}).get("markdown", "")
            return ""
        except Exception as e:
            print("Firecrawl error:", e)
            return ""
