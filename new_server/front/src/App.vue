<template>
  <div class="main-container">
    <Header/>
    <div class="sidebar-and-content">
      <SideBar/>
      <div class="content">
        <router-view></router-view>
      </div>
    </div>
  </div>

  <TipDocumentation/>
</template>

<script setup>
import { provide } from 'vue'
import SideBar from './components/controls/SideBar.vue'
import Header from './components/controls/Header.vue'
import TipDocumentation from './components/common/TipDocumentation.vue'
import { useTheme } from './setTheme.js'

const theme = useTheme()
provide('theme', theme)

</script>

<style scoped>
* {
  transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
}

.main-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.sidebar-and-content {
  display: flex;
  flex: 1;
  min-height: 0;
}

.content {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  overflow-x: hidden;
  display: flex;
  justify-content: center;
}

</style>