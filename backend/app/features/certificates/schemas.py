from typing import Optional, List, Literal
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import date

Env = Literal["PROD", "UAT", "DEV"]
CertStatus = Literal["ACTIVE", "EXPIRED", "REPLACED", "REVOKED"]

class CertificateOut(BaseModel):
    id: UUID
    cert_name: str
    system_name: Optional[str] = None
    environment: Env
    cert_type: str

    owner_team: Optional[str] = None
    vendor: Optional[str] = None
    host: Optional[str] = None
    ip_address: Optional[str] = None

    issuer: Optional[str] = None
    subject: Optional[str] = None
    thumbprint: Optional[str] = None
    serial_number: Optional[str] = None

    start_date: Optional[date] = None
    expiry_date: date

    renewal_lead_days: int = 30
    status: CertStatus = "ACTIVE"
    notes: Optional[str] = None