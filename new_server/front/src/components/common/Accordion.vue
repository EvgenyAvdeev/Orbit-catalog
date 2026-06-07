<template>
    <div class="container" :style="setSize">
        <div class="arrow-and-text" @click="toggleAccordion">
            <img
                :src="arrowIcon"
                class="arrow"
                :class="{ open: isOpen, inverted: currentTheme.value === 'dark' }"
                alt="Стрелка"
            />
            <slot name="header">
            </slot>
        </div>

        <div class="content-wrapper" :class="{ hidden: !isOpen }">
            <slot name="content"></slot>
        </div>
  </div>
</template>

<script setup>
import { ref, inject, computed } from 'vue'
import arrowIcon from "../../assets/arrow.svg";

const props = defineProps({
    width: {
        type: String,
        default: '200px'
    }
})

const isOpen = ref(true)

const theme = inject('theme')
const currentTheme = computed(() => theme?.currentTheme || 'light')

const setSize = computed(() => ({
    'width': props.width
}))

const toggleAccordion = () => {
    isOpen.value = !isOpen.value
}
</script>

<style scoped>
.arrow-and-text{
    cursor: pointer;
    display: flex;
    justify-content: left; 
    align-items: center;
    align-content: center;
    gap: 7px;
    margin-bottom: 10px;
}

.content-wrapper.hidden {
    display: none;
}

.arrow {
    width: 15px;
    transition: transform 0.3s ease;
    rotate: -90deg;
}

.arrow.open {
    transform: rotate(90deg);
}

.arrow.inverted{
    filter: invert(1);
}
</style>