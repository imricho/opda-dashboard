import { createRouter, createWebHistory } from "vue-router";
import SummaryPage from "@/pages/summary/SummaryPage.vue";

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: "/", name: "summary", component: SummaryPage
        }
    ]
});

export default router;