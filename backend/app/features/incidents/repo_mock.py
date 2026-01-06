from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional

class IncidentsMockRepository:
    def list_incidents(
            self,
            status: Optional[str],
            severity: Optional[str],
            app_code: Optional[str],
            limit: int,
            offset: int,
    ) -> List[Dict[str, Any]]:
        now = datetime.now(timezone.utc)

        sample = [
            {
                "id": 101,
                "severity": "P1",
                "status": "OPEN",
                "title": "Payment processing delayed",
                "app_code": "RTGS",
                "created_at": (now - timedelta(minutes=45)).isoformat(),
                "sla_due_date": (now + timedelta(minutes=75)).isoformat()
            },
            {
                "id": 102,
                "severity": "P2",
                "status": "OPEN",
                "title": "Intermittent timeout",
                "app_code": "BI-FAST",
                "created_at": (now - timedelta(hours=6)).isoformat(),
                "sla_due_date": (now + timedelta(minutes=10)).isoformat()
            },
            {
                "id": 103,
                "severity": "P3",
                "status": "ACK",
                "title": "Monitoring alert noise",
                "app_code": "CBS",
                "created_at": (now - timedelta(days=1, minutes=10)).isoformat(),
                "sla_due_date": (now + timedelta(hours=10)).isoformat()
            }
        ]

        def ok(x: Dict[str, Any]) -> bool:
            if status and x["status"] != status:
                return False
            if severity and x["severity"] != severity:
                return False
            if app_code and x["app_code"] != app_code:
                return False
            return True

        filtered = [x for x in sample if ok(x)]
        return filtered[offset:offset + limit]