from fastapi import APIRouter, Request

from app.rsrv.auth import get_bearer_token, validate_token, require_scope

router = APIRouter(tags=["resource-server"])


@router.get("/resource/research")
def research_resource(request: Request):
    token = get_bearer_token(request)
    token_record = validate_token(token)
    require_scope(token_record, "research.read")

    return {
        "data": "📄 protected research data",
        "scope": token_record.scope,
    }
