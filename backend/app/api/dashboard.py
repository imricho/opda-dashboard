from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from typing import Dict, Any

from app.services.dashboard_service import get_dashboard_repo
from app.auth.keycloak import require_roles

router = APIRouter(prefix="api/dashboard", tags=["dashboard"])

@router.get("/summary")
def summary(_payload: Dict[str, Any] = Depends(require_roles["OPDA_VIEWER", "OPDA_MANAGER", "OPDA_ADMIN"])):
    tiles = get_dashboard_repo().get_summary_tiles()
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tiles": tiles
    }