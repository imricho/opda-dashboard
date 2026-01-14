from fastapi import APIRouter
from typing import List, Optional
import os
import psycopg
from psycopg.rows import dict_row

from .schemas import CertificateOut

router = APIRouter(prefix="/api/certificates", tags=["certificates"])

def get_conn():
    return psycopg.connect(os.environ["DATABASE_URL"], row_factory=dict_row)

@router.get("", response_model=List[CertificateOut])
def list_certificates(
        q: Optional[str] = None,
        environment: Optional[str] = None,
        status: Optional[str] = None,
        system_name: Optional[str] = None,
        exp_within_days: Optional[int] = None,  # e.g., 30
):
    where = []
    args = []

    if q:
        where.append("""
          (
            cert_name ilike %s
            or coalesce(system_name,'') ilike %s
            or coalesce(host,'') ilike %s
            or coalesce(issuer,'') ilike %s
          )
        """)
        args += [f"%{q}%", f"%{q}%", f"%{q}%", f"%{q}%"]

    if environment:
        where.append("environment = %s")
        args.append(environment)

    if status:
        where.append("status = %s")
        args.append(status)

    if system_name:
        where.append("system_name = %s")
        args.append(system_name)

    if exp_within_days is not None:
        where.append("expiry_date <= (current_date + (%s || ' days')::interval)")
        args.append(exp_within_days)

    clause = ("where " + " and ".join(where)) if where else ""

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                select
                  id,
                  cert_name,
                  system_name,
                  environment,
                  cert_type,
                  owner_team,
                  vendor,
                  host,
                  ip_address::text as ip_address,
                  serial_number,
                  issuer,
                  subject,
                  thumbprint,
                  start_date,
                  expiry_date,
                  renewal_lead_days,
                  status,
                  notes
                from certificates
                {clause}
                order by expiry_date asc
                """,
                args
            )
            return cur.fetchall()