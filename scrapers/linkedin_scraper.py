from __future__ import annotations

from typing import Any, Dict, List

from bs4 import BeautifulSoup

from scrapers.base_scraper import BaseScraper

LINKEDIN_SEARCH_URL = "https://www.google.com/search?q=site:linkedin.com/company+{query}"


class LinkedInScraper(BaseScraper):
    async def search_and_extract(self, query: str) -> List[Dict[str, Any]]:
        # Use Google to discover LinkedIn company profile URLs, then do a light scrape.
        search_url = LINKEDIN_SEARCH_URL.format(query=query.replace(" ", "+"))
        search_html = await self.request_manager.get_text(search_url)
        soup = BeautifulSoup(search_html, "lxml")
        profiles: List[str] = []
        for a in soup.select("a"):
            href = a.get("href") or ""
            if "linkedin.com/company" in href and href not in profiles:
                profiles.append(href)

        results: List[Dict[str, Any]] = []
        for url in profiles[:5]:
            try:
                html = await self.request_manager.get_text(url)
            except Exception:
                continue
            psoup = BeautifulSoup(html, "lxml")
            name = psoup.find("h1")
            headline = psoup.find("h2")
            desc = headline.get_text(" ", strip=True) if headline else ""
            results.append(
                {
                    "company_name": name.get_text(" ", strip=True) if name else "",
                    "website": "",
                    "description": desc,
                    "source": "linkedin",
                }
            )
        return results

