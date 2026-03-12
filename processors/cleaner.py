from __future__ import annotations

from typing import Any, Dict

from extractors.email_extractor import EMAIL_REGEX


def clean_record(rec: Dict[str, Any]) -> Dict[str, Any]:
    cleaned: Dict[str, Any] = {}
    for k, v in rec.items():
        if isinstance(v, str):
            v2 = v.strip()
            cleaned[k] = v2 if v2 else None
        else:
            cleaned[k] = v

    # Remove invalid email formats.
    email = cleaned.get("email")
    if email and not EMAIL_REGEX.fullmatch(email):
        cleaned["email"] = None

    # Remove malformed URLs (very basic).
    url = cleaned.get("website")
    if isinstance(url, str) and url and "." not in url:
        cleaned["website"] = None

    return cleaned

