from typing import Protocol, Dict, Any, List, Optional

class IncidentsRepository(Protocol):
    def list_incidents(
            self,
            status: Optional[str],
            severity: Optional[str],
            app_code: Optional[str],
            limit: int,
            offset: int,
    ) -> List[Dict[str, Any]]:
        ...