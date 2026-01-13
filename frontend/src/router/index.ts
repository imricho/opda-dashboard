import { createRouter, createWebHistory } from "vue-router";
import SummaryPage from "@/pages/summary/SummaryPage.vue";
import ContractManagementPage from "@/pages/contracts/ContractManagementPage.vue";
import IncidentPage from "@/pages/incidents/IncidentPage.vue";
import ServerManagementPage from "@/pages/servers/ServerManagementPage.vue";
import WorkerPage from "@/pages/workorder/WorkorderPage.vue";

const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: "/", name: "summary", component: SummaryPage },
        { path: "/incidents", name: "incidents", component: IncidentPage },
        { path: "/contracts", name: "incidents", component: ContractManagementPage },
        { path: "/servers", name: "servers", component: ServerManagementPage },
        { path: "/workorders", name: "workorders", component: WorkerPage }
    ]
});

export default router;