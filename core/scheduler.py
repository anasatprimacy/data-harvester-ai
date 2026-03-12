from __future__ import annotations

from typing import Iterable, List

from core.job_manager import Job


class Scheduler:
    """Simple FIFO scheduler for now; can be extended to priority / rate-based."""

    def schedule(self, jobs: Iterable[Job]) -> List[Job]:
        return list(jobs)

