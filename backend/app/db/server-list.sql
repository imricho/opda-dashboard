create extension if not exists pgcrypto;

create table if not exists servers (
                                       id uuid primary key default gen_random_uuid(),
    hostname text not null unique,
    environment text not null,       -- PROD | UAT | DEV
    app_name text,                   -- BI-FAST / RTGS / etc
    ip_address inet,
    os text,
    location text,                   -- DC1 / DC2 / Cloud / etc
    owner_team text,                 -- OpDA / Infra / Vendor
    criticality text not null default 'MED', -- HIGH | MED | LOW
    status text not null default 'UP',       -- UP | DEGRADED | DOWN | MAINT
    tags text[] default '{}',
    notes text,

    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
    );

create index if not exists idx_servers_env on servers(environment);
create index if not exists idx_servers_status on servers(status);
create index if not exists idx_servers_app on servers(app_name);