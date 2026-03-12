from __future__ import annotations

from typing import Any, Dict, List

from bs4 import BeautifulSoup

from extractors.email_extractor import extract_emails
from extractors.phone_extractor import extract_phones
from scrapers.base_scraper import BaseScraper


SEARCH_URL = "https://www.indiamart.com/search.mp?ss={query}"


class IndiaMartScraper(BaseScraper):
    async def search_and_extract(self, query: str) -> List[Dict[str, Any]]:
        url = SEARCH_URL.format(query=query.replace(" ", "+"))
        html = await self.request_manager.get_text(url)
        soup = BeautifulSoup(html, "lxml")

        records: List[Dict[str, Any]] = []
        # IndiaMART structure changes frequently; this is a heuristic targeting common patterns.
        for card in soup.select("div.l-cl.brdwhite.mkcl"):
            name_el = card.select_one("a.fs20")
            if not name_el:
                continue
            name = name_el.get_text(strip=True)
            profile_url = name_el.get("href") or ""

            addr_el = card.select_one(".fwn.grey-txt.fs12")
            address = addr_el.get_text(" ", strip=True) if addr_el else ""

            desc_el = card.select_one(".fs13")
            description = desc_el.get_text(" ", strip=True) if desc_el else ""

            phone_el = card.select_one(".nsup-txt")
            phone_text = phone_el.get_text(" ", strip=True) if phone_el else ""
            phones = extract_phones(phone_text)

            emails = extract_emails(description)

            records.append(
                {
                    "company_name": name,
                    "website": "",  # often hidden behind contact flow
                    "phone": phones[0] if phones else "",
                    "email": emails[0] if emails else "",
                    "address": address,
                    "industry": "",
                    "description": description,
                    "additional_info": f"IndiaMART profile: {profile_url}",
                    "source": "indiamart",
                }
            )

        return records

