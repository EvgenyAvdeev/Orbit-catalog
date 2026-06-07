import './css/main.css'

import { createApp } from 'vue'
import { createI18n } from 'vue-i18n'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from "./router/router.js"
import * as echarts from 'echarts'
import 'echarts-gl'

import en from './locales/en.json'
import ru from './locales/ru.json'

window.echarts = echarts

const i18n = createI18n({
  legacy: false,
  locale: localStorage.getItem('locale') || 'ru',
  fallbackLocale: 'ru',
  messages: {
    en,
    ru
  }
})

const pinia = createPinia()
const app = createApp(App).use(router).use(i18n).use(pinia)

async function detectLocalhost() {
    if(window.location.hostname === 'orbital-catalog.auditory.ru'){
        app.config.globalProperties.$AppURL = 'https://orbital-catalog.auditory.ru'
    }
    else{
        app.config.globalProperties.$AppURL = 'http://localhost:8000'
    }
    console.log('Используется: ', app.config.globalProperties.$AppURL)
}

export function updateTitle() {
  const title = i18n.global.t('common.site_name')
  document.title = title
}

updateTitle()

const savedLocale = localStorage.getItem('locale')
if (savedLocale) {
  i18n.global.locale.value = savedLocale
}

detectLocalhost().then(() => {
    app.mount('#app')
})