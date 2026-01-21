from fastapi import APIRouter, HTTPException, Query, Form
from fastapi.responses import RedirectResponse

from app.asrv.storage import (
    # REGISTERED_REDIRECT_URIS,
    issue_authorization_code,
    pop_authorization_code,
    issue_access_token,
)
from app.asrv.pkce import verify_pkce

from app.cimd.fetcher import fetch_client_metadata
from app.cimd.cache import get_cached, set_cached


router = APIRouter(tags=["authorization-server"])


@router.get("/authorize")
async def authorize(
    client_id: str = Query(...),
    response_type: str = Query(...),
    redirect_uri: str = Query(...),
    scope: str = Query(""),
    code_challenge: str = Query(...),
    code_challenge_method: str = Query("S256"),
):
    # Minimal strictness for Phase 3.2
    if response_type != "code":
        raise HTTPException(status_code=400, detail="unsupported response_type")

    if code_challenge_method != "S256":
        raise HTTPException(status_code=400, detail="unsupported code_challenge_method")

    metadata = get_cached(client_id)
    if not metadata:
        metadata = await fetch_client_metadata(client_id)
        set_cached(client_id, metadata)

    # Invariant 4: exact redirect match
    if redirect_uri not in [str(u) for u in metadata.redirect_uris]:
        raise HTTPException(status_code=400, detail="redirect_uri not registered")
        

    # Issue auth code
    code = issue_authorization_code(
        client_id=client_id,
        redirect_uri=redirect_uri,
        scope=scope,
        code_challenge=code_challenge,
        code_challenge_method=code_challenge_method,
    )

    # Redirect back with code
    sep = "&" if "?" in redirect_uri else "?"
    return RedirectResponse(url=f"{redirect_uri}{sep}code={code}", status_code=307)


@router.post("/token")
def token(
    grant_type: str = Form(...),
    code: str = Form(...),
    redirect_uri: str = Form(...),
    client_id: str = Form(...),
    code_verifier: str = Form(...),
):
    if grant_type != "authorization_code":
        raise HTTPException(status_code=400, detail="unsupported grant_type")

    record = pop_authorization_code(code)
    if not record:
        raise HTTPException(status_code=400, detail="invalid authorization code")

    # Bindings must match what was authorized
    if record.client_id != client_id:
        raise HTTPException(status_code=400, detail="client_id mismatch")
    if record.redirect_uri != redirect_uri:
        raise HTTPException(status_code=400, detail="redirect_uri mismatch")

    # PKCE verification
    if not verify_pkce(code_verifier, record.code_challenge, record.code_challenge_method):
        raise HTTPException(status_code=400, detail="PKCE verification failed")

    # Issue token
    access_token = issue_access_token(client_id=client_id, scope=record.scope)

    return {
        "access_token": access_token,
        "token_type": "Bearer",
        "expires_in": 3600,
        "scope": record.scope,
    }
