<template>
    <nav class="sidebar">
      <div class="icons-container">
        <router-link  v-for="page_number in 4" :to="getPath(page_number)">
          <img v-if="currentTheme.value === 'light'" class="toolbar-icon" :src="getIconPath(page_number, '')" :alt="`icon-${page_number}`">
          <img v-else class="toolbar-icon" :src="getIconPath(page_number, '-dark')" :alt="`icon-${page_number}`">
        </router-link>
      
        <div class="bottom-buttons">
          <!--<downloadFiles class="download-button"/> --> 
          <LanguageToggle class="language-toggle"/>
          <ThemeToggle class="theme-toggle"/>
        </div>
      </div>
    </nav>
</template>

<script>
import ThemeToggle from './ThemeToggle.vue'
import LanguageToggle from './LanguageToggle.vue'
import downloadFiles from '../common/downloadFiles.vue'

export default {
  components: { ThemeToggle, LanguageToggle, downloadFiles },
  methods: {
    getPath(page_number){
      const pagePaths = {
        1: '/map',
        2: '/orbit',
        3: '/orbit_family',
        4: '/cj',
        5: '/families'
      };
      return pagePaths[page_number];
    },
    getIconPath(page_number, postfix) {
      const isFamiliesRoute = page_number === 5 && this.$route.path.startsWith('/families');
      const if_active = this.$route.name === `Page${page_number}` || isFamiliesRoute ? 'active' : 'non-active';
      return new URL(`../../assets/${if_active}/icon-${page_number}${postfix}.svg`, import.meta.url).href; 
    }
  },
  inject: ['theme'],
  computed: {
    currentTheme() {
      return this.theme?.currentTheme || 'light'
    }
  },
  watch: {
      'theme.currentTheme': {
      handler() {
        
      },
      deep: true,
      immediate: true
    }
  }
}
</script>

<style>
.sidebar {
  background: var(--bg-primary);
  width: 60px;
  display: flex;
  justify-content: center;
  height: 100%;
  box-shadow: 0px 10px 10px 2px var(--shadow-primary);
  z-index: 1000;
}

.icons-container{
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.toolbar-icon{
  width: 50px;
  margin: 2px;
  cursor: pointer;
}

.bottom-buttons{
  position: absolute;
  bottom: 0px;
  left: 0px;

  display: flex;
  flex-direction: column;
  gap: 10px 0;

  padding: 8.5px;
}

</style>