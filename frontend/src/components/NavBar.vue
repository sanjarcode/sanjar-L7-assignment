<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<template>
  <nav class="bg-indigo-600 p-4 shadow-md">
    <div class="container mx-auto flex justify-between items-center">
      <RouterLink to="/" class="text-white text-2xl font-bold">MovieExplorer</RouterLink>
      <div class="space-x-4">
        <RouterLink to="/" class="text-white hover:text-indigo-200">Home</RouterLink>
        <!-- Add more links if needed -->
      </div>
    </div>
  </nav>
</template>
