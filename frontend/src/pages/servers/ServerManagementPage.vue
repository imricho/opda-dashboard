<template>
  <div class="page-header d-print-none mb-3">
    <div class="container-xl">
      <div class="row g-2 align-items-center">
        <div class="col">
          <h2 class="page-title">Servers</h2>
          <div class="text-secondary">Server inventory handled by OpDA (sortable, filterable).</div>
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
              <h3 class="card-title">Server list</h3>
              <div class="card-actions d-flex gap-2">
                <input v-model="q" class="form-control form-control-sm" placeholder="Search hostname/app/location..." style="width: 260px" />
                <select v-model="environment" class="form-select form-select-sm">
                  <option value="">Env: All</option>
                  <option>PROD</option><option>UAT</option><option>DEV</option>
                </select>
                <select v-model="status" class="form-select form-select-sm">
                  <option value="">Status: All</option>
                  <option>UP</option><option>DEGRADED</option><option>DOWN</option><option>MAINT</option>
                </select>
                <button class="btn btn-sm btn-outline-primary" @click="reload">Refresh</button>
              </div>
            </div>

            <div class="card-body">
              <div ref="tableEl"></div>
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

function buildUrl() {
  const params = new URLSearchParams();
  if (q.value) params.set("q", q.value);
  if (environment.value) params.set("environment", environment.value);
  if (status.value) params.set("status", status.value);
  return `/api/servers?${params.toString()}`;
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
    placeholder: "No servers found",
    columns: [
      { title: "Hostname", field: "hostname", sorter: "string", headerFilter: true },
      { title: "Env", field: "environment", sorter: "string", headerFilter: true, width: 90 },
      { title: "App", field: "app_name", sorter: "string", headerFilter: true },
      { title: "IP", field: "ip_address", sorter: "string", headerFilter: true, width: 140 },
      { title: "Status", field: "status", sorter: "string", headerFilter: true, width: 110 },
      { title: "Criticality", field: "criticality", sorter: "string", headerFilter: true, width: 120 },
      { title: "Location", field: "location", sorter: "string", headerFilter: true },
      { title: "Owner", field: "owner_team", sorter: "string", headerFilter: true },
    ],
  });
});

onBeforeUnmount(() => {
  table?.destroy?.();
  table = null;
});

watch([q, environment, status], () => {
  // debounce-lite: you can add a real debounce later
  reload();
});
</script>