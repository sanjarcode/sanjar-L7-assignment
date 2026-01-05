<script setup lang="ts">
import type { Movie } from '@/types';
import { RouterLink } from 'vue-router';
import Button from 'primevue/button';

defineProps<{
  movie: Movie
}>()
</script>

<template>

  <div class="group bg-imdb-dark rounded-md overflow-hidden shadow-sm hover:shadow-lg transition-shadow duration-300 w-full flex flex-col h-full">
    <RouterLink :to="{ name: 'movie-detail', params: { id: movie.id } }" class="block relative aspect-[2/3] w-full overflow-hidden bg-imdb-gray">
       <!-- Poster -->
       <img v-if="movie.poster_url" :src="movie.poster_url" :alt="movie.title" class="w-full h-full object-cover group-hover:opacity-90 transition-opacity" />
      <div v-else class="w-full h-full flex items-center justify-center text-imdb-light-gray font-bold text-4xl select-none group-hover:opacity-90 transition-opacity">
        {{ movie.title[0] }}
      </div>
    </RouterLink>

    <div class="p-3 flex-1 flex flex-col gap-1">
        <div class="flex items-center gap-1 mb-1">
            <i class="pi pi-star-fill text-imdb-yellow text-sm"></i>
            <span class="text-slate-300 text-sm font-semibold">7.4</span> <!-- Mock rating -->
        </div>

      <RouterLink :to="{ name: 'movie-detail', params: { id: movie.id } }">
        <h3 class="text-white hover:underline truncate" :title="movie.title">{{ movie.title }}</h3>
      </RouterLink>

      <p class="text-slate-400 text-xs">{{ movie.release_year }}</p>
    </div>
  </div>
</template>
