<template>
    <div class="panel" :style="setPanelSizes">
        <slot></slot>
    </div>
</template>

<script>

export default {
  data(){
    return {
      minHeight: '200px'
    }
  },
  props: {
    height: {
      type: String,
      default: '500px'
    },
    width: {
      type: String,
      default: '320px'
    }
  },
  computed: {
    setPanelSizes() {
      return {
        'height': this.height,
        'width': this.width
      }
    }
  }
}
</script>

<style scoped>

.panel {
  background: var(--bg-primary);
  box-shadow: 0px 0px 9px 1px var(--shadow-primary);
  border-radius: 13px;
  width: var(width, 320px);
  height: var(height, 500px);
  flex: 1;
  padding: 15px;
  min-height: 100px;
}

</style>