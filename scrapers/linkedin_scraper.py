from __future__ import annotations

from typing import Dict, List
from urllib.parse import quote_plus

from bs4 import BeautifulSoup

from scrapers.base_scraper import BaseScraper

LINKEDIN_SEARCH_URL = "https://html.duckduckgo.com/html/?q=site:linkedin.com/company+{query}"

class LinkedInScraper(BaseScraper):
    async def search_and_extract(self, query: str) -> List[Dict[str, str]]:
        search_url = LINKEDIN_SEARCH_URL.format(query=quote_plus(query))
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36"
        }
        search_html = await self.request_manager.get_text(search_url, headers=headers)
        soup = BeautifulSoup(search_html, "lxml")
        profiles: List[str] = []

        for anchor in soup.select("a.result__url"):
            href = anchor.get("href") or ""
            # Parse DDG redirect
            if href.startswith("//duckduckgo.com/l/?uddg="):
                import urllib.parse
                parsed = urllib.parse.parse_qs(urllib.parse.urlparse(href).query)
                if "uddg" in parsed:
                    href = parsed["uddg"][0]
                    
            if "linkedin.com/company" in href and href not in profiles:
                profiles.append(href)

        results: List[Dict[str, str]] = []
        for url in profiles[:5]:
            profile = await self.enrich_from_profile(url, "LinkedIn")
            if not profile:
                continue
            results.append(
                self.build_record(
                    company_name=profile.get("description", "").split(" | ")[0],
                    decision_maker=profile.get("decision_maker", ""),
                    website=profile.get("website", ""),
                    address=profile.get("address", ""),
                    description=profile.get("description", ""),
                    email=profile.get("email", ""),
                    phone=profile.get("phone", ""),
                    source="linkedin",
                    additional_info=profile.get("additional_info", f"LinkedIn company profile: {url}"),
                )
            )
        return results
