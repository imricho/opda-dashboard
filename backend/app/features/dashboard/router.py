from datetime import datetime, timezone
from typing import Any, Dict
from fastapi import APIRouter, Depends

from app.auth.keycloak import require_roles
from app.features.dashboard.service import get_dashboard_repo

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

@router.get("/summary")
def summary(_payload: Dict[str, Any] = Depends(require_roles("OPDA_VIEWER", "OPDA_MANAGER", "OPDA_ADMIN"))):
    tiles = get_dashboard_repo().get_summary_tiles()
    return {"generated_at": datetime.now(timezone.utc).isoformat(), "tiles": tiles}