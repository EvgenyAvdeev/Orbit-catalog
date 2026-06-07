<template>
  <button @click="toggleTheme" class="theme-toggle">
    {{ currentTheme === 'dark' ? '☀️' : '🌙' }}
  </button>
</template>

<script setup>
import { inject } from 'vue'

const { currentTheme, toggleTheme } = inject('theme')
</script>

<style scoped>

.theme-toggle {
  cursor: pointer;
  padding: 10px;
  background-color: var(--bg-secondary);
  border: 2px solid var(--theme-toggle-border);
  border-radius: 8px;
}

</style>