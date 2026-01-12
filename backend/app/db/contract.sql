create table if not exists contracts (
                                         id uuid primary key default gen_random_uuid(),
    vendor_name text not null,
    contract_name text not null,
    start_date date,
    expiry_date date not null,

    -- operational planning fields
    renewal_start_date date,
    payment_window_start date,
    payment_window_end date,

    status text not null default 'ACTIVE', -- ACTIVE | EXPIRED | TERMINATED
    notes text,

    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
    );

-- If gen_random_uuid() fails, enable extension:
create extension if not exists pgcrypto;