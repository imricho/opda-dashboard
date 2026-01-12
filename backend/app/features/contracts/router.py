from fastapi import APIRouter, Depends, Query
from datetime import date
from typing import List, Optional
from uuid import UUID
import psycopg
from psycopg.rows import dict_row

from .schemas import ContractCreate, ContractOut, CalendarEvent

router = APIRouter(prefix="/api/contracts", tags=["contracts"])

def get_conn():
    # Adjust to your existing DB connection approach if you already have one
    # Example expects DATABASE_URL in env
    import os
    return psycopg.connect(os.environ["DATABASE_URL"], row_factory=dict_row)

@router.post("", response_model=ContractOut)
def create_contract(payload: ContractCreate):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                insert into contracts
                (vendor_name, contract_name, start_date, expiry_date,
                 renewal_start_date, payment_window_start, payment_window_end,
                 status, notes)
                values
                    (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    returning id, vendor_name, contract_name, start_date, expiry_date,
                          renewal_start_date, payment_window_start, payment_window_end,
                          status, notes
                """,
                (
                    payload.vendor_name,
                    payload.contract_name,
                    payload.start_date,
                    payload.expiry_date,
                    payload.renewal_start_date,
                    payload.payment_window_start,
                    payload.payment_window_end,
                    payload.status,
                    payload.notes,
                ),
            )
            row = cur.fetchone()
            return row

@router.get("/schedule", response_model=List[CalendarEvent])
def contract_schedule(
        from_date: date = Query(..., alias="from"),
        to_date: date = Query(..., alias="to"),
        vendor: Optional[str] = None,
):
    """
    Returns FullCalendar-ready events in a date range.
    We'll create multiple events per contract:
      - renewal_start_date
      - payment window (range)
      - expiry_date
    """
    where_vendor = ""
    args = [from_date, to_date]

    if vendor:
        where_vendor = "and vendor_name ilike %s"
        args.append(f"%{vendor}%")

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                select id, vendor_name, contract_name,
                       renewal_start_date, payment_window_start, payment_window_end, expiry_date
                from contracts
                where
                  (
                    (renewal_start_date between %s and %s)
                    or (expiry_date between %s and %s)
                    or (
                      payment_window_start is not null and payment_window_end is not null
                      and payment_window_start <= %s and payment_window_end >= %s
                    )
                  )
                  {where_vendor}
                order by expiry_date asc
                """,
                # args: from,to repeated for checks
                [from_date, to_date, from_date, to_date, to_date, from_date] + (args[2:] if vendor else []),
                )
            rows = cur.fetchall()

    events: List[CalendarEvent] = []
    for r in rows:
        cid = str(r["id"])
        vendor_name = r["vendor_name"]
        contract_name = r["contract_name"]

        if r["renewal_start_date"]:
            events.append(
                CalendarEvent(
                    id=f"{cid}:renewal",
                    title=f"Renewal start: {vendor_name} — {contract_name}",
                    start=r["renewal_start_date"],
                    type="contract",
                    kind="renewal_start",
                )
            )

        if r["payment_window_start"] and r["payment_window_end"]:
            events.append(
                CalendarEvent(
                    id=f"{cid}:payment",
                    title=f"Payment window: {vendor_name}",
                    start=r["payment_window_start"],
                    end=r["payment_window_end"],
                    type="contract",
                    kind="payment_window",
                )
            )

        events.append(
            CalendarEvent(
                id=f"{cid}:expiry",
                title=f"Contract exp: {vendor_name} — {contract_name}",
                start=r["expiry_date"],
                type="contract",
                kind="expiry",
            )
        )

    return events