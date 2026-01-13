<template>
  <header class="navbar navbar-expand-md navbar-light d-print-none">
    <div class="container-xl">
      <!-- Brand -->
      <a class="navbar-brand d-flex align-items-center gap-2" href="#">
        <span class="avatar avatar-sm bg-primary-lt">op</span>
        <span class="fw-bold">opda</span>
      </a>

      <!-- Right side top actions -->
      <div class="navbar-nav flex-row order-md-last">
        <!-- Collapse/Expand menu bar -->
        <button
            class="btn btn-ghost-secondary me-2"
            type="button"
            @click="toggleMenuBar"
            :aria-expanded="menuBarOpen ? 'true' : 'false'"
            aria-label="Toggle header menu"
        >
          <!-- “hamburger / close” -->
          <svg v-if="!menuBarOpen" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="4" y1="6" x2="20" y2="6"/><line x1="4" y1="12" x2="20" y2="12"/><line x1="4" y1="18" x2="20" y2="18"/>
          </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
          </svg>
        </button>

        <!-- Theme toggle (light/dark) -->
        <button class="btn btn-ghost-secondary me-2" type="button" @click="toggleTheme" aria-label="Toggle theme">
          <svg v-if="theme === 'light'" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="M4.93 4.93l1.41 1.41"/><path d="M17.66 17.66l1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="M6.34 17.66l-1.41 1.41"/><path d="M19.07 4.93l-1.41 1.41"/>
          </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
          </svg>
        </button>

        <!-- Notifications -->
        <a class="nav-link px-0 me-2" href="#" aria-label="Notifications">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M18 8a6 6 0 0 0-12 0c0 7-3 9-3 9h18s-3-2-3-9"/>
            <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
          </svg>
          <span class="badge bg-red"></span>
        </a>

        <!-- User dropdown -->
        <div class="nav-item dropdown">
          <a class="nav-link d-flex lh-1 text-reset p-0" href="#" data-bs-toggle="dropdown" aria-label="Open user menu">
            <span class="avatar avatar-sm" style="background-image: url('https://i.pravatar.cc/64?img=3')"></span>
            <div class="d-none d-xl-block ps-2">
              <div class="fw-semibold">Coco</div>
              <div class="mt-1 small text-secondary">OPDA</div>
            </div>
          </a>
          <div class="dropdown-menu dropdown-menu-end dropdown-menu-arrow">
            <a class="dropdown-item" href="#">Profile</a>
            <a class="dropdown-item" href="#">Settings</a>
            <div class="dropdown-divider"></div>
            <a class="dropdown-item" href="#">Logout</a>
          </div>
        </div>
      </div>
    </div>
  </header>

  <!-- SECOND ROW: menu bar (Tabler-style) -->
  <div class="navbar navbar-expand-md navbar-light d-print-none border-top" v-show="menuBarOpen">
    <div class="container-xl">
      <!-- In mobile, this collapses -->
      <div class="collapse navbar-collapse show">
        <ul class="navbar-nav">
          <li class="nav-item">
            <a class="nav-link" href="#">
              <span class="nav-link-title">Dashboards</span>
            </a>
          </li>

          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" data-bs-toggle="dropdown">
              <span class="nav-link-title">Interface</span>
            </a>
            <div class="dropdown-menu">
              <a class="dropdown-item" href="#">Cards</a>
              <a class="dropdown-item" href="#">Tables</a>
              <a class="dropdown-item" href="#">Charts</a>
            </div>
          </li>

          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" data-bs-toggle="dropdown">
              <span class="nav-link-title">Forms</span>
            </a>
            <div class="dropdown-menu">
              <a class="dropdown-item" href="#">Inputs</a>
              <a class="dropdown-item" href="#">Validation</a>
            </div>
          </li>

          <li class="nav-item"><router-link class="nav-link" to="/contracts"><span class="nav-link-title">Contracts</span></router-link></li>
          <li class="nav-item"><router-link class="nav-link" to="/servers"><span class="nav-link-title">Servers</span></router-link></li>
          <li class="nav-item"><a class="nav-link" href="#"><span class="nav-link-title">Layout</span></a></li>
          <li class="nav-item"><a class="nav-link" href="#"><span class="nav-link-title">Plugins</span></a></li>
          <li class="nav-item"><a class="nav-link" href="#"><span class="nav-link-title">Addons</span></a></li>
          <li class="nav-item"><a class="nav-link" href="#"><span class="nav-link-title">Help</span></a></li>
        </ul>

        <!-- Right side action like “Theme settings” -->
        <div class="ms-auto d-flex align-items-center gap-2">
          <a class="btn btn-sm btn-outline-secondary" href="#">
            Theme Settings <span class="badge bg-red ms-1">New</span>
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";

const menuBarOpen = ref(true);
const theme = ref("light");

function toggleMenuBar() {
  menuBarOpen.value = !menuBarOpen.value;
}

function applyTheme(next: string) {
  theme.value = next;
  document.documentElement.setAttribute("data-bs-theme", next);
  localStorage.setItem("opda_theme", next);
}

function toggleTheme() {
  applyTheme(theme.value === "light" ? "dark" : "light");
}

onMounted(() => {
  const saved = localStorage.getItem("opda_theme");
  applyTheme(saved === "dark" ? "dark" : "light");
});
</script>

<style scoped>
/* Optional: make the second row feel tighter like Tabler demo */
.navbar.border-top {
  --tblr-navbar-padding-y: 0.35rem;
}
.badge.bg-red {
  top: 0px;
  right: 0px;
  width: 8px;
  height: 8px;
  padding: 0;
  border-radius: 999px;
}
</style>