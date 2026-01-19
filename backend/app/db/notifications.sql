create extension if not exists pgcrypto;

-- Recipients (who receives alerts)
create table if not exists notification_recipients (
                                                       id uuid primary key default gen_random_uuid(),
    display_name text not null,
    wa_phone_e164 text, -- +62812xxxx
    enabled boolean not null default true,
    labels text[] not null default '{}', -- ["OPDA_MANAGER","ONCALL"]
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
    );

create index if not exists idx_notif_recipients_enabled on notification_recipients(enabled);
create index if not exists idx_notif_recipients_labels on notification_recipients using gin(labels);

-- Templates (mapping to WhatsApp template names)
create table if not exists notification_templates (
                                                      id uuid primary key default gen_random_uuid(),
    provider text not null, -- WHATSAPP
    template_name text not null,
    language text not null default 'en_US',
    category text not null default 'UTILITY',
    schema jsonb not null default '[]'::jsonb, -- e.g. ["system","severity","title","status","link"]
    enabled boolean not null default true,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    unique(provider, template_name, language)
    );

create index if not exists idx_notif_templates_enabled on notification_templates(enabled);

-- Rules (when to notify + recipients + which template)
create table if not exists notification_rules (
                                                  id uuid primary key default gen_random_uuid(),
    feature text not null,        -- "incidents", "certificates"
    event_type text not null,     -- "incident.created"
    condition jsonb not null default '{}'::jsonb,
    recipient_selector jsonb not null default '{}'::jsonb, -- {"labels":["OPDA_MANAGER","ONCALL"]}
    template_id uuid not null references notification_templates(id),
    throttle_seconds int not null default 60,
    enabled boolean not null default true,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
    );

create index if not exists idx_notif_rules_enabled on notification_rules(enabled);
create index if not exists idx_notif_rules_event on notification_rules(event_type);

-- Events (audit incoming events)
create table if not exists notification_events (
                                                   id uuid primary key default gen_random_uuid(),
    event_type text not null,
    event_data jsonb not null,
    created_at timestamptz not null default now()
    );

create index if not exists idx_notif_events_type on notification_events(event_type);

-- Outbox Queue (messages to send)
create table if not exists notification_queue (
                                                  id uuid primary key default gen_random_uuid(),
    rule_id uuid references notification_rules(id),
    recipient_id uuid not null references notification_recipients(id),
    channel text not null default 'WHATSAPP',
    payload jsonb not null, -- rendered variables { "system": "...", "link": "...", ... }
    status text not null default 'PENDING', -- PENDING|SENT|DELIVERED|FAILED|DEAD
    attempts int not null default 0,
    next_retry_at timestamptz not null default now(),
    provider_message_id text,
    last_error text,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
    );

create index if not exists idx_notif_queue_status on notification_queue(status);
create index if not exists idx_notif_queue_retry on notification_queue(next_retry_at);

-- Simple dedupe helper: prevent same payload sending too often to same recipient
-- (Optional; leave commented if you don't want constraints)
-- create unique index if not exists uq_notif_queue_dedupe
-- on notification_queue(recipient_id, channel, (payload::text))
-- where status in ('PENDING','SENT');

insert into notification_recipients(display_name, wa_phone_e164, labels)
values ('Coco', '+6281234567890', array['OPDA_MANAGER','ONCALL']);

insert into notification_templates(provider, template_name, language, schema)
values ('WHATSAPP', 'opda_incident_alert', 'en_US', '["system","severity","title","status","link"]'::jsonb);

insert into notification_rules(feature, event_type, condition, recipient_selector, template_id, throttle_seconds)
select
    'incidents',
    'incident.created',
    '{"severity_in":["P1","P2"]}'::jsonb,
    '{"labels":["OPDA_MANAGER"]}'::jsonb,
    t.id,
    60
from notification_templates t
where t.template_name='opda_incident_alert';