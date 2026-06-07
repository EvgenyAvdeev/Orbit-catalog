import { ref, readonly } from 'vue'

export function useTheme() {
  const currentTheme = ref('light')
  
  const themeValues = ref({
    light: {
      '--bg-primary': '#fff',
      '--select-border': '#4F4F4F',
      '--text-primary': '#000',
      '--scrollbar': '#c1c1c1',
      '--select-hover': '#e1ebff',
      '--text-selected-family': '#333333',
      '--bg-selected-family': '#D8E5FF',
      '--select-shadow': 'rgba(0, 0, 0, 0.1)',
      '--selected-gradient': '#000',
      '--shadow-primary': '#A9C5FF',
      '--text-orbit-info': '#4C4C4C',
      '--text-logo': '#2a6ced',
      '--text-input': '#C2C2C2',
      '--highlight-color': '#2A6CED',
      '--highlight-shadow': '#ffffff',
      '--radio-bg-color': '#ffffff',
      '--radio-inside-color': '#ffffff',
      '--button-disabled': '#94B5F6',
      '--text-button-able': '#ffffff',
      '--text-button-disable': '#ffffff',
      '--theme-toggle-border': '#c1c1c1',
      '--selector-color-inactive': '#EFEFEF',
      '--selector-color-active': '#CDDEFF',
      '--download-button-bg': '#e2e2e2',

      '--grid-color': 'rgba(195, 195, 195, 1)',
      '--minor-grid-color': 'rgba(234, 234, 234, 1)',
      '--axis-color': '#667',
      '--labels-color': '#667',
      '--labels-shadow-color': '#ffffff',
      '--icons-color': '#667',
      '--broucke-lines-color': '#333333',
      '--graphs-border-color': '#000000',
      '--loading-color': '#cccccc',
      '--line-color': 'lightgray'
    },
    dark: {
      '--bg-primary': '#1a1a1a',
      '--bg-selected-family': '#2d2d2d',
      '--text-primary': '#d7d7d7',
      '--text-selected-family': '#d7d7d7',
      '--text-orbit-info': '#a5a5a5',
      '--text-logo': '#6b8cff',
      '--select-border': '#404040',
      '--scrollbar': '#404040',
      '--select-hover': '#363636',
      '--select-shadow': 'rgba(0, 0, 0, 0.4)',
      '--selected-gradient': '#d7d7d7',
      '--shadow-primary': 'rgba(0, 145, 255, 0.2)',
      '--text-input': '#414141',
      '--highlight-color': '#2a6ced',
      '--highlight-shadow': '#2d2d2d',
      '--radio-bg-color': '#252525',
      '--radio-inside-color': '#ffffff',
      '--button-disabled': '#536996ff',
      '--text-button-able': '#ffffff',
      '--text-button-disable': '#a4a4a4ff',
      '--theme-toggle-border': '#404040',
      '--selector-color-inactive': '#4E4E4E',
      '--selector-color-active': '#92B3F7',
      '--download-button-bg': '#363636',

      '--grid-color': 'rgba(77, 77, 77, 1)',
      '--minor-grid-color': 'rgba(37, 37, 37, 1)',
      '--axis-color': 'rgba(152, 152, 152, 1), 1)',
      '--labels-color': 'rgba(191, 191, 191, 1)',
      '--labels-shadow-color': '#1a1a1a',
      '--icons-color': 'rgba(169, 169, 169, 1)',
      '--broucke-lines-color': '#565656ff',
      '--graphs-border-color': '#d5d5d5ff',
      '--loading-color': '#cccccc',
      '--line-color': '#575757'
    }
  })

  const updateCSSVariables = (theme) => {
    const values = themeValues.value[theme]
    Object.entries(values).forEach(([key, value]) => {
      document.documentElement.style.setProperty(key, value)
    })
  }

  const toggleTheme = () => {
    currentTheme.value = currentTheme.value === 'light' ? 'dark' : 'light'
    updateCSSVariables(currentTheme.value)
    localStorage.setItem('theme', currentTheme.value)
  }

  const setTheme = (theme) => {
    if (['light', 'dark'].includes(theme)) {
      currentTheme.value = theme
      updateCSSVariables(theme)
      localStorage.setItem('theme', theme)
    }
  }

  const initializeTheme = () => {
    const savedTheme = localStorage.getItem('theme')
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
    
   if (savedTheme) {
      setTheme(savedTheme)
    } else if (systemPrefersDark) {
      setTheme('dark')
    } else {
      updateCSSVariables(currentTheme.value)
    }
  }

  initializeTheme()

  return {
    currentTheme: readonly(currentTheme),
    toggleTheme,
    setTheme,
    getCurrentValues: () => themeValues.value[currentTheme.value]
  }
}