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
      <div class="w-full h-full flex items-center justify-center text-imdb-light-gray font-bold text-4xl select-none group-hover:opacity-90 transition-opacity">
        {{ movie.title[0] }}
      </div>
      <div class="absolute top-0 left-0">
          <div class="bg-black/60 p-1 flex items-center justify-center">
             <i class="pi pi-bookmark-plus text-white/50 hover:text-white cursor-pointer text-2xl"></i>
          </div>
      </div>
    </RouterLink>

    <div class="p-3 flex-1 flex flex-col gap-1">
        <div class="flex items-center gap-1 mb-1">
            <i class="pi pi-star-fill text-imdb-yellow text-sm"></i>
            <span class="text-slate-300 text-sm font-semibold">7.4</span> <!-- Mock rating -->
            <Button icon="pi pi-thumbs-up" variant="text" class="ml-auto !text-blue-400 hover:!bg-slate-800/50 !p-0 !w-8 !h-8" rounded />
        </div>

      <RouterLink :to="{ name: 'movie-detail', params: { id: movie.id } }">
        <h3 class="text-white hover:underline truncate" :title="movie.title">{{ movie.title }}</h3>
      </RouterLink>

      <p class="text-slate-400 text-xs">{{ movie.release_year }}</p>

      <Button label="Watchlist" icon="pi pi-plus" class="mt-3 w-full !bg-imdb-gray !text-blue-400 !font-bold !text-sm !py-2 !border-none hover:!bg-opacity-80 group-hover:!bg-imdb-gray/80" />

      <div class="mt-2 flex items-center justify-center gap-2 text-xs text-slate-300 hover:text-white cursor-pointer group/play">
          <i class="pi pi-play-circle text-3xl text-gray-400 group-hover/play:text-white transition-colors"></i>
          <span>Trailer</span>
      </div>

    </div>
  </div>
</template>
