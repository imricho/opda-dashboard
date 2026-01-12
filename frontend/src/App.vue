<template>
  <div class="page">
    <!-- HEADER -->
    <AppHeader />

    <!-- MAIN CONTENT -->
    <div class="page-wrapper">
      <div class="page-body">
        <div class="container-xl py-3">
          <router-view />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import AppHeader from "@/components/AppHeader.vue";
</script>