from __future__ import annotations

from typing import Any, Dict

from .repo import NotificationRepo

def _match_condition(condition: Dict[str, Any], data: Dict[str, Any]) -> bool:
    """
    Minimal condition engine:
      - {"severity_in":["P1","P2"]} checks data["severity"]
      - {"system_in":["RTGS"]} checks data["system"]
    Extend later as needed.
    """
    if not condition:
        return True

    for key, val in condition.items():
        if key.endswith("_in") and isinstance(val, list):
            field = key[:-3]
            if data.get(field) not in val:
                return False
        else:
            if data.get(key) != val:
                return False
    return True

def _render_payload(schema: list[str], data: Dict[str, Any]) -> Dict[str, Any]:
    # Ensure required vars exist; fill missing with empty string
    out = {}
    for k in schema or []:
        out[k] = data.get(k, "")
    # Keep link if present even if not in schema
    if "link" in data and "link" not in out:
        out["link"] = data["link"]
    return out

class NotificationService:
    def __init__(self, repo: NotificationRepo):
        self.repo = repo

    def ingest_event(self, event_type: str, data: Dict[str, Any]) -> dict:
        self.repo.insert_event(event_type, data)

        rules = self.repo.list_enabled_rules_for_event(event_type)
        queued = 0

        for r in rules:
            condition = r.get("condition") or {}
            if not _match_condition(condition, data):
                continue

            selector = r.get("recipient_selector") or {}
            recipients = self.repo.select_recipients(selector)

            schema = r.get("schema") or []
            payload = _render_payload(schema, data)

            for rc in recipients:
                # Only WhatsApp for now
                if not rc.get("wa_phone_e164"):
                    continue
                self.repo.enqueue_message(
                    rule_id=r["id"],
                    recipient_id=rc["id"],
                    channel="WHATSAPP",
                    payload=payload,
                )
                queued += 1

        return {"event_type": event_type, "queued": queued}