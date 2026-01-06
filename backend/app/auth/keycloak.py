import os
from typing import Any, Dict, List, Optional, Set

import requests
from jose import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

KC_INTERNAL_BASE = os.getenv("KC_INTERNAL_BASE", "http://keycloak:8080/auth")
KC_REALM = os.getenv("KC_REALM", "opda-dashboard")
KC_EXTERNAL_ISSUER = os.getenv("KC_EXTERNAL_ISSUER", "http://localhost:8088/auth/realms/opda-dashboard")
KC_CLIENT_ID = os.getenv("KC_CLIENT_ID", "opda-frontend")

INTERNAL_ISSUER = f"{KC_INTERNAL_BASE}/realms/{KC_REALM}"
security = HTTPBearer(auto_error=True)
_JWKS_CACHE: Optional[Dict[str, Any]] = None

def _get_jwks() -> Dict[str, Any]:
    global _JWKS_CACHE
    if _JWKS_CACHE is not None:
        return _JWKS_CACHE

    discovery_url = f"{INTERNAL_ISSUER}/.well-known/openid-configuration"
    r = requests.get(discovery_url, timeout=10)
    if r.status_code != 200:
        raise HTTPException(status_code=503, detail=f"OIDC discovery failed ({r.status_code})")

    jwks_uri = r.json().get("jwks_uri")
    r2 = requests.get(jwks_uri, timeout=10)
    if r2.status_code != 200:
        raise HTTPException(status_code=503, detail=f"JWKS fetch failed ({r2.status_code})")

    _JWKS_CACHE = r2.json()
    return _JWKS_CACHE

def verify_access_token(token: str) -> Dict[str, Any]:
    jwks = _get_jwks()

    try:
        headers = jwt.get_unverified_header(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Token invalid: malformed header")

    kid = headers.get("kid")
    key = next((k for k in jwks.get("keys", []) if k.get("kid") == kid), None)
    if not key:
        raise HTTPException(status_code=401, detail="Token invalid: signing key not found")

    try:
        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            issuer=KC_EXTERNAL_ISSUER,
            options={"verify_aud": False, "verify_at_hash": False},
        )
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token invalid: {str(e)}")

    if payload.get("azp") != KC_CLIENT_ID:
        raise HTTPException(status_code=401, detail="Token invalid: wrong client (azp)")

    return payload

def get_current_user(creds: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    return verify_access_token(creds.credentials)

def require_roles(*required: str):
    required_set: Set[str] = set(required)

    def _dep(payload: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
        roles = set(payload.get("realm_access", {}).get("roles", []) or [])
        if required_set and roles.isdisjoint(required_set):
            raise HTTPException(status_code=403, detail="Forbidden: missing role")
        return payload

    return _dep