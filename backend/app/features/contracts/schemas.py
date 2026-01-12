from datetime import date
from typing import Optional, Literal
from pydantic import BaseModel, Field
from uuid import UUID

ContractStatus = Literal["ACTIVE", "EXPIRED", "TERMINATED"]

class ContractCreate(BaseModel):
    vendor_name: str = Field(min_length=1)
    contract_name: str = Field(min_length=1)
    start_date: Optional[date] = None
    expiry_date: date

    renewal_start_date: Optional[date] = None
    payment_window_start: Optional[date] = None
    payment_window_end: Optional[date] = None

    status: ContractStatus = "ACTIVE"
    notes: Optional[str] = None

class ContractOut(ContractCreate):
    id: UUID

class CalendarEvent(BaseModel):
    id: str
    title: str
    start: date
    end: Optional[date] = None
    allDay: bool = True
    type: str  # "contract"
    kind: str  # "expiry" | "renewal_start" | "payment_window"