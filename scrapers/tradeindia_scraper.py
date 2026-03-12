from __future__ import annotations

from typing import Any, Dict, List

from bs4 import BeautifulSoup

from extractors.phone_extractor import extract_phones
from scrapers.base_scraper import BaseScraper


SEARCH_URL = "https://www.tradeindia.com/search.html?search_text={query}"


class TradeIndiaScraper(BaseScraper):
    async def search_and_extract(self, query: str) -> List[Dict[str, Any]]:
        url = SEARCH_URL.format(query=query.replace(" ", "+"))
        html = await self.request_manager.get_text(url)
        soup = BeautifulSoup(html, "lxml")

        records: List[Dict[str, Any]] = []
        for card in soup.select("div.listing_product"):
            name_el = card.select_one("a.title")
            if not name_el:
                continue
            name = name_el.get_text(strip=True)
            profile_url = name_el.get("href") or ""

            addr_el = card.select_one(".listing_address")
            address = addr_el.get_text(" ", strip=True) if addr_el else ""

            cat_el = card.select_one(".listing_category")
            category = cat_el.get_text(" ", strip=True) if cat_el else ""

            phone_el = card.select_one(".contact_detail")
            phone_text = phone_el.get_text(" ", strip=True) if phone_el else ""
            phones = extract_phones(phone_text)

            records.append(
                {
                    "company_name": name,
                    "website": "",
                    "phone": phones[0] if phones else "",
                    "email": "",
                    "address": address,
                    "industry": category,
                    "description": "",
                    "additional_info": f"TradeIndia profile: {profile_url}",
                    "source": "tradeindia",
                }
            )

        return records

