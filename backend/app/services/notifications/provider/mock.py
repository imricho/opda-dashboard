from __future__ import annotations

from typing import Dict, Tuple
from .base import NotificationProvider

class MockProvider(NotificationProvider):
    def send_template(self, to_e164: str, template_name: str, language: str, variables: Dict[str, str]) -> Tuple[bool, str]:
        # In mock mode: "pretend" success and return fake id
        return True, f"mock:{template_name}:{to_e164}"