<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue';
import api from '@/api';
import type { Movie } from '@/types';
import MovieCard from '@/components/MovieCard.vue';
import IconField from 'primevue/iconfield';
import InputIcon from 'primevue/inputicon';
import InputText from 'primevue/inputtext';
import Select from 'primevue/select';
import ProgressSpinner from 'primevue/progressspinner';
import ScriptEditor from '@/components/ScriptEditor.vue';

// Search/Filter state
const movies = ref<Movie[]>([]);
const search = ref('');
const genreFilter = ref(null);
const directorFilter = ref(null);
const actorFilter = ref(null);
const loading = ref(false);

const genresList = ref<{id: number, name: string}[]>([]);
const directorsList = ref<{id: number, name: string}[]>([]);
const actorsList = ref<{id: number, name: string}[]>([]);

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

const clearFilters = () => {
  search.value = '';
  genreFilter.value = null;
  directorFilter.value = null;
  actorFilter.value = null;
};

const hasActiveFilters = computed(() => {
  return !!(search.value || genreFilter.value || directorFilter.value || actorFilter.value);
});

// Debounce search could be added here, but for now direct watch
let timeout: ReturnType<typeof setTimeout>;
watch([search, genreFilter, directorFilter, actorFilter], () => {
  clearTimeout(timeout);
  timeout = setTimeout(() => {
    fetchMovies();
  }, 300);
});

const fetchMetadata = async () => {
    try {
        const [gRes, dRes, aRes] = await Promise.all([
            api.get('/genres/'),
            api.get('/directors/'),
            api.get('/actors/')
        ]);
        genresList.value = gRes.data;
        directorsList.value = dRes.data;
        actorsList.value = aRes.data;
    } catch (error) {
        console.error("Failed to fetch metadata", error);
    }
}

onMounted(() => {
  fetchMetadata();
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
                    <InputText v-model="search" placeholder="Search movies by title..." class="w-full !text-slate-700 !bg-white placeholder:!text-slate-400" />
                </IconField>
             </div>

             <!-- Advanced Filters -->
             <div class="flex flex-col md:flex-row gap-4 items-center">
                 <div class="flex-1 w-full">
                      <Select v-model="genreFilter" :options="genresList" optionLabel="name" optionValue="name" placeholder="Filter by Genre..." filter showClear class="w-full !bg-white custom-select" :pt="{ label: { class: '!text-slate-700' } }" />
                 </div>
                 <div class="flex-1 w-full">
                      <Select v-model="directorFilter" :options="directorsList" optionLabel="name" optionValue="name" placeholder="Filter by Director..." filter showClear class="w-full !bg-white custom-select" :pt="{ label: { class: '!text-slate-700' } }" />
                 </div>
                 <div class="flex-1 w-full">
                      <Select v-model="actorFilter" :options="actorsList" optionLabel="name" optionValue="name" placeholder="Filter by Actor..." filter showClear class="w-full !bg-white custom-select" :pt="{ label: { class: '!text-slate-700' } }" />
                 </div>
                 <button
                    @click="clearFilters"
                    :disabled="!hasActiveFilters"
                    class="px-4 py-2 text-sm font-medium transition-colors whitespace-nowrap border rounded"
                    :class="[
                        hasActiveFilters
                        ? 'text-slate-300 hover:text-imdb-yellow border-slate-500 hover:border-imdb-yellow'
                        : 'text-slate-600 border-slate-600 cursor-not-allowed opacity-50'
                    ]"
                 >
                    Clear All
                 </button>
             </div>
        </div>

        <!-- JS Script Editor -->
        <ScriptEditor />
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

<style scoped>
:deep(.custom-select .p-select-placeholder) {
    color: #cbd5e1 !important; /* text-slate-300 */
    font-size: 0.875rem;
}

:deep(.p-inputtext::placeholder) {
    color: #cbd5e1 !important; /* text-slate-300 */
}
</style>
