from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List

from utils.request_manager import RequestManager


class BaseScraper(ABC):
    """Abstract base class for all platform scrapers."""

    def __init__(self, request_manager: RequestManager) -> None:
        self.request_manager = request_manager

    async def initialize(self) -> None:
        """Optional async initialization hook (e.g. Playwright browser spin-up)."""
        return None

    @abstractmethod
    async def search_and_extract(self, query: str) -> List[Dict[str, Any]]:
        """Run the complete platform-specific search and extraction for a query."""
        raise NotImplementedError

