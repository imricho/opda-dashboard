-- INCIDENTS (tickets/incidents)
CREATE TABLE IF NOT EXISTS incidents (
  id            BIGSERIAL PRIMARY KEY,
  severity      TEXT NOT NULL CHECK (severity IN ('P1','P2','P3','P4')),
  status        TEXT NOT NULL CHECK (status IN ('OPEN','ACK','MITIGATED','RESOLVED','CLOSED')),
  title         TEXT NOT NULL,
  app_code      TEXT NOT NULL,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
  resolved_at   TIMESTAMPTZ NULL,
  sla_due_at    TIMESTAMPTZ NULL
);

-- APPLICATION HEALTH / INVENTORY (very minimal)
CREATE TABLE IF NOT EXISTS applications (
  app_code      TEXT PRIMARY KEY,
  app_name      TEXT NOT NULL,
  is_critical   BOOLEAN NOT NULL DEFAULT false,
  health_status TEXT NOT NULL CHECK (health_status IN ('UP','DEGRADED','DOWN')) DEFAULT 'UP',
  updated_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- CERTIFICATES
CREATE TABLE IF NOT EXISTS certificates (
  id           BIGSERIAL PRIMARY KEY,
  common_name  TEXT NOT NULL,
  system_name  TEXT NOT NULL,
  expires_at   TIMESTAMPTZ NOT NULL
);