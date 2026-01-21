import time
import secrets
from dataclasses import dataclass

from typing import Dict


@dataclass(frozen=True)
class AuthCodeRecord:
    client_id: str
    redirect_uri: str
    scope: str
    code_challenge: str
    code_challenge_method: str
    issued_at: float
    


@dataclass(frozen=True)
class TokenRecord:
    client_id: str
    scope: str
    issued_at: float
    expires_in: int
    
    
AUTHORIZATION_CODES: Dict[str, AuthCodeRecord] = {}
ACCESS_TOKENS: Dict[str, TokenRecord] = {}

def issue_authorization_code(
    *,
    client_id: str,
    redirect_uri: str,
    scope: str,
    code_challenge: str,
    code_challenge_method: str,
)-> str:
    code = secrets.token_urlsafe(16)
    AUTHORIZATION_CODES[code] = AuthCodeRecord(
        client_id = client_id,
        redirect_uri = redirect_uri,
        scope = scope,
        code_challenge = code_challenge,
        code_challenge_method = code_challenge_method,
        issued_at = time.time()
    )
    
    return code

def pop_authorization_code(code: str) -> AuthCodeRecord | None:
    return AUTHORIZATION_CODES.pop(code, None)

def issue_access_token(
    *,
    client_id: str,
    scope: str,
    expires_in: int = 3600
)-> str:
    token = secrets.token_urlsafe(24)
    ACCESS_TOKENS[token] = TokenRecord(
        client_id=client_id,
        scope=scope,
        issued_at=time.time(),
        expires_in=expires_in
    )
    
    return token