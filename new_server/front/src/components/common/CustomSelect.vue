<template>
  <div
    class="custom-select"
    :style="setPanelWidth"
    @blur="closeSelect"
    @keydown.escape="closeSelect"
  >
    <div class="selected" :class="{ 
          open: open, 
        }" @click="toggleOpen">
      {{ modelValue || $t('other.choose_option') }}
      <img
        :src="arrowIcon"
        class="arrow"
        :class="{ open: open, inverted: currentTheme.value === 'dark'  }"
        alt="Стрелка"
      />
    </div>
    <transition name="fade">
      <div
        v-if="open"
        class="items"
        :style="{ height: computedHeight }"
      >
        <div
          v-for="(option, index) in options"
          :key="index"
          @click="selectOption(option)"
          :class="{ 'selected-option': option === modelValue }"
        >
          {{ option }}
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import arrowIcon from "../../assets/arrow.svg";
export default {
  data() {
    return {
      open: false,
      arrowIcon,
      optionHeight: 32
    };
  },
  props: {
    width: {
      type: String,
      default: '300px'
    },
    options: {
      type: Array,
      required: true,
    },
    modelValue: {
      type: String,
      required: false,
      default: '',
    },
    maxVisibleOptions: {
      type: Number,
      required: false,
      default: 5, // Максимальное количество видимых опций без прокрутки
    },
  },
  inject: ['theme'],
  computed: {
    currentTheme() {
      return this.theme?.currentTheme || 'light'
    },
    computedHeight() {
      const visibleOptions = Math.min(
        this.options.length,
        this.maxVisibleOptions
      );
      return `${visibleOptions * this.optionHeight + 1.5}px`;
    },
    setPanelWidth() {
      return {
        'width': this.width
      }
    }
  },
  methods: {
    toggleOpen() {
      this.open = !this.open;
    },
    closeSelect() {
      this.open = false;
    },
    selectOption(option) {
      this.open = false;
      this.$emit("update:modelValue", option);
    },
    handleClickOutside(event) {
      const selectElement = this.$el;
      if (!selectElement.contains(event.target)) {
        this.closeSelect();
      }
    },
  },
  mounted() {
    document.addEventListener("click", this.handleClickOutside);
  },
  beforeUnmount() {
    document.removeEventListener("click", this.handleClickOutside);
  },
};
</script>

<style scoped>
.custom-select {
  position: relative;
  width: 300px;
  text-align: left;
  outline: none;
  padding: 5px 15px 5px 10px; /* Отступ для стрелки */
  border: 2px solid  var(--select-border);
  border-radius: 10px;
  cursor: pointer;
  user-select: none;
  background-color: var(--bg-primary);
  transition: height 0.3s ease;
}

.custom-select .selected {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
  font-size: 15px;
  color: var(--text-primary);
}

.custom-select .items {
  min-height: 32.5px;
  width: calc(100% + 1px);
  overflow: hidden;
  border-radius: 10px;
  overflow-y: auto;
  border: 2px solid var(--select-border);
  position: absolute;
  background-color: var(--bg-primary);
  margin-top: 5px;
  left: -2px;
  right: 0;
  z-index: 25;
  box-shadow: 0 4px 8px var(--select-shadow);
  transition: max-height 0.3s ease, opacity 0.3s ease;
  scrollbar-color: var(--scrollbar) transparent;
}

.custom-select .items div {
  padding: 7px;
  cursor: pointer;
  font-size: 15px;
  color: var(--text-primary);
}

.custom-select .items div:hover {
  background-color: var(--select-hover);
}

.selectHide {
  display: none;
}

.custom-select .items div.selected-option {
  background-color: var(--select-hover);
}

.custom-select .arrow {
  transition: transform 0.3s ease;
  width: 12px;
  height: 20px;
}

.custom-select.arrow.open {
  transform: rotate(180deg);
}

.inverted{
  filter: invert(1);
}

/* Анимация для перехода */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
.fade-enter-to,
.fade-leave-from {
  opacity: 1;
}

</style>