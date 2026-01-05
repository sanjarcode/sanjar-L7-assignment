<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, RouterLink } from 'vue-router';
import api from '@/api';
import type { Movie } from '@/types';
import Button from 'primevue/button';
import Tag from 'primevue/tag';
import ProgressSpinner from 'primevue/progressspinner';

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
  <div v-if="loading" class="flex items-center justify-center min-h-[50vh]">
      <ProgressSpinner style="width: 50px; height: 50px" strokeWidth="4" fill="transparent" animationDuration=".5s" />
  </div>
  <div v-else-if="movie" class="bg-imdb-dark min-h-screen text-white">
    <!-- Header -->
    <div class="bg-black/20 p-6">
        <div class="container mx-auto">
             <div class="flex justify-between items-start mb-4">
                 <div class="space-y-2">
                     <h1 class="text-4xl font-normal text-white">{{ movie.title }}</h1>
                     <div class="flex items-center gap-4 text-sm text-slate-400">
                         <span>{{ movie.release_year }}</span>
                         <span>•</span>
                         <div class="flex gap-2">
                             <Tag v-for="genre in movie.genres" :key="genre.id" :value="genre.name" severity="secondary" />
                         </div>
                     </div>
                 </div>
                 <div class="hidden md:flex flex-col items-end">
                      <div class="text-xs text-slate-400 font-bold tracking-widest uppercase mb-1">IMDb RATING</div>
                      <div class="flex items-center gap-2">
                          <i class="pi pi-star-fill text-imdb-yellow text-3xl"></i>
                        <div class="flex flex-col">
                             <span class="text-xl font-bold text-white leading-none">7.4<span class="text-base text-slate-400 font-normal">/10</span></span>
                             <span class="text-xs text-slate-400">12K votes</span>
                        </div>
                      </div>
                 </div>
             </div>
        </div>
    </div>

    <div class="container mx-auto p-6">
        <div class="flex flex-col md:flex-row gap-8">
            <!-- Poster Side -->
             <div class="w-full md:w-1/3 lg:w-1/4">
                 <div class="aspect-[2/3] bg-imdb-gray rounded overflow-hidden flex items-center justify-center text-5xl font-bold text-imdb-light-gray select-none relative group">
                      <img v-if="movie.poster_url" :src="movie.poster_url" :alt="movie.title" class="w-full h-full object-cover group-hover:opacity-90 transition-opacity" />
                      <span v-else>{{ movie.title[0] }}</span>
                      <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent flex items-end p-4 opacity-0 group-hover:opacity-100 transition-opacity">
                         <Button label="Watch Trailer" icon="pi pi-play" class="w-full !bg-imdb-yellow/90 hover:!bg-imdb-yellow !text-black !font-bold !border-none" />
                      </div>
                 </div>
             </div>

             <!-- Main Content -->
             <div class="flex-1">
                 <!-- Director -->
                 <div class="border-b border-white/10 py-4 flex items-center gap-2">
                     <span class="font-bold text-white">Director</span>
                     <Button v-if="movie.director" :label="movie.director.name" as="router-link" :to="{name: 'profile', params: {type: 'directors', id: movie.director.id}}" variant="link" class="!p-0 !text-blue-400" />
                     <span v-else class="text-slate-400">Unknown</span>
                 </div>

                 <!-- Cast -->
                 <div class="py-6">
                     <h2 class="text-2xl font-bold text-imdb-yellow mb-4 border-l-4 border-imdb-yellow pl-3">Top Cast</h2>
                     <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
                         <RouterLink
                             v-for="actor in movie.actors"
                             :key="actor.id"
                             :to="{name: 'profile', params: {type: 'actors', id: actor.id}}"
                             class="flex items-center gap-3 bg-imdb-gray p-2 rounded hover:bg-white/10 transition-colors group"
                         >
                             <div class="w-12 h-12 rounded-full overflow-hidden bg-imdb-black flex items-center justify-center text-slate-500 font-bold text-xs group-hover:text-white transition-colors">
                                <img v-if="actor.profile_url" :src="actor.profile_url" :alt="actor.name" class="w-full h-full object-cover" />
                                <span v-else>{{ actor.name[0] }}</span>
                            </div>
                            <span class="text-slate-200 text-sm font-semibold truncate group-hover:text-white transition-colors">{{ actor.name }}</span>
                         </RouterLink>
                     </div>
                 </div>
             </div>
        </div>
    </div>
  </div>
  <div v-else class="text-center text-red-500 py-10">Movie not found</div>
</template>
