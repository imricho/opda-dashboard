from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, Tuple

class NotificationProvider(ABC):
    @abstractmethod
    def send_template(
            self,
            to_e164: str,
            template_name: str,
            language: str,
            variables: Dict[str, str],
    ) -> Tuple[bool, str]:
        """
        Returns: (ok, message_id_or_error)
        """
        raise NotImplementedError