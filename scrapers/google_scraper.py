from __future__ import annotations

from typing import Any, Dict, List

from bs4 import BeautifulSoup

from extractors.email_extractor import extract_emails
from extractors.phone_extractor import extract_phones
from scrapers.base_scraper import BaseScraper

GOOGLE_SEARCH_URL = "https://www.google.com/search?q={query}"


class GoogleScraper(BaseScraper):
    async def search_and_extract(self, query: str) -> List[Dict[str, Any]]:
        url = GOOGLE_SEARCH_URL.format(query=query.replace(" ", "+"))
        html = await self.request_manager.get_text(url)
        soup = BeautifulSoup(html, "lxml")
        results: List[Dict[str, Any]] = []
        for div in soup.select("div.g"):
            title_el = div.select_one("h3")
            link_el = div.select_one("a")
            if not title_el or not link_el:
                continue
            name = title_el.get_text(strip=True)
            href = link_el.get("href") or ""
            snippet_el = div.select_one("span.aCOpRe, div.VwiC3b")
            description = snippet_el.get_text(" ", strip=True) if snippet_el else ""
            emails = extract_emails(description)
            phones = extract_phones(description)
            results.append(
                {
                    "company_name": name,
                    "website": href,
                    "description": description,
                    "email": emails[0] if emails else None,
                    "phone": phones[0] if phones else None,
                    "source": "google",
                }
            )
        return results

