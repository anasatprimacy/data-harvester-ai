from __future__ import annotations

from typing import Any, Dict, Iterable, List

from processors.cleaner import clean_record
from processors.normalizer import normalize_record
from processors.company_enrichment import enrich_company
from processors.deduplicator import deduplicate
from utils.schema_formatter import to_output_schema


class Pipeline:
    def run(self, raw_records: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
        cleaned = [clean_record(r) for r in raw_records]
        normalized = [normalize_record(r) for r in cleaned]
        enriched = [enrich_company(r) for r in normalized]
        unique = deduplicate(enriched)
        return to_output_schema(unique)

