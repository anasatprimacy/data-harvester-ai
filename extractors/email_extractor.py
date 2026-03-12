from __future__ import annotations

import re
from typing import List, Set


EMAIL_REGEX = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


def extract_emails(text: str) -> List[str]:
    matches = EMAIL_REGEX.findall(text or "")
    uniq: Set[str] = set(m.strip().lower() for m in matches)
    return sorted(uniq)

