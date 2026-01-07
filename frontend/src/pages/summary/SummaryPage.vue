<template>
  <AppShell>
    <!-- Page header -->
    <div class="page-header d-print-none mt-3">
      <div class="row g-2 align-items-center">
        <div class="col">
          <div class="d-flex align-items-center gap-2">
            <h2 class="page-title mb-0">Operations Summary</h2>

            <span class="badge" :class="opsBadge(summary.ops_status)">
              {{ summary.ops_status }}
            </span>

            <span class="text-secondary">
              Scope: <span class="fw-semibold">{{ summary.scope }}</span>
            </span>
          </div>

          <div class="text-secondary mt-1">
            Last updated:
            <span class="fw-semibold">{{ summary.generated_at }}</span>
            <span class="mx-2">•</span>
            Data source:
            <span class="fw-semibold">{{ summary.data_source }}</span>
          </div>
        </div>

        <div class="col-auto ms-auto d-print-none">
          <div class="btn-list">
            <div class="btn-group">
              <button class="btn" :class="summary.scope === 'today' ? 'btn-primary' : 'btn-outline-primary'"
                      @click="setScope('today')">
                Today
              </button>
              <button class="btn" :class="summary.scope === '24h' ? 'btn-primary' : 'btn-outline-primary'"
                      @click="setScope('24h')">
                24h
              </button>
              <button class="btn" :class="summary.scope === '7d' ? 'btn-primary' : 'btn-outline-primary'"
                      @click="setScope('7d')">
                7d
              </button>
            </div>

            <button class="btn btn-outline-primary" @click="reload" :disabled="loading">
              <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status" />
              Refresh
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Alerts / Attention -->
    <div class="row row-deck row-cards mt-3">
      <div class="col-12">
        <div class="card">
          <div class="card-header">
            <h3 class="card-title mb-0">What needs attention now</h3>
            <div class="card-actions">
              <a class="btn btn-sm btn-outline-primary" href="#" @click.prevent="go('/incidents')">
                View incidents
              </a>
            </div>
          </div>

          <div class="list-group list-group-flush">
            <div
                v-for="(item, idx) in summary.attention_items"
                :key="idx"
                class="list-group-item"
            >
              <div class="row align-items-center">
                <div class="col-auto">
                  <span class="badge" :class="sevBadge(item.severity)">
                    {{ item.severity }}
                  </span>
                </div>

                <div class="col">
                  <div class="fw-semibold">{{ item.title }}</div>
                  <div class="text-secondary">
                    {{ item.subtitle }}
                    <span class="mx-2">•</span>
                    Owner: <span class="fw-semibold">{{ item.owner }}</span>
                  </div>
                  <div class="text-secondary mt-1">
                    Next action: <span class="fw-semibold">{{ item.next_action }}</span>
                  </div>
                </div>

                <div class="col-auto text-end">
                  <div class="text-secondary">Due</div>
                  <div class="fw-semibold">{{ item.due }}</div>
                </div>
              </div>
            </div>

            <div v-if="!summary.attention_items.length" class="list-group-item text-secondary">
              No attention items.
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- KPI Tiles -->
    <div class="row row-deck row-cards mt-3">
      <div class="col-12 col-md-6 col-xl-3">
        <div class="card">
          <div class="card-body">
            <div class="subheader">Availability ({{ summary.scope }})</div>
            <div class="d-flex align-items-baseline gap-2 mt-1">
              <div class="h1 mb-0">{{ summary.kpi.availability_pct }}%</div>
              <span class="text-secondary">Target {{ summary.kpi.availability_target_pct }}%</span>
            </div>
            <div class="text-secondary mt-2">
              Degraded minutes: <span class="fw-semibold">{{ summary.kpi.degraded_minutes }}</span>
            </div>
          </div>
        </div>
      </div>

      <div class="col-12 col-md-6 col-xl-3">
        <div class="card">
          <div class="card-body">
            <div class="subheader">Open Incidents</div>
            <div class="mt-1 d-flex gap-2 flex-wrap">
              <span class="badge bg-red-lt">P1: {{ summary.kpi.open_incidents.p1 }}</span>
              <span class="badge bg-yellow-lt">P2: {{ summary.kpi.open_incidents.p2 }}</span>
              <span class="badge bg-azure-lt">P3+: {{ summary.kpi.open_incidents.p3 }}</span>
            </div>
            <div class="text-secondary mt-2">
              MTTR (7d): <span class="fw-semibold">{{ summary.kpi.mttr_minutes_7d }}m</span>
              <span class="ms-2 badge" :class="trendBadge(summary.kpi.mttr_trend)">
                {{ summary.kpi.mttr_trend }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <div class="col-12 col-md-6 col-xl-3">
        <div class="card">
          <div class="card-body">
            <div class="subheader">Work Execution</div>
            <div class="h1 mt-1 mb-0">{{ summary.kpi.work.backlog }}</div>
            <div class="text-secondary">Backlog</div>

            <div class="mt-2 d-flex flex-wrap gap-2">
              <span class="badge bg-orange-lt">Overdue: {{ summary.kpi.work.overdue }}</span>
              <span class="badge bg-yellow-lt">SLA at risk: {{ summary.kpi.work.sla_at_risk }}</span>
            </div>
          </div>
        </div>
      </div>

      <div class="col-12 col-md-6 col-xl-3">
        <div class="card">
          <div class="card-body">
            <div class="subheader">Risk & Compliance</div>
            <div class="h1 mt-1 mb-0">{{ summary.kpi.risk.high_risk_items }}</div>
            <div class="text-secondary">High risk items</div>

            <div class="mt-2 d-flex flex-wrap gap-2">
              <span class="badge bg-azure-lt">Contracts due: {{ summary.kpi.risk.contracts_due }}</span>
              <span class="badge bg-orange-lt">Certs &lt;30d: {{ summary.kpi.risk.certs_expiring_30d }}</span>
              <span class="badge bg-yellow-lt">Access overdue: {{ summary.kpi.risk.access_review_overdue }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 3-column: Incidents / Deadlines / People -->
    <div class="row row-deck row-cards mt-3">
      <!-- Incidents snapshot -->
      <div class="col-12 col-xl-4">
        <div class="card h-100">
          <div class="card-header">
            <h3 class="card-title mb-0">Live incidents</h3>
            <div class="card-actions">
              <a class="btn btn-sm btn-outline-primary" href="#" @click.prevent="go('/incidents')">
                Open
              </a>
            </div>
          </div>

          <div class="table-responsive">
            <table class="table table-vcenter card-table">
              <thead>
              <tr>
                <th>Sev</th>
                <th>Service</th>
                <th>Status</th>
                <th class="text-end">Age</th>
              </tr>
              </thead>
              <tbody>
              <tr v-for="(inc, idx) in summary.incidents_top" :key="idx">
                <td>
                  <span class="badge" :class="sevBadge(inc.severity)">{{ inc.severity }}</span>
                </td>
                <td>
                  <div class="fw-semibold">{{ inc.service }}</div>
                  <div class="text-secondary small">{{ inc.title }}</div>
                </td>
                <td>
                  <span class="badge" :class="statusBadge(inc.status)">{{ inc.status }}</span>
                </td>
                <td class="text-end text-secondary">{{ inc.age }}</td>
              </tr>

              <tr v-if="!summary.incidents_top.length">
                <td colspan="4" class="text-secondary">No open incidents.</td>
              </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Deadlines -->
      <div class="col-12 col-xl-4">
        <div class="card h-100">
          <div class="card-header">
            <h3 class="card-title mb-0">Upcoming deadlines</h3>
          </div>

          <div class="card-body">
            <ul class="nav nav-pills mb-3">
              <li class="nav-item">
                <a class="nav-link" href="#" :class="{ active: deadlineTab === 'contracts' }"
                   @click.prevent="deadlineTab='contracts'">Contracts</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="#" :class="{ active: deadlineTab === 'certs' }"
                   @click.prevent="deadlineTab='certs'">Certificates</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="#" :class="{ active: deadlineTab === 'drp' }"
                   @click.prevent="deadlineTab='drp'">DRP</a>
              </li>
            </ul>

            <div v-if="deadlineTab==='contracts'">
              <div v-for="(c, idx) in summary.deadlines.contracts" :key="idx" class="mb-3">
                <div class="fw-semibold">{{ c.vendor }} — {{ c.system }}</div>
                <div class="text-secondary">
                  Exp: <span class="fw-semibold">{{ c.expires }}</span>
                  <span class="mx-2">•</span>
                  Start renewal: <span class="fw-semibold">{{ c.renewal_start }}</span>
                </div>
                <div class="text-secondary">
                  Payment window: <span class="fw-semibold">{{ c.payment_window }}</span>
                </div>
              </div>
              <div v-if="!summary.deadlines.contracts.length" class="text-secondary">No upcoming contract deadlines.</div>
            </div>

            <div v-else-if="deadlineTab==='certs'">
              <div v-for="(c, idx) in summary.deadlines.certs" :key="idx" class="mb-3">
                <div class="fw-semibold">{{ c.system }}</div>
                <div class="text-secondary">
                  Expires: <span class="fw-semibold">{{ c.expires }}</span>
                  <span class="mx-2">•</span>
                  Renew plan: <span class="fw-semibold">{{ c.renew_plan }}</span>
                </div>
              </div>
              <div v-if="!summary.deadlines.certs.length" class="text-secondary">No certificates expiring soon.</div>
            </div>

            <div v-else>
              <div v-for="(d, idx) in summary.deadlines.drp" :key="idx" class="mb-3">
                <div class="fw-semibold">{{ d.system }}</div>
                <div class="text-secondary">
                  Next DRP: <span class="fw-semibold">{{ d.date }}</span>
                  <span class="mx-2">•</span>
                  Owner: <span class="fw-semibold">{{ d.owner }}</span>
                </div>
              </div>
              <div v-if="!summary.deadlines.drp.length" class="text-secondary">No DRP schedule entries.</div>
            </div>
          </div>
        </div>
      </div>

      <!-- People -->
      <div class="col-12 col-xl-4">
        <div class="card h-100">
          <div class="card-header">
            <h3 class="card-title mb-0">People readiness</h3>
          </div>

          <div class="card-body">
            <div class="mb-3">
              <div class="text-secondary mb-1">Absent today</div>
              <div class="d-flex flex-wrap gap-2">
                <span v-for="(p, idx) in summary.people.absent_today" :key="idx" class="badge bg-azure-lt">
                  {{ p }}
                </span>
                <span v-if="!summary.people.absent_today.length" class="text-secondary">None</span>
              </div>
            </div>

            <div class="mb-3">
              <div class="text-secondary mb-1">Absent this week</div>
              <div class="d-flex flex-wrap gap-2">
                <span v-for="(p, idx) in summary.people.absent_week" :key="idx" class="badge bg-azure-lt">
                  {{ p }}
                </span>
                <span v-if="!summary.people.absent_week.length" class="text-secondary">None</span>
              </div>
            </div>

            <div>
              <div class="text-secondary mb-1">Birthdays this week</div>
              <div class="d-flex flex-wrap gap-2">
                <span v-for="(p, idx) in summary.people.birthdays_week" :key="idx" class="badge bg-green-lt">
                  {{ p }}
                </span>
                <span v-if="!summary.people.birthdays_week.length" class="text-secondary">None</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Trends (optional placeholders) -->
    <div class="row row-deck row-cards mt-3 mb-4">
      <div class="col-12 col-xl-6">
        <div class="card">
          <div class="card-header">
            <h3 class="card-title mb-0">Trends (last 7 days)</h3>
          </div>
          <div class="card-body">
            <div class="text-secondary">
              Availability trend and incident volume chart can be placed here later.
            </div>
            <div class="mt-3 d-flex flex-wrap gap-2">
              <span class="badge bg-green-lt">MTTR: 42m → 35m</span>
              <span class="badge bg-azure-lt">Backlog: 52 → 48</span>
              <span class="badge bg-yellow-lt">P1 count: 0 → 1</span>
            </div>
          </div>
        </div>
      </div>

      <div class="col-12 col-xl-6">
        <div class="card">
          <div class="card-header">
            <h3 class="card-title mb-0">Notes</h3>
          </div>
          <div class="card-body">
            <ul class="mb-0">
              <li>Use this area for executive notes / key decisions / announcements.</li>
              <li>Later we can load it from an API (e.g. /api/summary/notes).</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </AppShell>
</template>

<script setup lang="ts">
import { ref } from "vue";
import AppShell from "@/layouts/AppShell.vue";

// UI state
const loading = ref(false);
const deadlineTab = ref<"contracts" | "certs" | "drp">("contracts");

// Mock data (works immediately). Later replace reload() with API call.
const summary = ref({
  ops_status: "DEGRADED", // NORMAL | DEGRADED | MAJOR_INCIDENT
  scope: "24h", // today | 24h | 7d
  generated_at: "2026-01-07T10:15:00+07:00",
  data_source: "mock",

  attention_items: [
    {
      severity: "P1",
      title: "RTGS service degraded",
      subtitle: "Latency increased on core path",
      owner: "KODIT",
      next_action: "Confirm DB saturation & apply mitigation",
      due: "Today 14:00",
    },
    {
      severity: "HIGH",
      title: "Certificate expiring soon",
      subtitle: "BI-FAST API gateway cert < 30 days",
      owner: "OpDA",
      next_action: "Raise renewal request to CA + schedule change window",
      due: "Jan 15",
    },
    {
      severity: "P2",
      title: "Workorder overdue",
      subtitle: "Recurring issue escalation to dev team",
      owner: "DLDS",
      next_action: "Finalize RCA & push permanent fix timeline",
      due: "Jan 10",
    },
  ],

  kpi: {
    availability_pct: 99.93,
    availability_target_pct: 99.9,
    degraded_minutes: 12,

    open_incidents: { p1: 1, p2: 2, p3: 4 },
    mttr_minutes_7d: 35,
    mttr_trend: "improving", // improving | worsening | flat

    work: { backlog: 48, overdue: 6, sla_at_risk: 2 },

    risk: { high_risk_items: 5, contracts_due: 2, certs_expiring_30d: 1, access_review_overdue: 2 },
  },

  incidents_top: [
    { severity: "P1", service: "RTGS", title: "High latency", status: "OPEN", age: "2h 13m" },
    { severity: "P2", service: "BI-FAST", title: "Intermittent timeout", status: "MITIGATING", age: "5h 01m" },
    { severity: "P2", service: "CBS", title: "Batch delay", status: "OPEN", age: "9h 40m" },
  ],

  deadlines: {
    contracts: [
      { vendor: "PT MII", system: "RTGS Ops Support", expires: "2026-03-31", renewal_start: "2026-02-01", payment_window: "Feb 10–Feb 25" },
      { vendor: "PCI", system: "BI-FAST Support", expires: "2026-04-30", renewal_start: "2026-03-01", payment_window: "Mar 10–Mar 20" },
    ],
    certs: [
      { system: "BI-FAST API Gateway", expires: "2026-01-28", renew_plan: "2026-01-15 change window" },
      { system: "RTGS SSO", expires: "2026-02-10", renew_plan: "2026-01-30 change window" },
    ],
    drp: [
      { system: "RTGS", date: "2026-02-20", owner: "OpDA" },
      { system: "BI-FAST", date: "2026-03-05", owner: "OpDA" },
    ],
  },

  people: {
    absent_today: ["Raka (AM)", "Dini (PM)"],
    absent_week: ["Wawan (Thu–Fri)"],
    birthdays_week: ["Teresa (Fri)", "Budi (Sat)"],
  },
});

function opsBadge(status: string) {
  if (status === "NORMAL") return "bg-green-lt";
  if (status === "DEGRADED") return "bg-yellow-lt";
  if (status === "MAJOR_INCIDENT") return "bg-red-lt";
  return "bg-secondary-lt";
}

function sevBadge(sev: string) {
  if (sev === "P1") return "bg-red-lt";
  if (sev === "P2") return "bg-yellow-lt";
  if (sev === "P3") return "bg-azure-lt";
  if (sev === "HIGH") return "bg-orange-lt";
  if (sev === "MED") return "bg-azure-lt";
  return "bg-secondary-lt";
}

function statusBadge(status: string) {
  if (status === "OPEN") return "bg-red-lt";
  if (status === "MITIGATING") return "bg-yellow-lt";
  if (status === "RESOLVED") return "bg-green-lt";
  return "bg-secondary-lt";
}

function trendBadge(trend: string) {
  if (trend === "improving") return "bg-green-lt";
  if (trend === "worsening") return "bg-red-lt";
  return "bg-secondary-lt";
}

function setScope(scope: "today" | "24h" | "7d") {
  summary.value.scope = scope;
  reload();
}

function go(path: string) {
  // Simple approach: rely on normal links or use router later
  window.location.href = path;
}

async function reload() {
  loading.value = true;
  try {
    // Later: call /api/dashboard/summary?scope=...
    // For now we just simulate refresh timestamp.
    summary.value.generated_at = new Date().toISOString();
    summary.value.data_source = "mock";
  } finally {
    loading.value = false;
  }
}
</script>