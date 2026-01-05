<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import api from '@/api';
import type { Director, Actor } from '@/types';
import MovieCard from '@/components/MovieCard.vue';
import ProgressSpinner from 'primevue/progressspinner';

const route = useRoute();
const person = ref<Director | Actor | null>(null);
const loading = ref(true);
const type = ref('');

const fetchPerson = async () => {
    loading.value = true;
    try {
        const id = route.params.id;
        type.value = route.params.type as string; // 'actors' or 'directors'
        const response = await api.get(`/${type.value}/${id}`);
        person.value = response.data;
    } catch (error) {
        console.error("Error fetching profile", error);
    } finally {
        loading.value = false;
    }
}

onMounted(fetchPerson);
watch(() => route.params, fetchPerson);
</script>

<template>
  <div v-if="loading" class="flex items-center justify-center min-h-[50vh]">
      <ProgressSpinner style="width: 50px; height: 50px" strokeWidth="4" fill="transparent" animationDuration=".5s" />
  </div>
  <div v-else-if="person" class="space-y-6">
    <div class="bg-imdb-dark p-8 rounded border border-white/5">
      <h1 class="text-4xl font-bold text-white mb-2">{{ person.name }}</h1>
      <p class="text-imdb-yellow font-semibold uppercase tracking-wider text-sm">{{ type.slice(0, -1) }}</p>
    </div>

    <div>
      <h2 class="text-2xl font-bold text-imdb-yellow mb-4 border-l-4 border-imdb-yellow pl-3">Filmography</h2>
      <div v-if="person.movies && person.movies.length > 0" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6">
         <MovieCard v-for="movie in person.movies" :key="movie.id" :movie="movie" />
      </div>
      <p v-else class="text-slate-500">No movies found.</p>
    </div>
  </div>
  <div v-else class="text-center text-red-500 py-10">Profile not found</div>
</template>
