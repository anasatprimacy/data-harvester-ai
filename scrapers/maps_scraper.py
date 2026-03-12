from __future__ import annotations

from typing import Any, Dict, List

from bs4 import BeautifulSoup

from scrapers.base_scraper import BaseScraper

MAPS_SEARCH_URL = "https://www.google.com/maps/search/{query}"


class MapsScraper(BaseScraper):
    async def search_and_extract(self, query: str) -> List[Dict[str, Any]]:
        # NOTE: Google Maps HTML is not stable; this is a best-effort basic scraper.
        url = MAPS_SEARCH_URL.format(query=query.replace(" ", "+"))
        html = await self.request_manager.get_text(url)
        soup = BeautifulSoup(html, "lxml")
        results: List[Dict[str, Any]] = []
        for item in soup.find_all("a"):
            name = item.get("aria-label")
            href = item.get("href", "")
            if not name or "/maps/place" not in href:
                continue
            results.append(
                {
                    "company_name": name,
                    "website": "",
                    "address": "",
                    "source": "maps",
                }
            )
        return results

