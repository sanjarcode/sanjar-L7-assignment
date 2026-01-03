<script setup lang="ts">
import { RouterView } from 'vue-router'
import NavBar from './components/NavBar.vue'
</script>

<template>
  <div class="min-h-screen flex flex-col">
    <NavBar />
    <main class="flex-grow container mx-auto p-4">
      <RouterView />
    </main>
    <footer class="bg-gray-800 text-white text-center p-4">
      &copy; 2026 Movie Explorer
    </footer>
  </div>
</template>
