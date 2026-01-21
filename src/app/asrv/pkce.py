import base64
import hashlib


def s256(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("utf-8")


def verify_pkce(code_verifier: str, code_challenge: str, method: str) -> bool:
    # For Phase 3.2, we only support S256. Spec sends "S256", accept case-insensitively.
    if method.upper() != "S256":
        return False
    return s256(code_verifier) == code_challenge