<template>
  <div class="page-header d-print-none mb-3">
    <div class="container-xl">
      <div class="row g-2 align-items-center">
        <div class="col">
          <h2 class="page-title">Contract Management</h2>
          <div class="text-secondary">
            Track contract expiry, renewal start, payment windows, and related schedules.
          </div>
        </div>
        <div class="col-auto ms-auto d-print-none">
          <div class="btn-list">
            <button class="btn btn-outline-primary" @click="refresh">
              Refresh
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="page-body">
    <div class="container-xl">
      <div class="row row-cards">
        <div class="col-12 col-lg-4">
          <ContractForm @saved="onSaved" />
        </div>
        <!-- Schedule Widget -->
        <div class="col-12 col-lg-8">
          <ScheduleWidget
              ref="scheduleRef"
              title="Contract schedule"
              :types="['contract']"
              :defaultView="'dayGridMonth'"
              apiBase="/api/contracts/schedule"
          />
        </div>

        <!-- Optional: later add a table below -->
        <div class="col-12">
          <div class="card">
            <div class="card-header">
              <h3 class="card-title">Upcoming deadlines (table)</h3>
              <div class="card-actions">
                <span class="text-secondary">Next: we can add Tabulator here</span>
              </div>
            </div>
            <div class="card-body">
              <div class="text-secondary">
                Placeholder. We’ll add table/list view after calendar is stable.
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import ContractForm from "@/pages/contracts/ContractForm.vue";
import ScheduleWidget from "@/components/schedule/ScheduleWidget.vue";

const scheduleRef = ref<any>(null);

function onSaved() {
  // reload calendar events after saving
  scheduleRef.value?.reload?.();
}

function refresh() {
  // ScheduleWidget already has its own refresh logic,
  // but keeping a page-level action is useful later.
  // We’ll expand this when you add table+filters.
}
</script>