<template>
  <div class="page">
    <!-- Sidebar -->
    <aside class="navbar navbar-vertical navbar-expand-lg" data-bs-theme="dark">
      <div class="container-fluid">
        <h1 class="navbar-brand navbar-brand-autodark">
          <a href="#" class="text-decoration-none text-white">
            OPDA Dashboard
          </a>
        </h1>

        <div class="collapse navbar-collapse show">
          <ul class="navbar-nav pt-lg-3">

            <li class="nav-item">
              <RouterLink class="nav-link" to="/">
                <span class="nav-link-title">Summary</span>
              </RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink class="nav-link" to="/incidents">
                <span class="nav-link-title">Incidents</span>
              </RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink class="nav-link" to="/workorders">
                <span class="nav-link-title">Workorders</span>
              </RouterLink>
            </li>

          </ul>
        </div>
      </div>
    </aside>

    <!-- Main content -->
    <div class="page-wrapper">
      <!-- Topbar -->
      <header class="navbar navbar-expand-md d-print-none">
        <div class="container-xl">
          <div class="navbar-nav flex-row order-md-last gap-2">
            <div class="text-secondary align-self-center">
              Logged in as <span class="fw-semibold">{{ username }}</span>
            </div>
          </div>
        </div>
      </header>

      <!-- Page body -->
      <div class="page-body">
        <div class="container-xl">
          <slot />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";

// temporary: read username from localStorage token payload if you want
const username = computed(() => localStorage.getItem("opda_username") ?? "coco");
</script>

<style scoped>
/* Make active route look nicer */
.router-link-active {
  font-weight: 600;
}
</style>