from __future__ import annotations

import os
from typing import Any, Dict, List, Optional
from uuid import UUID

import psycopg
from psycopg.rows import dict_row

def get_conn():
    return psycopg.connect(os.environ["DATABASE_URL"], row_factory=dict_row)

class NotificationRepo:
    def insert_event(self, event_type: str, event_data: Dict[str, Any]) -> None:
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute(
                "insert into notification_events(event_type, event_data) values (%s, %s::jsonb)",
                (event_type, psycopg.types.json.Jsonb(event_data)),
            )

    def list_enabled_rules_for_event(self, event_type: str) -> List[dict]:
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute(
                """
                select r.*, t.provider, t.template_name, t.language, t.schema
                from notification_rules r
                         join notification_templates t on t.id = r.template_id
                where r.enabled = true and t.enabled = true and r.event_type = %s
                """,
                (event_type,),
            )
            return cur.fetchall()

    def select_recipients(self, selector: Dict[str, Any]) -> List[dict]:
        """
        selector example:
          {"labels":["OPDA_MANAGER","ONCALL"]}
        """
        labels = selector.get("labels") or []
        with get_conn() as conn, conn.cursor() as cur:
            if labels:
                cur.execute(
                    """
                    select *
                    from notification_recipients
                    where enabled = true and labels && %s::text[]
                    """,
                    (labels,),
                )
            else:
                cur.execute(
                    "select * from notification_recipients where enabled = true"
                )
            return cur.fetchall()

    def enqueue_message(
            self,
            rule_id: Optional[UUID],
            recipient_id: UUID,
            channel: str,
            payload: Dict[str, Any],
    ) -> None:
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute(
                """
                insert into notification_queue(rule_id, recipient_id, channel, payload)
                values (%s, %s, %s, %s::jsonb)
                """,
                (rule_id, recipient_id, channel, psycopg.types.json.Jsonb(payload)),
            )

    def fetch_pending_batch(self, limit: int = 20) -> List[dict]:
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute(
                """
                select q.*, r.feature, r.event_type, r.throttle_seconds,
                       t.provider, t.template_name, t.language, t.schema,
                       rc.wa_phone_e164, rc.display_name
                from notification_queue q
                         left join notification_rules r on r.id = q.rule_id
                         left join notification_templates t on t.id = r.template_id
                         join notification_recipients rc on rc.id = q.recipient_id
                where q.status in ('PENDING','FAILED')
                  and q.next_retry_at <= now()
                order by q.created_at asc
                    limit %s
                """,
                (limit,),
            )
            return cur.fetchall()

    def mark_sent(self, queue_id: UUID, provider_message_id: str) -> None:
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute(
                """
                update notification_queue
                set status='SENT', provider_message_id=%s, last_error=null,
                    updated_at=now()
                where id=%s
                """,
                (provider_message_id, queue_id),
            )

    def mark_failed(self, queue_id: UUID, attempts: int, next_retry_seconds: int, error: str, dead: bool) -> None:
        status = "DEAD" if dead else "FAILED"
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute(
                """
                update notification_queue
                set status=%s,
                    attempts=%s,
                    next_retry_at=now() + (%s || ' seconds')::interval,
                    last_error=%s,
                    updated_at=now()
                where id=%s
                """,
                (status, attempts, next_retry_seconds, error[:1000], queue_id),
            )