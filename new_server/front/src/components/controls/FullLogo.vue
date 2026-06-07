<template>
    <div class="logo-container">
        <img class="logo" :src="logo" alt="png">
        <text class="logo-text">{{ $t('common.site_name') }}</text>
    </div>
</template>

<script>
import Logo from '../../assets/site-logo.png'
import { useI18n } from 'vue-i18n'

export default {
  data() {
    return {
      logo: Logo
    }
  },
  setup() {
    const { t, locale } = useI18n()
    return { t, locale }
  },
}
</script>

<style>
.logo-container{
    align-items: center;
	display: flex;
	justify-content: center;
    height: 60px; 
    gap: 10px;
}

.logo{
    height: 70px;
}

.logo-text{
    width: 235px;
    font-family: Inter;
    font-weight: 400;
    color: var(--text-logo);
}

.MIEM-logo{
    width: 150px;
}

</style>