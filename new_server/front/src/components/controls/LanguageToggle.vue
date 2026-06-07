<template>
  <button @click="toggleLanguage" class="language-toggle">
    <text style="color: var(--text-primary)">{{ currentLocale === 'en' ? 'RU' : 'EN' }}</text>
  </button>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import { computed } from 'vue'
import { updateTitle } from '../../main.js'

const { locale } = useI18n()

const currentLocale = computed(() => locale.value)

const toggleLanguage = () => {
  const newLocale = currentLocale.value === 'en' ? 'ru' : 'en'
  locale.value = newLocale
  localStorage.setItem('locale', newLocale)

  updateTitle()
}
</script>

<style scoped>
.language-toggle {
  cursor: pointer;
  background-color: var(--bg-secondary);
  border: 2px solid var(--theme-toggle-border);
  border-radius: 8px;
  width: 41px;
  height: 41px;
}
</style>