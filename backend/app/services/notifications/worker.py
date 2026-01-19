from __future__ import annotations

import os
import time
from uuid import UUID

from .repo import NotificationRepo
from .provider import get_provider

def backoff_seconds(attempts: int) -> int:
    # 1st retry: 10s, then 30s, 60s, 120s, max 300s
    steps = [10, 30, 60, 120, 300]
    return steps[min(attempts, len(steps)-1)]

def run_loop():
    repo = NotificationRepo()
    provider = get_provider()

    poll_seconds = int(os.getenv("NOTIF_WORKER_POLL_SECONDS", "5"))
    batch_size = int(os.getenv("NOTIF_WORKER_BATCH_SIZE", "20"))
    max_attempts = int(os.getenv("NOTIF_WORKER_MAX_ATTEMPTS", "6"))

    print(f"[worker] started provider={os.getenv('NOTIF_PROVIDER','mock')} poll={poll_seconds}s batch={batch_size}")

    while True:
        items = repo.fetch_pending_batch(limit=batch_size)
        if not items:
            time.sleep(poll_seconds)
            continue

        for it in items:
            queue_id = UUID(str(it["id"]))
            attempts = int(it.get("attempts") or 0)

            # Need rule/template fields
            template_name = it.get("template_name") or ""
            language = it.get("language") or "en_US"
            schema = it.get("schema") or []
            to = it.get("wa_phone_e164") or ""

            if not (template_name and to):
                attempts += 1
                dead = attempts >= max_attempts
                repo.mark_failed(queue_id, attempts, backoff_seconds(attempts), "Missing template_name or recipient phone", dead)
                continue

            payload = it.get("payload") or {}
            # IMPORTANT: ordered variables -> schema order
            variables = {k: str(payload.get(k, "")) for k in schema}

            ok, msg = provider.send_template(to, template_name, language, variables)
            if ok:
                repo.mark_sent(queue_id, msg)
            else:
                attempts += 1
                dead = attempts >= max_attempts
                repo.mark_failed(queue_id, attempts, backoff_seconds(attempts), msg, dead)

        # Short pause to avoid hot loop
        time.sleep(1)

if __name__ == "__main__":
    run_loop()