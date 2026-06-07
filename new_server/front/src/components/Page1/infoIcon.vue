<template>
  <div class="common-container">
    <img v-if="currentTheme.value === 'light'" @mouseover="showTooltip" @mouseleave="hideTooltip" :src="infoIcon" class="info-icon">
    <img v-else @mouseover="showTooltip" @mouseleave="hideTooltip" :src="infoIconDark" class="info-icon">
    
    <div v-if="showTip" class="container-tip" :class="{ 'active': showTip }">
      <text style="color: var(--text-primary)">{{ $t('map.info_icon_text') }}</text>
    </div>
  </div>
</template>

<script>

import infoIcon from '../../assets/info.svg'
import infoIconDark from '../../assets/info-dark.svg'

export default {
  data(){
    return{
        showTip: false,
        infoIcon,
        infoIconDark
    };
  },
  inject: ['theme'],
  computed: {
    currentTheme() {
        return this.theme?.currentTheme || 'light'
    }
  },
  methods: {
    showTooltip() {
      this.showTip = true;
    },
    hideTooltip() {
      this.showTip = false;
    },
  },
};
</script>

<style scoped>

.common-container {
  position: relative;
  display: inline-block;
}

.info-icon {
  margin-top: 4px;
  cursor: pointer;
  width: 22px;
  height: 22px;
}

.container-tip {
  width: 210px;
  height: auto;
  background: var(--bg-primary);
  box-shadow: 0px 0px 10px 2px var(--shadow-primary);
  border-radius: 10px;
  padding: 7px;
  position: absolute;
  top: 100%;
  left: -204px;
  z-index: 150;
  font-size: 14px;
}

</style>