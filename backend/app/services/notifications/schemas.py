from __future__ import annotations

from typing import Any, Dict, List, Optional, Literal
from pydantic import BaseModel, Field
from uuid import UUID

Channel = Literal["WHATSAPP"]
QueueStatus = Literal["PENDING", "SENT", "DELIVERED", "FAILED", "DEAD"]

class NotifyEventIn(BaseModel):
    event_type: str = Field(min_length=1)
    data: Dict[str, Any] = Field(default_factory=dict)

class RecipientOut(BaseModel):
    id: UUID
    display_name: str
    wa_phone_e164: Optional[str] = None
    enabled: bool
    labels: List[str] = []

class TemplateOut(BaseModel):
    id: UUID
    provider: str
    template_name: str
    language: str
    category: str
    schema: List[str]
    enabled: bool

class RuleOut(BaseModel):
    id: UUID
    feature: str
    event_type: str
    condition: Dict[str, Any]
    recipient_selector: Dict[str, Any]
    template_id: UUID
    throttle_seconds: int
    enabled: bool

class QueueItemOut(BaseModel):
    id: UUID
    rule_id: Optional[UUID] = None
    recipient_id: UUID
    channel: Channel
    payload: Dict[str, Any]
    status: QueueStatus
    attempts: int
    provider_message_id: Optional[str] = None
    last_error: Optional[str] = None