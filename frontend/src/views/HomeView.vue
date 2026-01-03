<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import api from '@/api';
import type { Movie } from '@/types';
import MovieCard from '@/components/MovieCard.vue';
import { useRoute, useRouter } from 'vue-router';

// Search/Filter state
const movies = ref<Movie[]>([]);
const search = ref('');
const genreFilter = ref('');
const loading = ref(false);

const fetchMovies = async () => {
  loading.value = true;
  try {
    const params: any = {};
    if (search.value) params.search = search.value;
    if (genreFilter.value) params.genre = genreFilter.value;

    const response = await api.get('/movies/', { params });
    movies.value = response.data;
  } catch (error) {
    console.error("Failed to fetch movies", error);
  } finally {
    loading.value = false;
  }
};

// Debounce search could be added here, but for now direct watch
let timeout: any;
watch([search, genreFilter], () => {
  clearTimeout(timeout);
  timeout = setTimeout(() => {
    fetchMovies();
  }, 300);
});

onMounted(() => {
  fetchMovies();
});
</script>

<template>
  <div>
    <h1 class="text-3xl font-bold mb-6">Discover Movies</h1>

    <!-- Filters -->
    <div class="flex flex-col md:flex-row gap-4 mb-8">
      <input
        v-model="search"
        type="text"
        placeholder="Search movies..."
        class="flex-1 p-2 border rounded shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
      />
      <input
        v-model="genreFilter"
        type="text"
        placeholder="Filter by Genre..."
        class="flex-1 p-2 border rounded shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
      />
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-10">
      <p class="text-gray-500">Loading movies...</p>
    </div>

    <!-- Grid -->
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      <MovieCard v-for="movie in movies" :key="movie.id" :movie="movie" />
    </div>

    <div v-if="!loading && movies.length === 0" class="text-center py-10">
      <p class="text-gray-500">No movies found.</p>
    </div>
  </div>
</template>
