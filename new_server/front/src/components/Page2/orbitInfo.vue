<template>
    <div class="info-grid">
      <div class="info-group">
          <text class="info-description">X({{ $t('common.km') }})</text>
          <text class="orbit-info">{{ (this.orbitInfo.x || 0).toFixed(2) }}</text>
        </div>
        <div class="info-group">
          <text class="info-description">Z({{ $t('common.km') }})</text>
          <text class="orbit-info">{{ (this.orbitInfo.z || 0).toFixed(2) }}</text>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center">
          <text style="color: var(--text-primary);">{{ $t('orbit.family') }}</text>
          <text class="orbit-info" style="text-align: right">{{ tagToFamilyName[`${this.orbitInfo.lib_point}.${this.orbitInfo.family_tag}`] || '-' }}</text>
        </div>
        <div class="info-group">
          <text class="info-description">{{ $t('orbit.jacobi') }}</text>
          <text class="orbit-info">{{ (this.orbitInfo.cj || 0).toFixed(6) }}</text>
        </div>
        <div class="info-group">
          <text class="info-description">{{ $t('orbit.period') }}({{ $t('common.days') }})</text>
          <text class="orbit-info">{{ (this.orbitInfo.t || 0).toFixed(2) }}</text>
        </div>
        <div class="info-group">
          <text class="info-description">{{ $t('orbit.ax') }}({{ $t('common.km') }})</text>
          <text class="orbit-info">{{ (this.orbitInfo.ax || 0).toFixed(2) }}</text>
        </div>
        <div class="info-group">
          <text class="info-description">{{ $t('orbit.ay') }}({{ $t('common.km') }})</text>
          <text class="orbit-info">{{ (this.orbitInfo.ay || 0).toFixed(2) }}</text>
        </div>
        <div class="info-group">
          <text class="info-description">{{ $t('orbit.az') }}({{ $t('common.km') }})</text>
          <text class="orbit-info">{{ (this.orbitInfo.az || 0).toFixed(2) }}</text>
        </div>
        <div class="info-group">
          <text class="info-description">{{ $t('orbit.earth_dist') }}({{ $t('common.km') }})</text>
          <text class="orbit-info">{{ (this.orbitInfo.dist_primary || 0).toFixed(2) }}</text>
        </div>
        <div class="info-group">
          <text class="info-description">{{ $t('orbit.moon_dist') }}({{ $t('common.km') }})</text>
          <text class="orbit-info">{{ (this.orbitInfo.dist_secondary || 0).toFixed(2) }}</text>
        </div>
        <div class="info-group">
          <text class="info-description">{{ $t('orbit.stability') }}</text>
          <text class="orbit-info">{{ this.orbitInfo.stable === undefined ? '-' : (this.orbitInfo.stable ?  $t('orbit.stable') : $t('orbit.not_stable')) }}</text>
        </div>
      </div>
</template>

<script>
import { useOrbitNames } from '../../constants/familiesAndTags.js'
import { useI18n } from 'vue-i18n'

export default {
    props: {
      orbitInfo: {
        type: Object,
        default: () => ({})
      }
    },
    data() {
      return {
        localOrbitInfo: { ...this.orbitInfo }
      }
    },
    watch: {
      orbitInfo: {
        handler(newOrbitInfo) {
          this.localOrbitInfo = { ...newOrbitInfo };
        },
        deep: true,
        immediate: true
      }
    },
    setup() {
      const { t, locale } = useI18n();
      const { tagToFamilyName } = useOrbitNames()

      return { t, locale, tagToFamilyName }
    }
}
</script>

<style scoped>
.info-grid {
  margin-top: 5px;
  display: grid;
  gap: 6px 6px;
}

.info-group {
  display: contents;
  display: flex;
  justify-content: space-between;
}

.info-description {
  color: var(--text-primary);
  grid-column: 1;
}

.orbit-info {
  grid-column: 2;
  font-size: 16px;
  color: var(--text-orbit-info);
}
</style>