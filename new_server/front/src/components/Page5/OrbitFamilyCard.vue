<template>
  <article class="family-card">
    <div class="card-title">{{ title }}</div>

    <div class="card-content">
      <div class="image-box">
        <img :src="imageSrc" :alt="imageAlt" class="family-image" />
      </div>

      <div class="text-actions">
        <div class="description-box">
          {{ description }}
        </div>

        <RouterLink :to="to" class="more-button">
          {{ buttonLabel }}
        </RouterLink>
      </div>
    </div>
  </article>
</template>

<script setup>
import { RouterLink } from 'vue-router'

defineProps({
  title: { type: String, required: true },
  description: { type: String, required: true },
  imageSrc: { type: String, required: true },
  imageAlt: { type: String, default: '' },
  buttonLabel: { type: String, required: true },
  to: { type: String, required: true }
})
</script>

<style scoped>
.family-card {
  min-height: 340px;
  padding: 18px 18px 22px;
  display: flex;
  flex-direction: column;
  border-radius: 22px;
  border: 1px solid rgba(169, 197, 255, 0.22);
  background: color-mix(in srgb, var(--bg-primary) 96%, #eef5ff 4%);
  box-shadow: 0 0 18px 1px var(--shadow-primary);
  box-sizing: border-box;
}

.card-title {
  margin-bottom: 18px;
  min-height: 78px;
  padding: 10px 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 18px;
  background: color-mix(in srgb, var(--bg-primary) 94%, #eef5ff 6%);
  box-shadow: 0 0 14px 1px var(--shadow-primary);
  color: var(--highlight-color);
  font-size: 22px;
  font-weight: 400;
  line-height: 1.15;
  text-align: center;
}

.card-content {
  display: grid;
  grid-template-columns: minmax(260px, 1.1fr) minmax(240px, 0.9fr);
  gap: 18px;
  align-items: stretch;
  flex: 1;
}

.image-box {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 210px;
  padding: 4px;
}

.family-image {
  display: block;
  max-width: 100%;
  max-height: 210px;
  object-fit: contain;
}

.text-actions {
  display: grid;
  grid-template-rows: 1fr auto;
  gap: 18px;
  min-height: 210px;
}

.description-box,
.more-button {
  border-radius: 18px;
  background: color-mix(in srgb, var(--bg-primary) 94%, #eef5ff 6%);
  box-shadow: 0 0 14px 1px var(--shadow-primary);
  color: var(--highlight-color);
}

.description-box {
  min-height: 158px;
  padding: 18px 20px;
  box-sizing: border-box;
  font-size: 16px;
  font-weight: 400;
  line-height: 1.25;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
}

.more-button {
  min-height: 68px;
  border: none;
  padding: 10px 18px;
  font-size: 18px;
  font-weight: 400;
  line-height: 1.15;
  display: flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  cursor: pointer;
}

@media (max-width: 1500px) {
  .card-content {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .image-box {
    min-height: 0;
  }

  .family-image {
    max-height: 240px;
  }

  .text-actions {
    min-height: 0;
  }

  .description-box {
    min-height: 132px;
  }
}

@media (max-width: 980px) {
  .family-card {
    min-height: 0;
  }

  .card-content {
    grid-template-columns: 1fr;
  }

  .image-box {
    min-height: 0;
  }

  .family-image {
    max-height: 260px;
  }

  .text-actions {
    min-height: 0;
  }

  .description-box {
    min-height: 0;
  }
}

@media (max-width: 640px) {
  .family-card {
    padding: 14px 14px 18px;
  }

  .card-title {
    min-height: 0;
    padding: 10px 16px;
    font-size: 18px;
  }

  .description-box {
    padding: 14px 16px;
    font-size: 15px;
  }

  .more-button {
    min-height: 58px;
    font-size: 16px;
  }
}
</style>
