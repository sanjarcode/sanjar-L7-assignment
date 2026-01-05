<script setup lang="ts">
import { RouterLink } from 'vue-router'
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import InputGroup from 'primevue/inputgroup';
import InputGroupAddon from 'primevue/inputgroupaddon';
</script>

<template>
  <nav class="sticky top-0 z-50 bg-imdb-black border-none shadow-md">
    <div class="container mx-auto px-4 h-14 flex items-center justify-between">
      <div class="flex items-center gap-4">
        <RouterLink to="/" class="flex items-center gap-1 group">
          <!-- IMDB Branding -->
          <div class="bg-imdb-yellow rounded px-2 py-1 text-black font-extrabold text-lg leading-none tracking-tighter">
            IMDb-L7
          </div>
        </RouterLink>
      </div>


      <div class="flex items-center gap-4">
        <!-- Removed IMDbPro, Watchlist, and Sign In as they are non-functional -->
      </div>
    </div>
  </nav>
</template>
