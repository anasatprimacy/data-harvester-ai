from __future__ import annotations

from typing import List

from bs4 import BeautifulSoup


KEYWORDS = ["ceo", "founder", "co-founder", "cto", "cfo", "head of it", "it manager", "director"]


def extract_decision_makers(html: str) -> List[str]:
    """Very simple heuristic to pull potential decision maker names from about/leadership-like content."""
    soup = BeautifulSoup(html or "", "lxml")
    texts: List[str] = []
    for tag in soup.find_all(["p", "li", "h2", "h3", "h4"]):
        text = tag.get_text(separator=" ", strip=True)
        lower = text.lower()
        if any(k in lower for k in KEYWORDS):
            texts.append(text)
    return texts

