from __future__ import annotations

from typing import Any, Dict, Optional


def get_proxy_for_request(proxy_config: Dict[str, Any]) -> Optional[str]:
    if not proxy_config.get("enabled"):
        return None
    # Simple strategy: prefer HTTPS proxy, fall back to HTTP.
    https = proxy_config.get("https")
    http = proxy_config.get("http")
    return https or http

