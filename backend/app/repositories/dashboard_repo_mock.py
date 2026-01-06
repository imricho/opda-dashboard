from datetime import datetime
from typing import Dict, Any

class DashboardMockRepository:
    def get_summary_tiles(self) -> Dict[str, Any]:
        # Simple time-based variation (changes slowly)
        m = datetime.utcnow().minute
        return {
            "open_incidents": 6 + (m % 3),
            "p1_open": 1 + (m % 2),
            "sla_breaches_24h": (m % 2),
            "apps_down": 1 if (m % 5 == 0) else 0,
            "apps_degraded": 2 + (m % 2),
            "certs_expiring_30d": 4,
        }