from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable, Mapping, Any, List

from utils.schema_formatter import OUTPUT_FIELDS


def write_csv(path: Path, records: Iterable[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows: List[Mapping[str, Any]] = list(records)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in OUTPUT_FIELDS})

