<template>
  <div class="multiple-select">
    
      <div class="selected-families-container" :style="setPanelWidth">
        <span class="selected-family"
        v-for="(option, index) in Array.from(this.selectedOptions)"
        :key="index">
          <img style="cursor: pointer;" :src="smallСross" alt="svg" @click="switchOption(option)">
          {{ option }}
        </span>
      </div>

    <div class="slot-and-selection" :style="setPanelWidth">
      <slot></slot>
      <div
        class="custom-select"
        @keydown.escape="closeSelect"
      >
        <div class="selected" :class="{ open: open }" @click="toggleOpen">
            <text v-if="selectedOptions.size == 1">{{ selectedOptions.values().next().value }}</text>
            <text v-else-if="selectedOptions.size > 1">{{ $t('other.selected_families') }}{{ selectedOptions.size }}</text>
            <text v-else>{{ $t('other.choose_option') }}</text>
          <img
            :src="arrowIcon"
            class="arrow"
            :class="{ open: open, inverted: currentTheme.value === 'dark'  }"
            alt="Стрелка"
          />
        </div>
        <div v-if="open" class="items">

          <div class="checkbox-container-top">
            <input type="checkbox" v-model="selectAllPeriodic" @change="switchPeriodic"/>
            <text style="color: var(--text-primary)">{{ $t('map.choose_periodic') }}</text>
          </div>

          <div v-for="(mainWordPart, index2) in keyWords" :key="index2">
            <div class="accordion-button" @click="hideOptions(index2)">
              <img
                :src="arrowIcon"
                class="arrow2"
                :class="{ turned: showOptions[index2], inverted: currentTheme.value === 'dark' }"
                alt="Стрелка"
              />
              <text class="section-name">{{ sectionNames[index2] }} {{ $t('map.orbits') }}</text>
            </div>
            <div v-if="showOptions[index2]">
              <div
                v-for="(option, index) in options"
                :key="index"
                @click="selectOption(option)"
                class="option-to-choose"
                :class="{ 'selected-option': isOptionSelected(option) }"
              >
                <div v-if="option.toLowerCase().includes(mainWordPart)" class="checkbox-container">
                  <input type="checkbox" :checked="isOptionSelected(option)"/>
                  {{ option }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import arrowIcon from "../../assets/arrow.svg";
import smallСross from "../../assets/small_cross.svg"
import { useI18n } from 'vue-i18n'
import { ref, computed } from 'vue'

export default {
  setup(props) {
    const { t, locale } = useI18n()

    const sectionNames = computed(() => {
      let base = [t('map.horizontal'), t('map.vertical'), t('map.halo_title')]
      if (props.currentPoint === 'L1') {
        base.push(t('map.quasiperiodic'))
      }
      return base
    })

    const keyWords = computed(() => {
      let base = [t('map.horiz'), t('map.verti'), t('map.halo')]
      if (props.currentPoint === 'L1ОПА') {
        base.push(t('map.quasiper'))
      }
      return base
    })

    const showOptions = ref([0, 0, 0])
    if (props.currentPoint === 'L1') {
      showOptions.value.push(0)
    }

    return { t, locale, sectionNames, keyWords, showOptions }
  },
  data() {
    return {
      smallСross,
      arrowIcon,
      open: false,
      selectedOptions: this.defaultOptions,
      optionHeight: 32,
      selectAllPeriodic: false
    };
  },
  props: {
    width: {
      type: String,
      default: '300px'
    },
    defaultOptions:{
      type: Set,
      default: () => new Set()
    },
    options: {
      type: Array,
      required: true,
    },
    maxVisibleOptions: {
      type: Number,
      required: false,
      default: 5, // Максимальное количество видимых опций без прокрутки
    },
    currentPoint: {
      type: String,
      default: 'L1'
    }
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
      return `${visibleOptions * this.optionHeight}px`;
    },
    setPanelWidth() {
      return {
        'width': this.width
      }
    }
  },
  watch: {
    selectedOptions: { //следим за изменениями множества и перерисовываем компонент при обновлении 
      handler() {
        this.$forceUpdate();
      },
    },
    defaultOptions: {
      handler(newOptions) {
        this.selectedOptions = new Set(newOptions);
      },
      immediate: true,
      deep: true
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
      this.switchOption(option);
      this.$emit("update:modelValue", option);
    },
    handleClickOutside(event) {
      const isClickOnCustomSelect = event.target.closest('.custom-select');
      
      if (!isClickOnCustomSelect) {
        this.closeSelect();
      }
    },
    isOptionSelected(option){
      return this.selectedOptions.has(option);
    },
    switchOption(option){
      this.selectAllPeriodic = false;

      if (this.selectedOptions.has(option)){
        this.selectedOptions.delete(option);
      }
      else {
        this.selectedOptions.add(option);
      }

      this.$emit('change-options', Array.from(this.selectedOptions));
    },
    hideOptions(option){
      this.showOptions[option] = 1-this.showOptions[option]
    },
    switchPeriodic(){
      if(this.selectAllPeriodic){
        this.selectedOptions = new Set()

        for(let i=0; i<this.options.length; ++i){
          if(this.options[i].toLowerCase().includes(this.t('map.periodi')) && !this.options[i].toLowerCase().includes(this.t('map.quasiper'))){
            this.selectedOptions.add(this.options[i])
          }
        }
      }
      else this.selectedOptions = new Set()

      this.$emit('change-options', Array.from(this.selectedOptions));
    }
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
  border: 2px solid var(--select-border);
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
  max-height: 200px;
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

.section-name{
  color: var(--text-primary);
}

.option-to-choose{
  cursor: pointer;
  font-size: 15px;
  color: var(--text-primary);
}

.option-to-choose:hover {
  background-color: var(--select-hover);
}

.selectHide {
  display: none;
}

.accordion{
  margin: 0;
  padding: 0;
}

.option-to-choose.selected-option {
  background-color: var(--select-hover);
}

.custom-select .arrow {
  transition: transform 0.3s ease;
  width: 12px;
  height: 20px;
}

.custom-select .arrow.open {
  transform: rotate(180deg);
}

.accordion-button{
  margin: 3px 2px 3px 5px;
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 15.5px;
  font-weight: 500;
}

.custom-select .arrow2 {
  transition: transform 0.3s ease;
  width: 12px;
  height: 20px;
  rotate: -90deg;
}

.custom-select .arrow2.turned {
  transform: rotate(90deg);
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

input[type="checkbox"] {
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
}

input[type="checkbox"] {
  height: 17px;
  width: 17px;
  cursor: pointer;
  margin: 0;
  padding: 0;
  flex-shrink: 0;
  border: 2px solid var(--select-border);
  border-radius: 4px;
  background-color: var(--radio-bg-color);
  position: relative;
}

input[type="checkbox"]:checked {
  background-color: var(--highlight-color);
  border-color: var(--highlight-color);
}

input[type="checkbox"]:checked::before {
  content: "✔";
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: var(--radio-inside-color);
  font-size: 14px;
  font-weight: bold;
}

.checkbox-container-top{
  display: flex;
  align-items: center;
  gap: 7px;
  padding: 5px 3px 4px 5px;
  border-bottom: 2px solid var(--select-border);
}

.checkbox-container{
  display: flex;
  align-items: center;
  gap: 7px;
  margin: 0 3px 0 5px;
  padding: 7px 0; 
}

.multiple-select{
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.slot-and-selection{
  display: flex;
  align-content: center;
  align-items: center;
  gap: 5px;
  justify-content: space-between;
}

.selected-families-container{
  display: flex;
  flex-wrap: wrap;
  gap: 2px;
}

.selected-family{
  display: inline-flex;
  align-items: center;
  color: var(--text-selected-family);
  font-weight: 500;
  font-size: 14px;
  background-color: var(--bg-selected-family);
  border-radius: 7px;
  padding: 5px 5px 5px 7px;
  gap: 5px;
}

.small-cross{
  height: 14px;
}

</style>