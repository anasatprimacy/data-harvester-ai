from __future__ import annotations

from typing import Any, Dict


def normalize_phone(phone: str | None) -> str | None:
    if not phone:
        return None
    phone = phone.replace(" ", "").replace("-", "")
    return phone


def normalize_url(url: str | None) -> str | None:
    if not url:
        return None
    url = url.strip()
    if not url:
        return None
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url.lower()


def normalize_record(rec: Dict[str, Any]) -> Dict[str, Any]:
    rec = dict(rec)
    if "website" in rec:
        rec["website"] = normalize_url(rec.get("website"))
    if "phone" in rec:
        rec["phone"] = normalize_phone(rec.get("phone"))
    # Normalize casing for company name.
    if "company_name" in rec and isinstance(rec["company_name"], str):
        rec["company_name"] = rec["company_name"].strip()
    return rec

