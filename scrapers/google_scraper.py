from __future__ import annotations

from typing import Dict, List
from urllib.parse import quote_plus

from bs4 import BeautifulSoup

from extractors.email_extractor import extract_emails
from extractors.phone_extractor import extract_phones
from scrapers.base_scraper import BaseScraper

# Using DuckDuckGo HTML instead of Google as it has zero bot protection and no JS required
DDG_SEARCH_URL = "https://html.duckduckgo.com/html/?q={query}"


class GoogleScraper(BaseScraper):
    async def search_and_extract(self, query: str) -> List[Dict[str, str]]:
        url = DDG_SEARCH_URL.format(query=quote_plus(query))
        
        # DDG requires a real user agent
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36"
        }
        
        html = await self.request_manager.get_text(url, headers=headers)
        soup = BeautifulSoup(html, "lxml")
        results: List[Dict[str, str]] = []

        # Parse DuckDuckGo results
        for div in soup.select("div.result__body")[:10]:
            title_el = div.select_one("h2.result__title a.result__url")
            if not title_el:
                continue

            href = title_el.get("href") or ""
            # DDG injects redirect URLs, let's try to parse the actual URL or just use it
            if href.startswith("//duckduckgo.com/l/?uddg="):
                import urllib.parse
                parsed = urllib.parse.parse_qs(urllib.parse.urlparse(href).query)
                if "uddg" in parsed:
                    href = parsed["uddg"][0]
            elif href.startswith("/url"):
                pass  # google style ?

            description_el = div.select_one("a.result__snippet")
            description = description_el.get_text(" ", strip=True) if description_el else ""
            
            emails = extract_emails(description)
            phones = extract_phones(description)
            profile_data = {}
            if href.startswith("http"):
                profile_data = await self.enrich_from_profile(href, "Search")

            record = self.build_record(
                company_name=title_el.get_text(" ", strip=True),
                website=href,
                description=description,
                email=emails[0] if emails else "",
                phone=phones[0] if phones else "",
                source="google",  # Keep source as google to maintain system compatibility
                additional_info=f"Search result for query: {query}",
            )
            results.append(self.merge_records(record, profile_data))

        return results

