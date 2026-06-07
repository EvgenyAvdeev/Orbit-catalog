<template>
  <div class="panel-container" :class="{ 'hidden': isHidden, 'right': onTheRight }">
    <div class="panels">
      <slot></slot>
    </div>
    <div class="toggle" :class="{ 'right': onTheRight }" @click="togglePanel">
        <img v-if="currentTheme.value === 'light'" class="hidding-arrow" :class="{ 'rotated': isHidden, 'right': onTheRight }" :src="HiddingArrow" alt="svg">
        <img v-else class="hidding-arrow" :class="{ 'rotated': isHidden, 'right': onTheRight }" :src="HiddingArrowDark" alt="svg">
    </div>
  </div>
</template>

<script>
import HiddingArrow from "../../assets/hidding-arrow.svg"
import HiddingArrowDark from "../../assets/hidding-arrow-dark.svg"

export default {
  data() {
    return {
      isHidden: false,
      HiddingArrow,
      HiddingArrowDark
    }
  },
  props: {
    onTheRight: {
      type: Boolean,
      default: false
    }
  },
  inject: ['theme'],
  computed: {
    currentTheme() {
        return this.theme?.currentTheme || 'light'
    }
  },
  methods: {
    togglePanel(){
      this.isHidden = !this.isHidden;

      if(this.onTheRight) return;

      this.$emit('panel-toggle', this.isHidden);
    }
  }
}

</script>

<style scoped>

.panel-container {
  position: fixed;
  top: 50.5%;
  display: flex;
  z-index: 100;
  transition: transform 0.2s ease;
  margin: 25px;

  left: 0;
  transform: translateY(-50%) translateX(47px);
} 

.panel-container.right {
  left: unset;
  right: 30px;
  transform: translateY(-50%) translateX(47px);
} 

.panels{
  display: grid;
  flex-direction: column;
  gap: 12px;
}

.panel-container.hidden {
  transform: translateY(-50%) translateX(calc(-1 * (100% - 30px)));
}

.panel-container.hidden.right {
  transform: translateY(-50%) translateX(calc(1 * (100% + 60px)));
}

.toggle {
  position: absolute;
  right: -55px;
  width: 45px;
  height: 45px;
  background: var(--bg-primary);
  box-shadow: 0px 0px 9px 1px var(--shadow-primary);
  border-radius: 13px;
  margin-left: 12px;
  cursor: pointer;
  align-self: top;
  outline: none;
  border:none;
}

.toggle.right {
  right: 380px;
}

.hidding-arrow {
  height: 30px;
  padding: 7px 14px 7px 12px;
  display: inline-block;
  transition: transform 0.2s ease;
  font-size: 24px;
}

.hidding-arrow.right {
  rotate: 180deg;
}

.hidding-arrow.rotated.right {
  transform: rotate(-180deg);
}

.hidding-arrow.rotated {
  transform: rotate(180deg);
}

</style>