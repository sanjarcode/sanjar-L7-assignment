<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import api from '@/api';
import type { Movie } from '@/types';
import MovieCard from '@/components/MovieCard.vue';
import IconField from 'primevue/iconfield';
import InputIcon from 'primevue/inputicon';
import InputText from 'primevue/inputtext';
import ProgressSpinner from 'primevue/progressspinner';

// Search/Filter state
const movies = ref<Movie[]>([]);
const search = ref('');
const genreFilter = ref('');
const directorFilter = ref('');
const actorFilter = ref('');
const loading = ref(false);

const fetchMovies = async () => {
  loading.value = true;
  try {
    const params: Record<string, string> = {};
    if (search.value) params.search = search.value;
    if (genreFilter.value) params.genre = genreFilter.value;
    if (directorFilter.value) params.director = directorFilter.value;
    if (actorFilter.value) params.actor = actorFilter.value;

    const response = await api.get('/movies/', { params });
    movies.value = response.data;
  } catch (error) {
    console.error("Failed to fetch movies", error);
  } finally {
    loading.value = false;
  }
};

// Debounce search could be added here, but for now direct watch
let timeout: ReturnType<typeof setTimeout>;
watch([search, genreFilter, directorFilter, actorFilter], () => {
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
  <div class="min-h-screen pb-20 bg-imdb-black text-white">
    <!-- Hero / Featured Section (Simplified) -->
    <div class="bg-black py-8 border-b border-white/10">
        <div class="container mx-auto px-4">
             <h1 class="text-3xl font-bold text-imdb-yellow mb-2">What to watch</h1>
             <p class="text-slate-400">Fan favorites and new releases</p>
        </div>
    </div>

    <!-- Filters and Search -->
    <div class="container mx-auto px-4 py-8">
        <div class="flex flex-col gap-4 mb-8 bg-imdb-gray p-4 rounded text-black">
             <!-- Main Search -->
             <div class="w-full">
                <IconField>
                    <InputIcon class="pi pi-search" />
                    <InputText v-model="search" placeholder="Search movies by title..." class="w-full !text-black !bg-white" />
                </IconField>
             </div>

             <!-- Advanced Filters -->
             <div class="flex flex-col md:flex-row gap-4">
                 <div class="flex-1">
                     <InputText v-model="genreFilter" placeholder="Filter by Genre..." class="w-full !text-black !bg-white" />
                 </div>
                 <div class="flex-1">
                     <InputText v-model="directorFilter" placeholder="Filter by Director..." class="w-full !text-black !bg-white" />
                 </div>
                 <div class="flex-1">
                     <InputText v-model="actorFilter" placeholder="Filter by Actor..." class="w-full !text-black !bg-white" />
                 </div>
             </div>
        </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex flex-col items-center justify-center py-20">
      <ProgressSpinner style="width: 50px; height: 50px" strokeWidth="4" fill="transparent" animationDuration=".5s" />
      <p class="text-slate-400 font-medium mt-4">Loading movies...</p>
    </div>

    <!-- Grid -->
    <div v-else class="container mx-auto px-4">
        <h2 class="text-2xl font-bold text-imdb-yellow mb-6 border-l-4 border-imdb-yellow pl-3">
            Top Picks
        </h2>
        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6">
            <MovieCard v-for="movie in movies" :key="movie.id" :movie="movie" />
        </div>
    </div>

    <div v-if="!loading && movies.length === 0" class="text-center py-20">
      <p class="text-slate-500 text-lg">No movies found matching your criteria.</p>
    </div>
  </div>
</template>
