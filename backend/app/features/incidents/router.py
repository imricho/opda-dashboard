from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, Query

from app.auth.keycloak import require_roles
from app.features.incidents.service import get_incidents_repo

router = APIRouter(prefix="/api/incidents", tags=["incidents"])

@router.get("")
def list_incidents(
    _payload: Dict[str, Any] = Depends(require_roles("OPDA_VIEWER", "OPDA_MANAGER", "OPDA_ADMIN")),
    status: Optional[str] = Query(default="OPEN"),
    severity: Optional[str] = Query(default=None),
    app_code: Optional[str] = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0)
):
    repo = get_incidents_repo()
    items = repo.list_incidents(status=status, severity=severity, app_code=app_code, limit=limit, offset=offset)

    return {"items": items, "limit": limit, "offset": offset}