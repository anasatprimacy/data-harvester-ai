from __future__ import annotations

from typing import List

from bs4 import BeautifulSoup


def extract_addresses(html: str) -> List[str]:
    """Heuristic address extraction from HTML."""
    soup = BeautifulSoup(html or "", "lxml")
    candidates = []
    for tag in soup.find_all(["address"]):
        text = " ".join(tag.get_text(separator=" ", strip=True).split())
        if text:
            candidates.append(text)
    return candidates

