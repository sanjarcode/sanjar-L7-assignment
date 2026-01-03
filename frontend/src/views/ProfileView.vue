<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import api from '@/api';
import type { Director, Actor } from '@/types';
import MovieCard from '@/components/MovieCard.vue';

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
  <div v-if="loading" class="text-center py-10">Loading...</div>
  <div v-else-if="person" class="space-y-6">
    <div class="bg-white p-6 rounded-lg shadow-md">
      <h1 class="text-3xl font-bold text-gray-800">{{ person.name }}</h1>
      <p class="text-gray-500 capitalize">{{ type.slice(0, -1) }} Profile</p>
    </div>

    <div>
      <h2 class="text-2xl font-bold mb-4">Filmography</h2>
      <div v-if="person.movies && person.movies.length > 0" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
         <MovieCard v-for="movie in person.movies" :key="movie.id" :movie="movie" />
      </div>
      <p v-else class="text-gray-500">No movies found.</p>
    </div>
  </div>
  <div v-else class="text-center text-red-500">Profile not found</div>
</template>
