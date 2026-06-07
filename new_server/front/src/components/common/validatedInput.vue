<template>
    <input type="text" :placeholder="placeholder" @input="validate" v-model="inputValue" :style="{width: width}">
</template>

<script>
import { checkFloat } from '../../utils/checkers.js'

export default {
  emits: ['input-changed'],
  data(){
    return {
        inputValue: this.defaultValue,
        realValue: this.defaultValue
    }
  },
  watch: {
     defaultValue(newVal) {
      this.inputValue = newVal;
      this.realValue = newVal;
    }
  },
  props: {
    placeholder: {
      type: String,
      default: ''
    },
    fields: {
      type: String,
      default: ''
    },
    defaultValue: {
      type: String,
      default: ''
    },
    width: {
      type: String,
      default: '64px'
    }
  },
  methods: {
    validate(){
        this.inputValue = this.inputValue.replace(',','.').replace('/','.');

        if(checkFloat(this.inputValue)){
            this.realValue = this.inputValue;
        }
        else{
            this.inputValue = this.realValue;
        }

        if(this.realValue.slice(-1) === '.'){ //только в этом случае нужно отправить отдельное событие
            this.$emit('input-changed', this.fields, this.realValue.slice(0, -1));
            return;
        }

        this.$emit('input-changed', this.fields, this.realValue); //.slice(0, 2)
    }
  }
}
</script>

<style scoped>

input[type="text"] {
  height: 24px;
  width: 64px;
  margin: 2px 0px 0px 0px;
  border-radius: 10px;
  border-width: 2px;
  border-style: solid;
  border-color: var(--select-border);
  background-color: var(--bg-primary);
  color: var(--text-primary);
  padding: 2px 0 0 4px;
  font-size: 15px;
}

input[type="text"]:focus {
  border-color: var(--select-border);
}

input[type="text"]::placeholder {
  color: var(--text-input);
  font-size: 15px;
}

</style>