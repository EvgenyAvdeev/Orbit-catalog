<template>
    <div class="header">
        <FullLogo/>
        <img v-if="currentTheme.value === 'light'" class="MIEM-logo" :src=MIEM_logo alt="MIEM-logo">
        <img v-else class="MIEM-logo" :src=MIEM_logo_dark alt="MIEM-logo">
    </div>
</template>

<script>
import FullLogo from './FullLogo.vue'
import MIEM_logo from '../../assets/MIEM-logo.svg'
import MIEM_logo_dark from '../../assets/MIEM-logo-dark.svg'

export default {
  components: { FullLogo },
  data() {
    return {
      MIEM_logo,
      MIEM_logo_dark
    }
  },
  inject: ['theme'],
  computed: {
    currentTheme() {
        return this.theme?.currentTheme || 'light'
    }
  }
}
</script>

<style>
.header{
	display: flex;
	justify-content: space-between;
  background: var(--bg-primary);
  box-shadow: 0px 0px 10px 2px var(--shadow-primary);
  padding: 0px 60px;
  margin: 0;
  height: 60px;
  z-index: 1000;
}

</style>