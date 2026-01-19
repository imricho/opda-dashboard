from __future__ import annotations

from fastapi import APIRouter
from .schemas import NotifyEventIn
from .repo import NotificationRepo
from .service import NotificationService

router = APIRouter(prefix="/api/notify", tags=["notifications"])

@router.post("/event")
def post_event(payload: NotifyEventIn):
    svc = NotificationService(NotificationRepo())
    return svc.ingest_event(payload.event_type, payload.data)