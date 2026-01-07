<template>
  <div class="page">
    <!-- Top bar -->
    <header class="navbar navbar-expand-md d-print-none">
      <div class="container-xl">
        <div class="navbar-brand fw-bold">OPDA Operations Summary</div>

        <div class="navbar-nav flex-row order-md-last gap-2">
          <span class="text-secondary align-self-center">
            Last updated: <span class="fw-semibold">{{ summary?.generated_at ?? "-" }}</span>
          </span>
          <button class="btn btn-outline-primary" @click="load" :disabled="loading">
            <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
            Refresh
          </button>
        </div>
      </div>
    </header>

    <div class="page-wrapper">
      <div class="container-xl mt-3">

        <!-- Error -->
        <div v-if="error" class="alert alert-danger" role="alert">
          <div class="fw-semibold">Failed to load summary</div>
          <div class="mt-1 small">{{ error }}</div>
        </div>

        <!-- Hero row -->
        <div class="row row-deck row-cards">
          <div class="col-12 col-lg-4">
            <div class="card">
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-center">
                  <div class="card-title mb-0">Overall Ops Status</div>
                  <span class="badge" :class="opsBadge(summary?.ops_status)">
                    {{ summary?.ops_status ?? "UNKNOWN" }}
                  </span>
                </div>
                <div class="mt-3 text-secondary">Highlights</div>
                <ul class="mb-0">
                  <li v-for="(h, idx) in (summary?.highlights ?? [])" :key="idx">{{ h }}</li>
                  <li v-if="!(summary?.highlights?.length)" class="text-muted">-</li>
                </ul>
              </div>
            </div>
          </div>

          <div class="col-12 col-lg-4">
            <div class="card">
              <div class="card-body">
                <div class="card-title mb-0">Risk & Compliance</div>
                <div class="mt-3 display-6">
                  {{ summary?.risk?.high_risk_items ?? 0 }}
                  <span class="text-secondary fs-5">items</span>
                </div>
                <div class="mt-3 d-flex flex-wrap gap-2">
                  <span class="badge bg-azure-lt">Contracts due: {{ summary?.risk?.contracts_due ?? 0 }}</span>
                  <span class="badge bg-orange-lt">Certs <30d: {{ summary?.risk?.certs_expiring_30d ?? 0 }}</span>
                  <span class="badge bg-teal-lt">Access overdue: {{ summary?.risk?.access_review_overdue ?? 0 }}</span>
                </div>
              </div>
            </div>
          </div>

          <div class="col-12 col-lg-4">
            <div class="card">
              <div class="card-body">
                <div class="card-title mb-0">Execution Health</div>
                <div class="mt-3">
                  <div class="d-flex justify-content-between">
                    <span class="text-secondary">Ticket backlog</span>
                    <span class="fw-semibold">{{ summary?.execution?.ticket_backlog ?? 0 }}</span>
                  </div>
                  <div class="d-flex justify-content-between">
                    <span class="text-secondary">Overdue workorders</span>
                    <span class="fw-semibold">{{ summary?.execution?.overdue_workorders ?? 0 }}</span>
                  </div>
                  <div class="d-flex justify-content-between">
                    <span class="text-secondary">SLA at risk</span>
                    <span class="fw-semibold">{{ summary?.execution?.sla_at_risk ?? 0 }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div><!-- /hero row -->

        <!-- Attention -->
        <div class="row row-deck row-cards mt-3">
          <div class="col-12">
            <div class="card">
              <div class="card-header">
                <h3 class="card-title mb-0">What needs attention</h3>
              </div>
              <div class="list-group list-group-flush">
                <div v-for="(i, idx) in (summary?.attention_items ?? [])" :key="idx" class="list-group-item">
                  <div class="d-flex justify-content-between">
                    <div>
                      <span class="badge me-2" :class="sevBadge(i.severity)">{{ i.label }}</span>
                      <span class="fw-semibold">{{ i.title }}</span>
                      <span class="text-secondary">— {{ i.subtitle }}</span>
                    </div>
                    <div class="text-secondary">Owner: <span class="fw-semibold">{{ i.owner }}</span></div>
                  </div>
                  <div class="text-secondary mt-1">
                    Next action: <span class="fw-semibold">{{ i.next_action }}</span>
                  </div>
                </div>

                <div v-if="!(summary?.attention_items?.length)" class="list-group-item text-muted">
                  No attention items.
                </div>
              </div>
            </div>
          </div>
        </div>

      </div><!-- /container -->
    </div><!-- /page-wrapper -->
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { apiGet } from "@/services/api";

type Summary = any; // we’ll type this later with the backend schema

const summary = ref<Summary | null>(null);
const loading = ref(false);
const error = ref<string | null>(null);

// Dev token strategy (simple):
// - For now, you can paste token to localStorage: opda_access_token
function getToken(): string | null {
  return localStorage.getItem("opda_access_token");
}

function opsBadge(status?: string) {
  if (status === "NORMAL") return "bg-green-lt";
  if (status === "DEGRADED") return "bg-yellow-lt";
  if (status === "MAJOR_INCIDENT") return "bg-red-lt";
  return "bg-secondary-lt";
}

function sevBadge(sev?: string) {
  if (sev === "P1") return "bg-red-lt";
  if (sev === "P2") return "bg-yellow-lt";
  return "bg-azure-lt";
}

async function load() {
  loading.value = true;
  error.value = null;
  try {
    const token = getToken(); // optional, but your backend likely needs it
    summary.value = await apiGet<Summary>("/api/dashboard/summary", token ?? undefined);
  } catch (e: any) {
    error.value = e?.message ?? String(e);
  } finally {
    loading.value = false;
  }
}

onMounted(load);
</script>