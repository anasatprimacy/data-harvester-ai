from __future__ import annotations

from typing import Any, Dict, List

from bs4 import BeautifulSoup

from extractors.phone_extractor import extract_phones
from scrapers.base_scraper import BaseScraper


SEARCH_URL = "https://www.justdial.com/search?type=company&what={query}"


class JustDialScraper(BaseScraper):
    async def search_and_extract(self, query: str) -> List[Dict[str, Any]]:
        url = SEARCH_URL.format(query=query.replace(" ", "+"))
        html = await self.request_manager.get_text(url)
        soup = BeautifulSoup(html, "lxml")

        records: List[Dict[str, Any]] = []
        # JustDial frequently changes layout; this targets generic listing containers.
        for card in soup.select("div.cntanr"):
            name_el = card.select_one("span.jcn a")
            if not name_el:
                continue
            name = name_el.get_text(strip=True)
            profile_url = name_el.get("href") or ""

            addr_el = card.select_one("span.cont_fl_addr")
            address = addr_el.get_text(" ", strip=True) if addr_el else ""

            cat_el = card.select_one("span.cntanr span a")
            category = cat_el.get_text(" ", strip=True) if cat_el else ""

            phone_el = card.select_one("p.contact-info span")
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
                    "additional_info": f"JustDial profile: {profile_url}",
                    "source": "justdial",
                }
            )

        return records

