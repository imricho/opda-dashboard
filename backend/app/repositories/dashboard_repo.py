from typing import Protocol, Dict, Any

class DashboardRepository(Protocol):
    def get_summary_tiles(self) -> Dict[str, Any]:
        ...