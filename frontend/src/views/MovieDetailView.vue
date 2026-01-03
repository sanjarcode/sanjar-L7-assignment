<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, RouterLink } from 'vue-router';
import api from '@/api';
import type { Movie } from '@/types';

const route = useRoute();
const movie = ref<Movie | null>(null);
const loading = ref(true);

onMounted(async () => {
  try {
    const id = route.params.id;
    const response = await api.get(`/movies/${id}`);
    movie.value = response.data;
  } catch (error) {
    console.error("Error fetching movie", error);
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <div v-if="loading" class="text-center py-10">Loading...</div>
  <div v-else-if="movie" class="bg-white rounded-lg shadow-lg p-8">
    <div class="flex flex-col md:flex-row justify-between items-start mb-6">
      <h1 class="text-4xl font-bold text-indigo-800">{{ movie.title }}</h1>
      <span class="text-xl text-gray-500 font-bold border p-2 rounded">{{ movie.release_year }}</span>
    </div>

    <div class="mb-6">
      <h3 class="text-lg font-semibold mb-2">Director</h3>
      <RouterLink v-if="movie.director" :to="{name: 'profile', params: {type: 'directors', id: movie.director.id}}" class="text-indigo-600 hover:underline">
        {{ movie.director.name }}
      </RouterLink>
      <span v-else>Unknown</span>
    </div>

    <div class="mb-6">
      <h3 class="text-lg font-semibold mb-2">Genres</h3>
      <div class="flex flex-wrap gap-2">
         <span v-for="genre in movie.genres" :key="genre.id" class="px-3 py-1 bg-gray-200 rounded-full text-sm text-gray-700">
          {{ genre.name }}
        </span>
      </div>
    </div>

    <div class="mb-6">
      <h3 class="text-lg font-semibold mb-2">Cast</h3>
      <div class="flex flex-wrap gap-4">
        <RouterLink
          v-for="actor in movie.actors"
          :key="actor.id"
          :to="{name: 'profile', params: {type: 'actors', id: actor.id}}"
          class="bg-indigo-50 px-4 py-2 rounded text-indigo-700 hover:bg-indigo-100 transition"
        >
          {{ actor.name }}
        </RouterLink>
      </div>
    </div>
  </div>
  <div v-else class="text-center text-red-500">Movie not found</div>
</template>
