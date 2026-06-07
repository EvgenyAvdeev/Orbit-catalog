<template>
    <div class="input-grid">
        <div class="input-group-and-text">
            <text class="input-description">{{ $t('map.ax') }}</text>
            <div class="input-group">
            <div class="input-and-text">
                <validatedInput :defaultValue='formData.amplitudeX.min' :placeholder="String(minMax.min_ax === undefined ? '10000' : minMax.min_ax)" 
                  fields="amplitudeX.min" @input-changed="throwEmit"></validatedInput>
            </div>
            <text class="dash">—</text>
            <div class="input-and-text">
                <validatedInput  :defaultValue='formData.amplitudeX.max' :placeholder="String(minMax.max_ax === undefined ? '100000': minMax.max_ax)" 
                  fields="amplitudeX.max" @input-changed="throwEmit"></validatedInput>
            </div>
            </div>
        </div>
        <div class="input-group-and-text">
            <text class="input-description">{{ $t('map.ay') }}</text>
            <div class="input-group">
            <div class="input-and-text">
                
                <validatedInput  :defaultValue='formData.amplitudeY.min' :placeholder="String(minMax.min_ay === undefined ? '10000': minMax.min_ay)" 
                  fields="amplitudeY.min" @input-changed="throwEmit"></validatedInput>
            </div>
            <text class="dash"> — </text>
            <div class="input-and-text">
                <validatedInput  :defaultValue='formData.amplitudeY.max' :placeholder="String(minMax.max_ay === undefined ? '100000': minMax.max_ay)" 
                  fields="amplitudeY.max" @input-changed="throwEmit"></validatedInput>
            </div>
            </div>
        </div>
        <div class="input-group-and-text">
            <text class="input-description">{{ $t('map.az') }}</text>
            <div class="input-group">
            <div class="input-and-text">
                <validatedInput  :defaultValue='formData.amplitudeZ.min' :placeholder="String(minMax.min_az === undefined ? '10000': minMax.min_az)" 
                  fields="amplitudeZ.min" @input-changed="throwEmit"></validatedInput>
            </div>
            <text class="dash">—</text>
            <div class="input-and-text">
                <validatedInput  :defaultValue='formData.amplitudeZ.max' :placeholder="String(minMax.max_az === undefined ? '100000': minMax.max_az)" 
                  fields="amplitudeZ.max" @input-changed="throwEmit"></validatedInput>
            </div>
            </div>
        </div>
        <div class="input-group-and-text">
            <text class="input-description">{{ $t('map.earth_dist') }}</text>
            <div class="input-group">
            <div class="input-and-text">
                <validatedInput :defaultValue='formData.earthDistance.min' :placeholder="String(minMax.min_dist_primary === undefined ? '10000': minMax.min_dist_primary)" 
                  fields="earthDistance.min" @input-changed="throwEmit"></validatedInput>
            </div>
            <text class="dash">—</text>
            <div class="input-and-text">
                <validatedInput :defaultValue='formData.earthDistance.max' :placeholder="String(minMax.max_dist_primary === undefined ? '100000': minMax.max_dist_primary)" 
                  fields="earthDistance.max" @input-changed="throwEmit"></validatedInput>
            </div>
            </div>
        </div>
        <div class="input-group-and-text">
            <text class="input-description">{{ $t('map.moon_dist') }}</text>
            <div class="input-group">
            <div class="input-and-text">
                <validatedInput :defaultValue='formData.moonDistance.min' :placeholder="String(minMax.min_dist_secondary === undefined ? '10000': minMax.min_dist_secondary)" 
                  fields="moonDistance.min" @input-changed="throwEmit"></validatedInput>
            </div>
            <text class="dash">—</text>
            <div class="input-and-text">
                <validatedInput :defaultValue='formData.moonDistance.max' :placeholder="String(minMax.max_dist_secondary === undefined ? '100000': minMax.max_dist_secondary)" 
                  fields="moonDistance.max" @input-changed="throwEmit"></validatedInput>
            </div>
            </div>
        </div>
        <div class="input-group-and-text">
            <text class="input-description">{{ $t('map.period') }}</text>
            <div class="input-group">
            <div class="input-and-text">
                <validatedInput :defaultValue='formData.period.min' :placeholder="String(minMax.min_t === undefined ? '12': minMax.min_t)" 
                  fields="period.min" @input-changed="throwEmit"></validatedInput>
            </div>
            <text class="dash">—</text>
            <div class="input-and-text">
                <validatedInput :defaultValue='formData.period.max' :placeholder="String(minMax.max_t === undefined ? '15': minMax.max_t)" 
                  fields="period.max" @input-changed="throwEmit"></validatedInput>
            </div>
            </div>
        </div>
        <div class="input-group-and-text">
            <text class="input-description">{{ $t('map.jacobi') }}</text>
            <div class="input-group">
            <div class="input-and-text">
                <validatedInput :defaultValue='formData.jacobiConst.min' :placeholder="String(minMax.min_cj === undefined ? '3': minMax.min_cj)" 
                  fields="jacobiConst.min" @input-changed="throwEmit"></validatedInput>
            </div>
            <text class="dash">—</text>
            <div class="input-and-text">
                <validatedInput :defaultValue='formData.jacobiConst.max' :placeholder="String(minMax.max_cj === undefined ? '3.1': minMax.max_cj)" 
                  fields="jacobiConst.max" @input-changed="throwEmit"></validatedInput>
            </div>
            </div>
        </div>
        <div class="input-group-and-text">
            <text class="input-description">{{ $t('map.stability_index') }} 1</text>
            <div class="input-group">
            <div class="input-and-text">
                <validatedInput :defaultValue='formData.stability_ind_1.min' :placeholder="String(minMax.min_stability_ind_1 === undefined ? '0': minMax.min_stability_ind_1)" 
                  fields="stability_ind_1.min" @input-changed="throwEmit"></validatedInput>
            </div>
            <text class="dash">—</text>
            <div class="input-and-text">
                <validatedInput :defaultValue='formData.stability_ind_1.max' :placeholder="String(minMax.max_stability_ind_1 === undefined ? '40': minMax.max_stability_ind_1)" 
                  fields="stability_ind_1.max" @input-changed="throwEmit"></validatedInput>
            </div>
            </div>
        </div>
        <div class="input-group-and-text">
            <text class="input-description">{{ $t('map.stability_index') }} 2</text>
            <div class="input-group">
            <div class="input-and-text">
                <validatedInput :defaultValue='formData.stability_ind_2.min' :placeholder="String(minMax.min_stability_ind_2 === undefined ? '0': minMax.min_stability_ind_2)" 
                  fields="stability_ind_2.min" @input-changed="throwEmit"></validatedInput>
            </div>
            <text class="dash">—</text>
            <div class="input-and-text">
                <validatedInput :defaultValue='formData.stability_ind_2.max' :placeholder="String(minMax.max_stability_ind_2 === undefined ? '40': minMax.max_stability_ind_2)" 
                  fields="stability_ind_2.max" @input-changed="throwEmit"></validatedInput>
            </div>
            </div>
        </div>
        <div class="input-group-and-text">
            <text class="input-description">{{ $t('map.stability_index') }} 3</text>
            <div class="input-group">
            <div class="input-and-text">
                <validatedInput :defaultValue='formData.stability_ind_3.min' :placeholder="String(minMax.min_stability_ind_3 === undefined ? '0': minMax.min_stability_ind_3)" 
                  fields="stability_ind_3.min" @input-changed="throwEmit"></validatedInput>
            </div>
            <text class="dash">—</text>
            <div class="input-and-text">
                <validatedInput :defaultValue='formData.stability_ind_3.max' :placeholder="String(minMax.max_stability_ind_3 === undefined ? '40': minMax.max_stability_ind_3)" 
                  fields="stability_ind_3.max" @input-changed="throwEmit"></validatedInput>
            </div>
            </div>
        </div>
      </div>
</template>

<script>
import validatedInput from '../common/validatedInput.vue'
import { useI18n } from 'vue-i18n'

export default {
  components: { validatedInput },
  setup() {
    const { t, locale } = useI18n()
    return { t, locale }
  },
  props: {
    formData: {
      type: Object,
      default: {},
      required: true
    },
    minMax: {
      type: Object,
      default: {},
      required: true
    }
  },
  methods: {
    throwEmit(fields, value){
      this.$emit('input-changed', fields, value);
    }
  }
}
</script>

<style scoped>

.input-grid {
  width: 370px;
  margin-top: 5px;
  display: grid;
  gap: 6px 12px;
}

.input-group-and-text {
  display: contents;
}

.input-description {
  width: 185px;
  align-content: center;
  grid-column: 1;
  color: var(--text-primary);
}

.input-group {
  grid-column: 2;
  font-size: 16px;
  display: flex;
  width: 180px;
  justify-content: center;
}

.dash{
  margin: 7px 5px 0 5px;
  color: var(--select-border);
}

</style>