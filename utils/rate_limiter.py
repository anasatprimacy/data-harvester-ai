from __future__ import annotations

import asyncio
import time
from contextlib import asynccontextmanager
from typing import AsyncIterator


class RateLimiter:
    """Simple token-bucket style rate limiter for async contexts."""

    def __init__(self, rate_per_sec: float, burst: int | None = None) -> None:
        self.rate_per_sec = rate_per_sec
        self.burst = burst or int(rate_per_sec)
        self.tokens = self.burst
        self.updated_at = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self.updated_at
            self.updated_at = now
            self.tokens = min(self.burst, self.tokens + elapsed * self.rate_per_sec)
            if self.tokens < 1:
                sleep_for = (1 - self.tokens) / self.rate_per_sec
                await asyncio.sleep(sleep_for)
                self.tokens = 0
            self.tokens -= 1

    @asynccontextmanager
    async def limit(self) -> AsyncIterator[None]:
        await self.acquire()
        yield

