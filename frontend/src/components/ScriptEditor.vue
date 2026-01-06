<script setup lang="ts">
import { ref } from 'vue';
import Button from 'primevue/button';
import Textarea from 'primevue/textarea';

const code = ref('');
const output = ref('');

const runCode = () => {
    try {
        // Simple eval for demonstration purposes
        // In a real app, we might use a safer method
        const result = eval(code.value);
        output.value = result !== undefined ? String(result) : 'Success (no return value)';
    } catch (error: any) {
        output.value = `Error: ${error.message}`;
    }
};

const clearAll = () => {
    code.value = '';
    output.value = '';
};
</script>

<template>
    <div class="bg-imdb-gray p-4 rounded-lg border border-white/10 shadow-xl mb-8">
        <div class="flex items-center justify-between mb-4 border-b border-white/10 pb-2">
            <h3 class="text-imdb-yellow font-bold uppercase tracking-wider text-sm flex items-center gap-2">
                <i class="pi pi-code"></i> JS Playground
            </h3>
            <div class="flex gap-2">
                <Button label="Run" icon="pi pi-play" size="small" severity="success" @click="runCode" :disabled="!code.trim()" />
                <Button label="Clear" icon="pi pi-refresh" size="small" severity="secondary" @click="clearAll" />
            </div>
        </div>

        <div class="space-y-4">
            <div class="relative group">
                <div class="absolute -inset-0.5 bg-gradient-to-r from-imdb-yellow to-yellow-600 rounded-lg blur opacity-20 group-hover:opacity-40 transition duration-1000 group-hover:duration-200"></div>
                <Textarea
                    v-model="code"
                    placeholder="// Write your JavaScript code here...
console.log('Hello from IMDb-L7!');
const movies = ['Inception', 'The Matrix'];
movies.join(', ');"
                    rows="5"
                    class="w-full !bg-black !text-emerald-400 !font-mono !border-none focus:!ring-1 focus:!ring-imdb-yellow rounded-lg relative"
                />
            </div>

            <div v-if="output" class="p-3 bg-black/50 border border-white/5 rounded-lg">
                <div class="text-xs text-slate-500 mb-1 uppercase font-bold tracking-tighter">Output</div>
                <pre class="text-sm font-mono whitespace-pre-wrap" :class="output.startsWith('Error') ? 'text-red-400' : 'text-slate-300'">{{ output }}</pre>
            </div>
        </div>
    </div>
</template>

<style scoped>
:deep(.p-textarea) {
    padding: 1rem;
    line-height: 1.5;
}
</style>
