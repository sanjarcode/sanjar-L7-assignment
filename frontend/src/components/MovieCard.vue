<script setup lang="ts">
import type { Movie } from '@/types';
import { RouterLink } from 'vue-router';

defineProps<{
  movie: Movie
}>()
</script>

<template>
  <div class="bg-white rounded-lg shadow-md p-4 hover:shadow-lg transition">
    <RouterLink :to="{ name: 'movie-detail', params: { id: movie.id } }">
      <h3 class="text-xl font-semibold mb-2 text-indigo-700">{{ movie.title }}</h3>
      <p class="text-gray-600 mb-2">{{ movie.release_year }}</p>
      <div class="flex flex-wrap gap-2 mb-2">
        <span v-for="genre in movie.genres" :key="genre.id" class="px-2 py-1 bg-gray-200 rounded text-sm text-gray-700">
          {{ genre.name }}
        </span>
      </div>
      <p v-if="movie.director" class="text-sm text-gray-500">
        Dir: {{ movie.director.name }}
      </p>
    </RouterLink>
  </div>
</template>
