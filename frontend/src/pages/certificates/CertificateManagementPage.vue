<template>
  <div class="page-header d-print-none mb-3">
    <div class="container-xl">
      <div class="row g-2 align-items-center">
        <div class="col">
          <h2 class="page-title">Certificates</h2>
          <div class="text-secondary">Certificate inventory (sortable, filterable) with expiry monitoring.</div>
        </div>
      </div>
    </div>
  </div>

  <div class="page-body">
    <div class="container-xl">
      <div class="row row-cards">
        <div class="col-12">
          <div class="card">
            <div class="card-header">
              <h3 class="card-title">Certificate list</h3>

              <div class="card-actions d-flex gap-2 flex-wrap">
                <input
                    v-model="q"
                    class="form-control form-control-sm"
                    placeholder="Search name/system/host/issuer..."
                    style="width: 260px"
                />

                <select v-model="environment" class="form-select form-select-sm">
                  <option value="">Env: All</option>
                  <option>PROD</option><option>UAT</option><option>DEV</option>
                </select>

                <select v-model="status" class="form-select form-select-sm">
                  <option value="">Status: All</option>
                  <option>ACTIVE</option><option>EXPIRED</option><option>REPLACED</option><option>REVOKED</option>
                </select>

                <select v-model="expWithin" class="form-select form-select-sm">
                  <option value="">Exp: Any</option>
                  <option value="7">Exp ≤ 7 days</option>
                  <option value="14">Exp ≤ 14 days</option>
                  <option value="30">Exp ≤ 30 days</option>
                  <option value="60">Exp ≤ 60 days</option>
                </select>

                <button class="btn btn-sm btn-outline-primary" @click="reload">Refresh</button>
              </div>
            </div>

            <div class="card-body">
              <div ref="tableEl"></div>
              <div class="text-secondary small mt-3">
                Tip: click “Expiry” column to sort. Use “Exp ≤ 30 days” for quick risk view.
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onBeforeUnmount, ref, watch } from "vue";
import { TabulatorFull as Tabulator } from "tabulator-tables";

const tableEl = ref<HTMLElement | null>(null);
let table: any = null;

const q = ref("");
const environment = ref("");
const status = ref("");
const expWithin = ref(""); // string for select

function buildUrl() {
  const params = new URLSearchParams();
  if (q.value) params.set("q", q.value);
  if (environment.value) params.set("environment", environment.value);
  if (status.value) params.set("status", status.value);
  if (expWithin.value) params.set("exp_within_days", expWithin.value);
  return `/api/certificates?${params.toString()}`;
}

async function reload() {
  if (!table) return;
  table.setData(buildUrl());
}

onMounted(() => {
  table = new Tabulator(tableEl.value!, {
    layout: "fitColumns",
    height: "600px",
    ajaxURL: buildUrl(),
    ajaxConfig: "GET",
    pagination: true,
    paginationSize: 15,
    placeholder: "No certificates found",
    columns: [
      { title: "Name", field: "cert_name", sorter: "string", headerFilter: true, minWidth: 220 },
      { title: "System", field: "system_name", sorter: "string", headerFilter: true, width: 140 },
      { title: "Env", field: "environment", sorter: "string", headerFilter: true, width: 90 },
      { title: "Type", field: "cert_type", sorter: "string", headerFilter: true, width: 110 },
      { title: "Host", field: "host", sorter: "string", headerFilter: true, minWidth: 160 },
      { title: "IP", field: "ip_address", sorter: "string", headerFilter: true, width: 140 },
      { title: "Expiry", field: "expiry_date", sorter: "date", headerFilter: true, width: 130 },
      { title: "Lead(d)", field: "renewal_lead_days", sorter: "number", width: 90 },
      { title: "Status", field: "status", sorter: "string", headerFilter: true, width: 110 },
      { title: "Owner", field: "owner_team", sorter: "string", headerFilter: true, width: 140 },
      { title: "Vendor", field: "vendor", sorter: "string", headerFilter: true, width: 140 },
    ],
  });
});

onBeforeUnmount(() => {
  table?.destroy?.();
  table = null;
});

// auto reload when filters change (simple)
watch([q, environment, status, expWithin], () => reload());
</script>