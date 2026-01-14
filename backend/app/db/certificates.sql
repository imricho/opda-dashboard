create extension if not exists pgcrypto;

create table if not exists certificates (
                                            id uuid primary key default gen_random_uuid(),

    cert_name text not null,
    system_name text,                 -- BI-FAST / RTGS / etc
    environment text not null,        -- PROD | UAT | DEV
    cert_type text not null,          -- TLS | SIGNING | CLIENT | API | DB | etc

    owner_team text,                  -- OpDA / Infra / Vendor
    vendor text,                      -- Digicert, internal CA, etc

    host text,                        -- hostname or VIP
    ip_address inet,

    serial_number text,
    issuer text,
    subject text,
    thumbprint text,

    start_date date,
    expiry_date date not null,

    renewal_lead_days int not null default 30,  -- notify/plan renewal N days before expiry
    status text not null default 'ACTIVE',      -- ACTIVE | EXPIRED | REPLACED | REVOKED

    notes text,

    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
    );

create index if not exists idx_cert_env on certificates(environment);
create index if not exists idx_cert_expiry on certificates(expiry_date);
create index if not exists idx_cert_system on certificates(system_name);
create index if not exists idx_cert_status on certificates(status);