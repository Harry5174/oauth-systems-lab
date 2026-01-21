from fastapi import HTTPException, Request

from app.asrv.storage import ACCESS_TOKENS


def get_bearer_token(request: Request) -> str:
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="missing bearer token")
    return auth.removeprefix("Bearer ").strip()


def validate_token(token: str):
    record = ACCESS_TOKENS.get(token)
    if not record:
        raise HTTPException(status_code=401, detail="invalid token")
    return record


def require_scope(token_record, required_scope: str):
    scopes = token_record.scope.split()
    if required_scope not in scopes:
        raise HTTPException(status_code=403, detail="insufficient scope")
