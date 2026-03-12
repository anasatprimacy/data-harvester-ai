from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List


@dataclass
class QueryInput:
    keyword: str
    location: str | None = None
    industry: str | None = None


ERP_VARIANTS = [
    "ERP companies",
    "ERP software providers",
    "enterprise resource planning companies",
    "ERP vendors",
    "SAP partners",
    "Oracle ERP partners",
    "Microsoft Dynamics partners",
    "ERP implementation firms",
]


def build_queries(inputs: Iterable[QueryInput]) -> List[str]:
    """Generate global and location-specific query variants."""
    queries: List[str] = []
    for item in inputs:
        base = item.keyword.strip()
        if not base:
            continue
        has_location = bool(item.location)

        # Always include the base query.
        queries.append(base)

        # If seems ERP-related, add ERP variants.
        lower = base.lower()
        if any(k in lower for k in ["erp", "sap", "oracle", "odoo", "tally", "zoho"]):
            for variant in ERP_VARIANTS:
                if has_location:
                    queries.append(f"{variant} {item.location}")
                else:
                    queries.append(variant)
        else:
            # Generic expansions.
            if has_location:
                queries.append(f"{base} {item.location}")
                if item.industry:
                    queries.append(f"{base} {item.industry}".strip())
            else:
                if item.industry:
                    queries.append(f"{base} {item.industry}")

    # Deduplicate while preserving order; drop any query containing "nan" or "None".
    seen = set()
    uniq: List[str] = []
    for q in queries:
        if not q or "nan" in q.lower() or "none" in q.lower():
            continue
        if q not in seen:
            seen.add(q)
            uniq.append(q)
    return uniq

