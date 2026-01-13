from fastapi import APIRouter, Query
from typing import List, Optional
import os
import psycopg
from psycopg.rows import dict_row

from .schemas import ServerCreate, ServerOut

router = APIRouter(prefix="/api/servers", tags=["servers"])

def get_conn():
    return psycopg.connect(os.environ["DATABASE_URL"], row_factory=dict_row)

@router.get("", response_model=List[ServerOut])
def list_servers(
        q: Optional[str] = None,
        environment: Optional[str] = None,
        status: Optional[str] = None,
        app_name: Optional[str] = None,
):
    where = []
    args = []

    if q:
        where.append("(hostname ilike %s or coalesce(app_name,'') ilike %s or coalesce(location,'') ilike %s)")
        args += [f"%{q}%", f"%{q}%", f"%{q}%"]
    if environment:
        where.append("environment = %s")
        args.append(environment)
    if status:
        where.append("status = %s")
        args.append(status)
    if app_name:
        where.append("app_name = %s")
        args.append(app_name)

    clause = ("where " + " and ".join(where)) if where else ""

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                select id, hostname, environment, app_name,
                       ip_address::text as ip_address,
                       os, location, owner_team, criticality, status,
                       coalesce(tags, '{{}}') as tags, notes
                from servers
                {clause}
                order by hostname asc
                """,
                args
            )
            return cur.fetchall()

@router.post("", response_model=ServerOut)
def create_server(payload: ServerCreate):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                insert into servers
                (hostname, environment, app_name, ip_address, os, location, owner_team, criticality, status, tags, notes)
                values
                    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    returning id, hostname, environment, app_name,
                          ip_address::text as ip_address,
                          os, location, owner_team, criticality, status,
                          coalesce(tags,'{}') as tags, notes
                """,
                (
                    payload.hostname,
                    payload.environment,
                    payload.app_name,
                    payload.ip_address,
                    payload.os,
                    payload.location,
                    payload.owner_team,
                    payload.criticality,
                    payload.status,
                    payload.tags,
                    payload.notes,
                ),
            )
            return cur.fetchone()