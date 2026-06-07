<template>
  <div class="tooltip" v-if="is_visible">
    <div class="tip-text-container">
        <a class="tip-text" :href="`${$AppURL}/download/get_docs`" target="_blank">{{ $t('other.user_docs') }}</a>
        <div class="loading-container">
            <div class="loading animated" ref="loadingDiv"></div>
        </div>
    </div>
    <div class="close-btn" @click="is_visible = false">
        <img v-if="currentTheme.value === 'light'" class="cross" :src=Сross alt="svg">
        <img v-else class="cross" :src=CrossDark alt="svg">
    </div>
  </div>
</template>

<script>
import Сross from "../../assets/cross.svg"
import CrossDark from "../../assets/cross-dark.svg"
import { useI18n } from 'vue-i18n'

export default {
  data() {
    return {
      is_visible: true,
      Сross,
      CrossDark,
      loadingWidth: 0,
    }
  },
   setup() {
    const { t, locale } = useI18n()
    return { t, locale }
  },
  inject: ['theme'],
  computed: {
      currentTheme() {
          return this.theme?.currentTheme || 'light'
      }
  },
  mounted() {
    setTimeout(() => {
      this.is_visible = false;
    }, 20*230);
  }
}
</script>

<style scoped>

.tooltip{
    display: flex;
    justify-content: center;
    background: var(--bg-primary);
    box-shadow: 0px 0px 9px 1px var(--shadow-primary);
    border-radius: 15px;
    height: 50px;
    width: auto;

    position: fixed;
    bottom: 10px;
    right: 10px;
    z-index: 50;
}

.tip-text-container{
    padding: 8px 10px 0px 10px;
    margin: 0px;
}

.tip-text {
    font-size: 16px;
    color: var(--highlight-color);
}

.loading-container{
    margin-top: 5px; 
    height: 5px;
    width: 100%;
    border-radius: 5px;
    background-color: var(--loading-color);
}

.loading{
    height: 5px;
    border-radius: 5px;
    background-color: var(--highlight-color);
}

.cross {
    cursor: pointer;
    height: 28px;
    padding: 11px 11px 0px 0px;
}

 .loading.animated {
  width: 100%;
  transform: scaleX(0);
  transform-origin: left;
  animation: loadingProgress 4.6s linear forwards;
  will-change: transform; /* подсказка браузеру */
}

@keyframes loadingProgress {
  to { transform: scaleX(1); }
}

</style>