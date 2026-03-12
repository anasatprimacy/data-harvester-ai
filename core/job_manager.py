from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List


@dataclass
class Job:
    query: str


class JobManager:
    def build_jobs(self, queries: Iterable[str]) -> List[Job]:
        return [Job(query=q) for q in queries]

