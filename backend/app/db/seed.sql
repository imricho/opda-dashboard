INSERT INTO applications (app_code, app_name, is_critical, health_status)
VALUES
  ('BI-FAST','BI-FAST', true, 'UP'),
  ('RTGS','BI-RTGS', true, 'DEGRADED'),
  ('CBS','BI-CBS', true, 'UP'),
  ('SSSS','BI-SSSS', false, 'DOWN')
ON CONFLICT (app_code) DO UPDATE SET
  health_status = EXCLUDED.health_status,
  updated_at = now();

INSERT INTO certificates (common_name, system_name, expires_at)
VALUES
  ('api.opda.internal','OPDA Dashboard API', now() + interval '20 days'),
  ('rtgs.tls.internal','BI-RTGS', now() + interval '55 days'),
  ('cbs.tls.internal','BI-CBS', now() + interval '10 days')
ON CONFLICT DO NOTHING;

INSERT INTO incidents (severity, status, title, app_code, created_at, sla_due_at, resolved_at)
VALUES
  ('P1','OPEN','Payment processing delayed','RTGS', now() - interval '2 hours', now() + interval '2 hours', NULL),
  ('P2','OPEN','Intermittent timeout','BI-FAST', now() - interval '1 day', now() - interval '2 hours', NULL),
  ('P3','RESOLVED','UI bug on dashboard','CBS', now() - interval '3 days', now() - interval '2 days', now() - interval '1 day');