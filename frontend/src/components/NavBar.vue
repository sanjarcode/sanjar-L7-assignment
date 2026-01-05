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
            IMDb
          </div>
        </RouterLink>

        <!-- Menu Button -->
        <Button label="Menu" icon="pi pi-bars" variant="text" class="!text-white !font-semibold hover:!bg-white/10 !px-3" />
      </div>

      <!-- Search Bar -->
      <div class="hidden md:flex flex-1 max-w-2xl mx-4">
          <InputGroup class="h-8">
            <InputGroupAddon class="!p-0 !min-w-0 bg-white">
                 <button class="flex items-center px-3 bg-white text-black font-semibold text-sm border-r border-gray-300 hover:bg-gray-100 h-full transition-colors rounded-l">
                    All <i class="pi pi-chevron-down ml-1 text-xs"></i>
                </button>
            </InputGroupAddon>

            <InputText placeholder="Search IMDb" class="!border-none !shadow-none !rounded-none !text-black !bg-white" />

            <InputGroupAddon class="!p-0 !min-w-0 bg-white rounded-r">
                <Button icon="pi pi-search" variant="text" class="!text-gray-500 hover:!text-black !w-10 !h-full !rounded-none" />
            </InputGroupAddon>
          </InputGroup>
      </div>

      <div class="flex items-center gap-4">
        <!-- Removed IMDbPro, Watchlist, and Sign In as they are non-functional -->
      </div>
    </div>
  </nav>
</template>
