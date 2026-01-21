import time
from typing import Dict, Tuple

from app.cimd.types import ClientMetadata

_CACHE: Dict[str, Tuple[ClientMetadata, float]] = {}
TTL_SECONDS = 300  # 5 minutes (recommended default)


def get_cached(client_id: str) -> ClientMetadata | None:
    entry = _CACHE.get(client_id)
    if not entry:
        return None

    metadata, expires_at = entry
    if time.time() > expires_at:
        _CACHE.pop(client_id, None)
        return None

    return metadata


def set_cached(client_id: str, metadata: ClientMetadata):
    _CACHE[client_id] = (metadata, time.time() + TTL_SECONDS)


def revoke(client_id: str):
    _CACHE.pop(client_id, None)
