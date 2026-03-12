from __future__ import annotations

import re
from typing import List, Set


PHONE_REGEX = re.compile(r"(\+?\d[\d \-]{8,}\d)")


def extract_phones(text: str) -> List[str]:
    matches = PHONE_REGEX.findall(text or "")
    uniq: Set[str] = set(m.strip() for m in matches)
    return sorted(uniq)

