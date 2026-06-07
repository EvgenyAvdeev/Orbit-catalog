import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useTimerStore = defineStore('timer', () => {
  const startTime = ref(null)
  const isRunning = ref(false)
  
  const start = () => {
    startTime.value = Date.now()
    isRunning.value = true
  }
  
  const stop = () => {
    isRunning.value = false
  }
  
  const reset = () => {
    startTime.value = null
    isRunning.value = false
  }
  
  const getElapsedTime = () => {
    if (!startTime.value) return 0
    return Date.now() - startTime.value
  }
  
  return {
    startTime,
    isRunning,
    start,
    stop,
    reset,
    getElapsedTime
  }
})