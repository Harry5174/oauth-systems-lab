import httpx
from urllib.parse import urlparse
from fastapi import HTTPException

from app.cimd.types import ClientMetadata


def _is_allowed_http(client_id: str) -> bool:
    """Allow http only for 127.0.0.1/localhost (local CIMD testing)."""
    if not client_id.startswith("http://"):
        return False
    try:
        host = urlparse(client_id).hostname or ""
        return host in ("127.0.0.1", "localhost")
    except Exception:
        return False


async def fetch_client_metadata(client_id: str) -> ClientMetadata:
    # Invariant 1: HTTPS only (or http for 127.0.0.1/localhost in local testing)
    if not client_id.startswith("https://") and not _is_allowed_http(client_id):
        raise HTTPException(status_code=400, detail="client_id must be https")

    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            resp = await client.get(client_id)
    except Exception:
        raise HTTPException(status_code=400, detail="failed to fetch client metadata")

    if resp.status_code != 200:
        raise HTTPException(status_code=400, detail="metadata fetch failed")

    data = resp.json()

    # Parse + validate structure
    metadata = ClientMetadata.model_validate(data)

    # Invariant 3: self-identification
    if str(metadata.client_id) != client_id:
        raise HTTPException(status_code=400, detail="client_id mismatch in metadata")

    return metadata
