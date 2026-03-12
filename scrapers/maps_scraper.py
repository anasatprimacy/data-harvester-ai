from __future__ import annotations

from typing import Dict, List
from urllib.parse import quote_plus

from bs4 import BeautifulSoup

from scrapers.base_scraper import BaseScraper

MAPS_SEARCH_URL = "https://html.duckduckgo.com/html/?q={query}+location+address"

class MapsScraper(BaseScraper):
    async def search_and_extract(self, query: str) -> List[Dict[str, str]]:
        url = MAPS_SEARCH_URL.format(query=quote_plus(query))
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36"
        }
        
        html = await self.request_manager.get_text(url, headers=headers)
        soup = BeautifulSoup(html, "lxml")
        results: List[Dict[str, str]] = []

        for div in soup.select("div.result__body")[:5]:
            title_el = div.select_one("h2.result__title a.result__url")
            if not title_el:
                continue
            
            name = title_el.get_text(" ", strip=True)
            href = title_el.get("href", "")
            if href.startswith("//duckduckgo.com/l/?uddg="):
                import urllib.parse
                parsed = urllib.parse.parse_qs(urllib.parse.urlparse(href).query)
                if "uddg" in parsed:
                    href = parsed["uddg"][0]
            
            results.append(
                self.build_record(
                    company_name=name,
                    source="maps",
                    website=href if href.startswith("http") else "",
                    additional_info=f"Location result: {href}",
                )
            )
        return results
