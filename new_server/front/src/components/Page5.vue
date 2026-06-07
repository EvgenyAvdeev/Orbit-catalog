<template>
  <div class="families-page">
    <section class="families-shell">
      <div class="section-title">{{ content.header }}</div>

      <div class="cards-grid">
        <OrbitFamilyCard
          v-for="card in familyCards"
          :key="card.key"
          :title="card.title"
          :description="card.description"
          :image-src="card.image"
          :image-alt="card.title"
          :button-label="content.more"
          :to="card.to"
        />
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import OrbitFamilyCard from './Page5/OrbitFamilyCard.vue'
import { familyOverviewMeta, page5Content } from '../constants/page5Content'

const { locale } = useI18n()

const currentLanguage = computed(() => locale.value?.startsWith('ru') ? 'ru' : 'en')
const content = computed(() => page5Content[currentLanguage.value])

const familyCards = computed(() => familyOverviewMeta.map((card) => ({
  key: card.key,
  title: content.value.cards[card.key].title,
  description: content.value.cards[card.key].description,
  image: card.image,
  to: `/families/${card.slug}`
})))
</script>

<style scoped>
.families-page {
  width: 100%;
  min-height: 100%;
  padding: 24px 30px 36px;
  box-sizing: border-box;
  background-color: var(--bg-primary);
  background-image:
    linear-gradient(var(--minor-grid-color) 1px, transparent 1px),
    linear-gradient(90deg, var(--minor-grid-color) 1px, transparent 1px),
    linear-gradient(var(--grid-color) 1px, transparent 1px),
    linear-gradient(90deg, var(--grid-color) 1px, transparent 1px);
  background-size: 32px 32px, 32px 32px, 160px 160px, 160px 160px;
  background-position: -1px -1px, -1px -1px, -1px -1px, -1px -1px;
}

.families-shell {
  max-width: 1460px;
  margin: 0 auto;
  padding: 34px 42px 42px;
  border-radius: 24px;
  border: 2px solid rgba(169, 197, 255, 0.22);
  background: color-mix(in srgb, var(--bg-primary) 96%, #eef5ff 4%);
  box-shadow: 0 0 20px 2px var(--shadow-primary);
}

.section-title {
  width: fit-content;
  max-width: 100%;
  min-width: 0;
  box-sizing: border-box;
  display: block;
  margin-bottom: 26px;
  padding: 10px 28px;
  border-radius: 20px;
  background: color-mix(in srgb, var(--bg-primary) 94%, #eef5ff 6%);
  box-shadow: 0 0 16px 1px var(--shadow-primary);
  color: var(--highlight-color);
  font-size: 28px;
  font-weight: 400;
  line-height: 1.15;
  text-align: center;
  white-space: normal;
  overflow-wrap: anywhere;
}

.cards-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 34px 32px;
}

@media (max-width: 1520px) {
  .families-page {
    padding: 20px 18px 30px;
  }

  .families-shell {
    padding: 28px 26px 32px;
  }
}

@media (max-width: 1280px) {
  .cards-grid {
    grid-template-columns: 1fr;
    gap: 26px;
  }
}

@media (max-width: 900px) {
  .families-shell {
    padding: 22px 18px 26px;
  }

  .section-title {
    min-width: 0;
    width: 100%;
    padding-inline: 18px;
    font-size: 22px;
  }
}
</style>
