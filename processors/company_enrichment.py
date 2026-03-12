from __future__ import annotations

from typing import Any, Dict

ERP_KEYWORDS = [
    "erp",
    "enterprise resource planning",
    "sap",
    "oracle erp",
    "netsuite",
    "microsoft dynamics",
    "odoo",
    "zoho erp",
    "tally erp",
    "infor erp",
]


def enrich_company(rec: Dict[str, Any]) -> Dict[str, Any]:
    rec = dict(rec)
    description = f"{rec.get('description', '')} {rec.get('industry', '')}".lower()

    if any(k in description for k in ERP_KEYWORDS):
        rec["industry_type"] = "ERP Software / ERP Consulting"
    else:
        if "industry" in rec and rec.get("industry"):
            rec["industry_type"] = rec["industry"]

    # Placeholder for size, turnover, etc. Real logic could inspect extra fields.
    return rec

