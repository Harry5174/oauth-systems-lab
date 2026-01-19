from fastapi import APIRouter


from app.asrv.storage import (
    REGISTERED_REDIRECT_URIS,
    issue_authorization_code,
    pop_authorization_code,
    issue_access_token
)
from app.asrv.pkce import verify_pkce

router = APIRouter(tags=["authorization-server"])