<template>
  <div class="tooltip" v-if="is_visible">
    <div class="tip-text-container">
        <p class="tip-text">{{ $t('map.tip1_text1') }}</p>
        <p class="tip-text">{{ $t('map.tip1_text2') }}</p>
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
      CrossDark
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
    top: 70px;
    right: 165px;
    z-index: 50;
}

.tip-text-container{
    padding: 6px 20px 0px 10px;
    margin: 0px;
}

.tip-text {
    font-size: 16px;
    padding: 0px;
    margin: 0px;
    color: var(--text-primary);
}

.cross {
    cursor: pointer;
    height: 28px;
    padding: 11px 11px 0px 0px;
}

</style>