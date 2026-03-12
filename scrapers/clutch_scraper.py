from __future__ import annotations

from typing import Any, Dict, List

from bs4 import BeautifulSoup

from scrapers.base_scraper import BaseScraper


SEARCH_URL = "https://clutch.co/search?search={query}"


class ClutchScraper(BaseScraper):
    async def search_and_extract(self, query: str) -> List[Dict[str, Any]]:
        url = SEARCH_URL.format(query=query.replace(" ", "+"))
        html = await self.request_manager.get_text(url)
        soup = BeautifulSoup(html, "lxml")

        records: List[Dict[str, Any]] = []
        # Clutch listing cards – heuristic selectors.
        for card in soup.select("li.provider"):
            name_el = card.select_one("h3.company_name a")
            if not name_el:
                continue
            name = name_el.get_text(strip=True)
            profile_url = name_el.get("href") or ""

            website_el = card.select_one("a.website-link__item")
            website = website_el.get("href") if website_el else ""

            desc_el = card.select_one(".company_info .field-content")
            description = desc_el.get_text(" ", strip=True) if desc_el else ""

            industry_el = card.select_one(".list-item.block-tagline")
            industry = industry_el.get_text(" ", strip=True) if industry_el else ""

            records.append(
                {
                    "company_name": name,
                    "website": website,
                    "phone": "",
                    "email": "",
                    "address": "",
                    "industry": industry,
                    "description": description,
                    "additional_info": f"Clutch profile: {profile_url}",
                    "source": "clutch",
                }
            )

        return records

