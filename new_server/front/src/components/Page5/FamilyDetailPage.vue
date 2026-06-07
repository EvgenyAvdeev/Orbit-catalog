<template>
  <div v-if="detail" class="family-detail-page">
    <section class="detail-shell">
      <div class="detail-toolbar">
        <button type="button" class="back-button" @click="goBack" :aria-label="content.detail.back">
          <img
            :src="theme.currentTheme?.value === 'light' ? HiddingArrow : HiddingArrowDark"
            class="back-arrow"
            alt="back"
          />
        </button>
      </div>

      <div class="detail-top">
        <div class="image-panel">
          <div class="panel-title">{{ detail.title }}</div>
          <div class="panel-image-wrap">
            <img :src="meta.image" :alt="detail.title" class="detail-image" />
          </div>
        </div>

        <div class="text-panel-wrap">
          <div class="description-panel">{{ detail.longDescription }}</div>
          <div class="publications-title">{{ content.detail.publicationsTitle }}</div>
        </div>
      </div>

      <div class="publications-list">
        <article
          v-for="(publication, index) in detail.publications"
          :key="`${meta.slug}-${index}`"
          class="publication-card"
        >
          {{ publication }}
        </article>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, inject, watchEffect } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute, useRouter } from 'vue-router'
import { familyOverviewMetaBySlug, page5Content } from '../../constants/page5Content'
import HiddingArrow from '../../assets/hidding-arrow.svg'
import HiddingArrowDark from '../../assets/hidding-arrow-dark.svg'

const route = useRoute()
const router = useRouter()
const { locale } = useI18n()
const theme = inject('theme', { currentTheme: { value: 'light' } })

const currentLanguage = computed(() => locale.value?.startsWith('ru') ? 'ru' : 'en')
const content = computed(() => page5Content[currentLanguage.value])
const meta = computed(() => familyOverviewMetaBySlug[route.params.familyId])
const detail = computed(() => {
  if (!meta.value) return null
  return content.value.details[meta.value.key] ?? null
})

watchEffect(() => {
  if (!meta.value || !detail.value) {
    router.replace('/families')
  }
})

const goBack = () => {
  router.push('/families')
}
</script>

<style scoped>
.family-detail-page {
  width: 100%;
  min-height: 100%;
  padding: 20px 28px 28px;
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

.detail-shell {
  position: relative;
  max-width: 1420px;
  margin: 0 auto;
  padding: 24px 24px 28px;
  border-radius: 24px;
  border: 2px solid rgba(169, 197, 255, 0.22);
  background: color-mix(in srgb, var(--bg-primary) 96%, #eef5ff 4%);
  box-shadow: 0 0 20px 2px var(--shadow-primary);
}

.detail-toolbar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 10px;
}

.back-button {
  width: 45px;
  height: 45px;
  border: none;
  border-radius: 13px;
  background: var(--bg-primary);
  box-shadow: 0 0 9px 1px var(--shadow-primary);
  cursor: pointer;
  outline: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0;
}

.back-arrow {
  height: 30px;
  padding: 7px 14px 7px 12px;
  display: inline-block;
  transition: transform 0.2s ease;
}

.detail-top {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1.15fr);
  gap: 18px;
  align-items: stretch;
  margin-bottom: 22px;
}

.image-panel,
.description-panel,
.publications-title,
.publication-card {
  border-radius: 18px;
  background: color-mix(in srgb, var(--bg-primary) 94%, #eef5ff 6%);
  box-shadow: 0 0 14px 1px var(--shadow-primary);
}

.image-panel {
  padding: 18px 18px 20px;
}

.panel-title {
  margin-bottom: 18px;
  padding: 10px 24px;
  border-radius: 18px;
  background: color-mix(in srgb, var(--bg-primary) 94%, #eef5ff 6%);
  box-shadow: 0 0 14px 1px var(--shadow-primary);
  color: var(--highlight-color);
  font-size: 22px;
  font-weight: 400;
  line-height: 1.15;
  text-align: center;
}

.panel-image-wrap {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 360px;
  padding: 8px 10px;
}

.detail-image {
  display: block;
  max-width: 100%;
  max-height: 360px;
  object-fit: contain;
}

.text-panel-wrap {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.description-panel {
  flex: 1;
  padding: 18px 20px;
  color: var(--highlight-color);
  font-size: 22px;
  font-weight: 400;
  line-height: 1.35;
  white-space: pre-line;
}

.publications-title {
  min-height: 74px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 10px 18px;
  color: var(--highlight-color);
  font-size: 22px;
  font-weight: 400;
  line-height: 1.15;
  text-align: center;
}

.publications-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.publication-card {
  padding: 14px 22px;
  color: var(--highlight-color);
  font-size: 17px;
  font-weight: 400;
  line-height: 1.28;
}

@media (max-width: 1520px) {
  .family-detail-page {
    padding: 18px 16px 24px;
  }

  .detail-shell {
    padding: 20px 18px 24px;
  }
}

@media (max-width: 1240px) {
  .detail-top {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 760px) {
  .panel-title,
  .publications-title,
  .description-panel {
    font-size: 18px;
  }

  .panel-image-wrap {
    min-height: 240px;
  }

  .detail-image {
    max-height: 240px;
  }

  .publication-card {
    padding: 12px 16px;
    font-size: 15px;
  }
}
</style>
