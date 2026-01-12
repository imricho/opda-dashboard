<template>
  <div class="card">
    <div class="card-header">
      <h3 class="card-title">{{ title }}</h3>

      <div class="card-actions d-flex gap-2 align-items-center">
        <!-- Filters -->
        <select class="form-select form-select-sm" v-model="selectedType">
          <option value="all">All</option>
          <option v-for="t in types" :key="t" :value="t">{{ labelType(t) }}</option>
        </select>

        <button class="btn btn-sm btn-outline-primary" @click="loadEvents">
          Refresh
        </button>
      </div>
    </div>

    <div class="card-body">
      <FullCalendar ref="calendarRef" :options="calendarOptions" />
      <div class="text-secondary mt-3 small">
        Tip: use <b>Month</b> for overview and <b>List Week</b> for executive reading mode.
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from "vue";
import FullCalendar from "@fullcalendar/vue3";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import listPlugin from "@fullcalendar/list";
import interactionPlugin from "@fullcalendar/interaction";

type ScheduleType = "contract" | "certificate" | "drp";

const props = defineProps<{
  title: string;
  types: ScheduleType[];
  defaultView: "dayGridMonth" | "timeGridWeek" | "listWeek";
}>();

const emit = defineEmits<{ (e: "refresh"): void }>();

const calendarRef = ref<any>(null);
const selectedType = ref<"all" | ScheduleType>("all");

// ---- Data loading (mock for now, switch to API later) ----
type ScheduleEvent = {
  id: string;
  title: string;
  start: string;          // ISO date
  end?: string;           // ISO date
  type: ScheduleType;
  severity?: "P1" | "P2" | "NORMAL";
};

function mockEvents(): ScheduleEvent[] {
  return [
    {
      id: "c-ptmii-exp",
      title: "Contract exp: PT MII — RTGS Ops Support",
      start: "2026-03-31",
      type: "contract",
    },
    {
      id: "c-ptmii-renew",
      title: "Renewal start: PT MII — RTGS Ops Support",
      start: "2026-02-01",
      type: "contract",
    },
    {
      id: "c-ptmii-pay",
      title: "Payment window: PT MII",
      start: "2026-02-10",
      end: "2026-02-25",
      type: "contract",
    },
    {
      id: "cert-bifast",
      title: "Cert exp: BI-FAST API Gateway (<=30d)",
      start: "2026-01-15",
      type: "certificate",
      severity: "P2",
    },
    {
      id: "drp-q1",
      title: "DRP Simulation — BI-FAST (Q1)",
      start: "2026-02-20",
      type: "drp",
    },
  ];
}

function toFullCalendarEvent(e: ScheduleEvent) {
  return {
    id: e.id,
    title: e.title,
    start: e.start,
    end: e.end,
    allDay: true,
    classNames: [
      `opda-type-${e.type}`,
      e.severity ? `opda-sev-${e.severity}` : "",
    ].filter(Boolean),
    extendedProps: {
      type: e.type,
      severity: e.severity ?? "NORMAL",
    },
  };
}

const events = ref<any[]>([]);

async function loadEvents() {
  // Later: replace this with API call:
  // GET /api/contracts/schedule?type=...
  const raw = mockEvents();

  const filtered =
      selectedType.value === "all"
          ? raw
          : raw.filter((x) => x.type === selectedType.value);

  events.value = filtered.map(toFullCalendarEvent);

  // Refresh calendar view
  const api = calendarRef.value?.getApi?.();
  if (api) {
    api.removeAllEvents();
    events.value.forEach((ev) => api.addEvent(ev));
  }

  emit("refresh");
}

const calendarOptions = computed(() => ({
  plugins: [dayGridPlugin, timeGridPlugin, listPlugin, interactionPlugin],
  initialView: props.defaultView,
  height: "auto",
  headerToolbar: {
    left: "prev,next today",
    center: "title",
    right: "dayGridMonth,timeGridWeek,listWeek",
  },
  events: events.value,
  eventClick: (info: any) => {
    // Later: open a Tabler modal with details
    // For now:
    alert(info.event.title);
  },
}));

watch(selectedType, () => loadEvents());

// initial load
loadEvents();

// ---- helpers ----
function labelType(t: ScheduleType) {
  if (t === "contract") return "Contracts";
  if (t === "certificate") return "Certificates";
  return "DRP";
}
</script>

<style scoped>
/* Simple Tabler-compatible tags via FullCalendar classNames */
:deep(.opda-type-contract) { }
:deep(.opda-type-certificate) { }
:deep(.opda-type-drp) { }

/* Severity accents (don’t worry about exact colors yet; Tabler has CSS variables) */
:deep(.opda-sev-P1) { border-left: 3px solid var(--tblr-danger); }
:deep(.opda-sev-P2) { border-left: 3px solid var(--tblr-warning); }
:deep(.opda-sev-NORMAL) { border-left: 3px solid var(--tblr-primary); }

/* Make events look like “tags” */
:deep(.fc-event) {
  border-radius: 8px;
  padding: 2px 4px;
}
</style>