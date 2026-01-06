from datetime import datetime, timezone, timedelta
from typing import Dict, Any
from app.shared.db import get_conn

class DashboardDbRepository:
    def get_summary_tiles(self) -> Dict[str, Any]:
        now = datetime.now(timezone.utc)
        day_ago = now - timedelta(days=1)
        in_30d = now + timedelta(days=30)

        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM incidents WHERE status IN ('OPEN','ACK','MITIGATED');")
                open_incidents = cur.fetchone()[0]

                cur.execute("SELECT COUNT(*) FROM incidents WHERE status IN ('OPEN','ACK','MITIGATED') AND severity='P1';")
                p1_open = cur.fetchone()[0]

                cur.execute("""
                    SELECT COUNT(*)
                    FROM incidents
                    WHERE status IN ('OPEN','ACK','MITIGATED')
                      AND sla_due_at IS NOT NULL
                      AND sla_due_at < %s
                      AND created_at >= %s;
                """, (now, day_ago))
                sla_breaches_24h = cur.fetchone()[0]

                cur.execute("SELECT COUNT(*) FROM applications WHERE health_status='DOWN';")
                apps_down = cur.fetchone()[0]

                cur.execute("SELECT COUNT(*) FROM applications WHERE health_status='DEGRADED';")
                apps_degraded = cur.fetchone()[0]

                cur.execute("SELECT COUNT(*) FROM certificates WHERE expires_at <= %s;", (in_30d,))
                certs_expiring_30d = cur.fetchone()[0]

        return {
            "open_incidents": open_incidents,
            "p1_open": p1_open,
            "sla_breaches_24h": sla_breaches_24h,
            "apps_down": apps_down,
            "apps_degraded": apps_degraded,
            "certs_expiring_30d": certs_expiring_30d,
        }