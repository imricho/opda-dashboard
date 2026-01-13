from fastapi import FastAPI, Depends
from typing import Any, Dict
from fastapi.middleware.cors import CORSMiddleware

from app.shared.feature_loader import register_feature_routers
from app.auth.keycloak import get_current_user

app = FastAPI(title="OPDeck")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

included, skipped = register_feature_routers(app)

@app.get("/api/health")
def health():
    return {"service": "opda-dashboard", "status": "ok", "features_included": included, "features_skipped": skipped}

@app.get("/api/me")
def me(payload: Dict[str, Any] = Depends(get_current_user)):
    username = payload.get("preferred_username") or payload.get("email") or payload.get("sub")
    roles = payload.get("realm_access", {}).get("roles", []) or []
    return {"username": username, "roles": roles}