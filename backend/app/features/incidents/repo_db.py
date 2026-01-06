from typing import Dict, Any, List, Optional
from app.shared.db import get_conn


class IncidentsDbRepository:
    def list_incidents(
            self,
            status: Optional[str],
            severity: Optional[str],
            app_code: Optional[str],
            limit: int,
            offset: int
    ) -> List[Dict[str, Any]]:
        where = []
        params: List[Any] = []

        if status:
            where.append("status = %s")
            params.append(status)
        if severity:
            where.append("severity = %s")
            params.append(severity)
        if app_code:
            where.append("app_code = %s")
            params.append(app_code)

        where_sql = ("WHERE " + " AND ".join(where)) if where else ""

        sql = f"""
            SELECT id, severity, status, title, app_code, created_at, sla_due_at
            FROM incidents
            {where_sql}
            ORDER BY created_at DESC
            LIMIT %s OFFSET %s;
        """
        params.extend([limit, offset])

        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, tuple(params))
                rows = cur.fetchall()

        items: List[Dict[str, Any]] = []
        for r in rows:
            items.append(
                {
                    "id": r[0],
                    "severity": r[1],
                    "status": r[2],
                    "title": r[3],
                    "app_code": r[4],
                    "created_at": r[5].isoformat() if r[5] else None,
                    "sla_due_at": r[6].isoformat() if r[6] else None,
                }
            )

        return items