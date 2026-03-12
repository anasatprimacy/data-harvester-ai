from __future__ import annotations

from typing import Any, Dict, List

from bs4 import BeautifulSoup

from extractors.address_extractor import extract_addresses
from extractors.decision_maker_extractor import extract_decision_makers
from extractors.email_extractor import extract_emails
from extractors.phone_extractor import extract_phones
from scrapers.base_scraper import BaseScraper


class WebsiteScraper(BaseScraper):
    async def search_and_extract(self, query: str) -> List[Dict[str, Any]]:
        # Website scraper expects to be called with absolute URLs.
        # For now, treat the query as a URL if it looks like one, otherwise skip.
        if "http://" not in query and "https://" not in query:
            return []
        html = await self.request_manager.get_text(query)
        soup = BeautifulSoup(html, "lxml")
        title = soup.title.get_text(strip=True) if soup.title else query
        text = soup.get_text(" ", strip=True)
        emails = extract_emails(text)
        phones = extract_phones(text)
        addresses = extract_addresses(html)
        decisions = extract_decision_makers(html)
        return [
            {
                "company_name": title,
                "website": query,
                "email": emails[0] if emails else None,
                "phone": phones[0] if phones else None,
                "address": addresses[0] if addresses else None,
                "decision_maker": decisions[0] if decisions else None,
                "description": "",
                "source": "website",
            }
        ]

