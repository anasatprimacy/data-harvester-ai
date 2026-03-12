from __future__ import annotations

from typing import Any, Dict, Iterable, List, Set, Tuple


def _dedupe_key(rec: Dict[str, Any]) -> Tuple[Any, Any, Any]:
    return (
        (rec.get("company_name") or rec.get("name") or "").lower(),
        (rec.get("website") or "").lower(),
        (rec.get("email") or "").lower(),
    )


def deduplicate(records: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen: Set[Tuple[Any, Any, Any]] = set()
    result: List[Dict[str, Any]] = []
    for rec in records:
        key = _dedupe_key(rec)
        if key in seen:
            continue
        seen.add(key)
        result.append(rec)
    return result

