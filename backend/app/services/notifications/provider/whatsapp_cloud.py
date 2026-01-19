from __future__ import annotations

import os
import requests
from typing import Dict, Tuple

from .base import NotificationProvider

class WhatsAppCloudProvider(NotificationProvider):
    def __init__(self):
        self.token = os.environ["WA_TOKEN"]
        self.phone_number_id = os.environ["WA_PHONE_NUMBER_ID"]
        self.base_url = os.getenv("WA_BASE_URL", "https://graph.facebook.com/v21.0")

    def send_template(self, to_e164: str, template_name: str, language: str, variables: Dict[str, str]) -> Tuple[bool, str]:
        url = f"{self.base_url}/{self.phone_number_id}/messages"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

        # Map variables into template components (body parameters in order).
        # IMPORTANT: WhatsApp templates require ordered parameters.
        params = [{"type": "text", "text": str(v)} for v in variables.values()]

        payload = {
            "messaging_product": "whatsapp",
            "to": to_e164.replace("+", ""),
            "type": "template",
            "template": {
                "name": template_name,
                "language": {"code": language},
                "components": [{"type": "body", "parameters": params}],
            },
        }

        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=20)
            if resp.status_code >= 200 and resp.status_code < 300:
                data = resp.json()
                # Typical response: {"messages":[{"id":"..."}]}
                msg_id = (data.get("messages") or [{}])[0].get("id") or "OK"
                return True, msg_id
            return False, f"{resp.status_code} {resp.text}"
        except Exception as e:
            return False, str(e)