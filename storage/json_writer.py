from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, Mapping, Any


def write_json(path: Path, records: Iterable[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = list(records)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

