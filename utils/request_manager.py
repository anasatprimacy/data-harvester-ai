from __future__ import annotations

from typing import Any, Dict, Optional

import aiohttp
from tenacity import retry, stop_after_attempt, wait_exponential
import random

from utils.proxy_manager import get_proxy_for_request


USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36",
]


class RequestManager:
    def __init__(self, proxy_config: Dict[str, Any] | None = None, timeout: int = 20, delay_seconds: float = 1.0) -> None:
        self.proxy_config = proxy_config or {}
        self.timeout = timeout
        self._session: Optional[aiohttp.ClientSession] = None
        self.delay_seconds = delay_seconds

    async def __aenter__(self) -> "RequestManager":
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        self._session = aiohttp.ClientSession(timeout=timeout)
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if self._session:
            await self._session.close()
            self._session = None

    @retry(wait=wait_exponential(multiplier=1, min=1, max=10), stop=stop_after_attempt(3))
    async def get_text(self, url: str, *, headers: Dict[str, str] | None = None) -> str:
        if not self._session:
            raise RuntimeError("RequestManager session not initialized")

        proxy = get_proxy_for_request(self.proxy_config)
        base_headers: Dict[str, str] = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept-Language": "en-US,en;q=0.9",
        }
        if headers:
            base_headers.update(headers)

        async with self._session.get(url, headers=base_headers, proxy=proxy) as resp:
            resp.raise_for_status()
            return await resp.text()

