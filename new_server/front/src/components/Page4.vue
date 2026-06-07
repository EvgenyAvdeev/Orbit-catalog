<template>
  <HiddingPanel @panel-toggle="handlePanelToggle">
    <Panel height="500px">

      <Accordion width="100%">
        <template #header>
          <h3>{{ $t('cj.header') }}</h3>
        </template>

        <template #content>
          <div class="horizontal-group">
            <text class="text-description">{{ $t('cj.cj_constant') }}</text>
            <validatedInput :defaultValue='formData.cj' placeholder="2.9" fields="cj"  @input-changed="updateFormdata"></validatedInput>
          </div>

          <div class="horizontal-group">
            <text class="text-description">{{ $t('cj.inaccuracy') }}</text>
            <validatedInput :defaultValue='formData.rate' placeholder="0.001" fields="rate"  @input-changed="updateFormdata"></validatedInput>
          </div>

          <div class="horizontal-group">
            <text class="text-description">{{ $t('common.point') }}</text>
              <div class="inputs">
                <p>
                  <input type="radio" name="point" value="L1" checked v-model="formData.point"/>{{ $t('common.system') }} L1
                </p>
                <p>
                  <input type="radio" name="point" value="L2" v-model="formData.point"/>{{ $t('common.system') }} L2
                </p>
              </div>
          </div>

          <div class="horizontal-group">
            <text class="text-description">{{ $t('common.plane') }}</text>
            <CustomSelect
              v-model="formData.plane"
              :options="planeOptions"
              width="185px"
            ></CustomSelect>
          </div>
        </template>
      </Accordion>

      <Accordion width="100%">
        <template #header>
          <h3>{{ $t('common.graph_settings') }}</h3>
        </template>
        
        <template #content>
          <div class="horizontal-group" style="padding-bottom: 5px; align-items: center;">
            <text style="color: var(--text-primary)">{{ $t('common.palette') }}</text>
            <GradientSelect v-model="graphSettings.gradientName"/>
          </div>

          <div class="vertical-group">
            <text class="text-description">{{ $t('common.color_param') }}</text>
            <CustomSelect
              v-model="graphSettings.parameter"
              :options="Object.keys(highlightionParameters)"
              width="290px"
            ></CustomSelect>
          </div>
        </template>
      </Accordion>

      <input type="button" :value="$t('common.build')" @click="fetchData(true)" :disabled="isDisabled()">
      </Panel>
  </HiddingPanel>

  <div class="page-content">
    <Graph 
      :data="fetchedData" 
      :shift=labelsShift
      :gradientName=graphSettings.gradientName
      :selectedPoints="graphSettings.selectedPoints"
      width="100%" 
      height="100%"
      :x-axes-name="getAxisNames()[0]"
      :y-axes-name="getAxisNames()[1]"
      :show-line="false"
      @point-clicked="updateOnClickData"
    />
  </div>

  <Notification :newState="pageState"></Notification>
  <transferPopUp :popUp="popUp" :currPageNumber="4"></transferPopUp>
</template>

<script>
import HiddingPanel from './common/HiddingPanel.vue'
import Panel from './common/Panel.vue'
import Graph from './common/Graph.vue'
import CustomSelect from './common/CustomSelect.vue'
import Notification from './common/Notification.vue'
import Accordion from './common/Accordion.vue'
import GradientSelect from './common/GradientSelect.vue'
import validatedInput from './common/validatedInput.vue'
import transferPopUp from './common/transferPopUp.vue'
import { checkGradient, checkIncludes, checkFloat, checkPoints, checkIncludesReversed } from '../utils/checkers.js'
import { processPointsForCJPoincare } from "../utils/dataProcessing.js"
import { getFor4thPage } from "../utils/dataProcForTransfers.js"
import { PoincareTemplateArray, OrbitTemplate } from '@/utils/validation.js';
import { useOrbitNames } from '../constants/familiesAndTags.js'
import { z } from 'zod';
import { useI18n } from 'vue-i18n'
import { computed } from 'vue'

export default {
  components: { HiddingPanel, Panel, Graph, CustomSelect, Notification, Accordion, GradientSelect, validatedInput, transferPopUp },
  setup() {
    const { t, locale } = useI18n()

    const highlightionParameters = computed(() => ({
        [t('parameters.initial_x')]: 'x',
        [t('parameters.initial_y')]: 'y',
        [t('parameters.initial_z')]: 'z',
        [t('parameters.ax')]: 'ax',
        [t('parameters.ay')]: 'ay',
        [t('parameters.az')]: 'az',
        [t('parameters.earth_dist')]: 'dist_primary',
        [t('parameters.moon_dist')]: 'dist_secondary',
        [t('parameters.initial_speed_x')]: 'vx',
        [t('parameters.initial_speed_y')]: 'vy',
        [t('parameters.initial_speed_z')]: 'vz',
        [t('parameters.abs_v')]: "abs_v",
    }))

    const { tagToFamilyName, familyToTagL1, familyToTagL2 } = useOrbitNames()

    return { t, locale, highlightionParameters, tagToFamilyName }
  },
  data() {
    return {
      planeOptions: [
        "x = 0",
        "y = 0",
        "z = 0",
        "vx = 0",
        "vy = 0",
        "vz = 0"
      ],
      fetchedData: [[],[],[]],
      popUp: undefined,
      formData: {
        point: 'L1',
        plane: 'x = 0',
        cj: '2.958',
        rate: '0.0001'
      },
      graphSettings: {
        gradientName: 'Winter',
        parameter: this.t('parameters.initial_x'),
        selected_points: [],
        selectedPoints: []
      },
      labelsShift: 360,
      pageState: 'OK',
      canUpdateURL: true
    }
  },
  watch: {
    '$route.query': {
      handler() {
        this.loadParams();
      },
      deep: true,
      immediate: true
    },
    'formData': {
      handler() {
        this.updateUrl();
      },
      immediate: true,
      deep: true
    },
    'graphSettings': {
      handler() {
        this.updateUrl();
      },
      immediate: true,
      deep: true
    },
    'highlightionParameters': {
      handler(newValue, oldValue) {
        let param_tag = oldValue[this.graphSettings.parameter];

        let keys = Object.keys(newValue);
        for(let i = 0; i<keys.length; ++i){
          if(newValue[keys[i]] === param_tag){
            this.graphSettings.parameter = keys[i];
            break;
          }
        }
      }
    }
  },
  mounted(){
    this.drawGraphs();
  },
  methods: {
    updateUrl() {
      if(!this.canUpdateURL) return
      this.canUpdateURL = false

      var common = {};
      var specific = {};

      specific.graph = this.selectedType,
      specific.point = this.formData.point,
      specific.plane = this.formData.plane;
      specific.cj = this.formData.cj;
      specific.rate = this.formData.rate;
      specific.gradient = this.graphSettings.gradientName;
      specific.color_param = this.highlightionParameters[this.graphSettings.parameter];

      if(this.graphSettings.selectedPoints.length>0){

        var points = this.graphSettings.selectedPoints;
        var preparedPoints = [];
        for(var i = 0; i<points.length; ++i){
          preparedPoints.push(`[${points[i].join(';')}]`);
        }
        specific.selected_points = `[${preparedPoints.join(';')}]`
      }

      this.$router.replace({
        query: {
          ...common,
          ...specific
        }
      })

      setTimeout(() => this.canUpdateURL = true, 0);
    },
    loadParams() {
      if(!this.canUpdateURL) return

      const { point, plane, cj, rate, gradient, color_param, selected_points } = this.$route.query;

      this.formData.point = checkIncludes(point, ['L1', 'L2']);
      this.formData.plane = checkIncludes(plane, this.planeOptions, 1);
      this.graphSettings.parameter = checkIncludesReversed(color_param, this.highlightionParameters);
      this.graphSettings.gradientName = checkGradient(gradient);
      this.graphSettings.selectedPoints = checkPoints(selected_points);

      if(cj !== '' & checkFloat(cj)) {
        this.formData.cj = cj;
      }

      if(rate !== '' & checkFloat(rate)) {
        this.formData.rate = rate;
      }

      if(this.$route.fullPath === '/cj') this.updateUrl();
    },
    handlePanelToggle(isHidden){ //следим за движением панели
      if(isHidden){
        this.labelsShift = 0;
      }
      else{
        this.labelsShift = 360;
      }
    },
    getAxisNames(){ //получаем подписи осей
      var plane = this.formData.plane;
      if(plane == 'x = 0'){ return ['Y', 'Z']; }
      if(plane == 'y = 0'){ return ['X', 'Z']; }
      if(plane == 'z = 0'){ return ['X', 'Y']; }
      if(plane == 'vx = 0'){ return ['Vy', 'Vz']; }
      if(plane == 'vy = 0'){ return ['Vx', 'Vz']; }
      if(plane == 'vz = 0'){ return ['Vx', 'Vy']; }
      return ['', ''];
    },
    isDisabled(){ //блокируем кнопку, пока поля не заполнены
      if(this.formData.plane === '' || this.formData.cj === '' || this.formData.rate === '' || this.graphSettings.parameter === undefined){
        return true;
      }
      return false;
    },
    getFilters(){ //фильтр для запроса
      return `get_by_cj?filter_groups=[{"log_op":"NONE", "filters":[{"field":"lib_point", "op":"==", "value":"${this.formData.point}"},
      {"field":"plane", "op":"==", "value":"${this.formData.plane}"},{"field":"cj", "op":"==", "value":${this.formData.cj}}]}]&rate=${this.formData.rate}`
    },
    async fetchData(resetSelectedPoints=false) { //запрос
      if(resetSelectedPoints) this.graphSettings.selectedPoints = []

      this.pageState = 'Loading';
      try {
        const filter = this.getFilters();
        const response = await fetch(`${this.$AppURL}/orbit_poincare_view/${filter}`);

        if (!response.ok) {
          throw new Error(`статус запроса: ${response.status}`);
        }

        let parameter = this.highlightionParameters[this.graphSettings.parameter];
        const data = await response.json();
        this.fetchedData = PoincareTemplateArray.parse(data);
        this.dataForTransfer = getFor4thPage(this.fetchedData, this.formData.plane);
        this.fetchedData = processPointsForCJPoincare(this.fetchedData, this.formData.plane, parameter);

        if(this.fetchedData[0].length === 0){
          this.pageState = 'noPointsError';
        }
        else{
          this.pageState = 'OK';
        }
      } 
      catch (error) {
        if (error instanceof z.ZodError) {
          this.pageState = 'ValidError';
          console.error('Ошибка валидации данных:', error.errors);
        } 
        else {
          this.pageState = 'unknownError';
          console.error('Произошла ошибка:', error);
        }
      }
    },
    updateFormdata(field, newValue){
      this.formData[field] = newValue;
    },
    drawGraphs(){
      if(this.isDisabled()) return;

      this.fetchData()
    },
    async updateOnClickData(newPopUpData){
      this.pageState = 'OK';
      var { x, z } = this.dataForTransfer[`${newPopUpData.dataX}:${newPopUpData.dataY}`];

      try {
        let response = await fetch(`${this.$AppURL}/orbit_view/get_nearest_orbit?x=${x}&z=${z}`);
        
        if (!response.ok) {
          throw new Error(`статус запроса: ${response.status}`);
        }
      
        let data = await response.json();
        var family_tag = OrbitTemplate.parse(data)['family_tag'];

        newPopUpData = { ...newPopUpData, ...OrbitTemplate.parse(data) }
      } 
      catch (error) {
        if (error instanceof z.ZodError) {
          this.pageState = 'ValidError';
          console.error('Ошибка валидации данных:', error.errors);
        } 
        else {
          this.pageState = 'unknownError';
          console.error('Произошла ошибка:', error);
        }
      }

      this.popUp = { ...newPopUpData, point: this.formData.point, family_tag: family_tag };
    }
  }
}
</script>

<style scoped>

h3 {
  margin: 0;
  padding: 0;
  font-size: 20px;
  color: var(--text-primary);
}

.horizontal-group {
  padding-bottom: 7px;
  display: flex;
  justify-content: space-between;
  gap: 7px; 
}

.vertical-group {
  padding-bottom: 5px;
  display: flex;
  flex-direction: column;
  gap: 0px;
}

.text-description{
  font-size: 16px;
  margin: 5px 0;
  color: var(--text-primary);
}

.inputs {
  font-size: 17px;
  padding: 0;
}

input[type="radio"],
input[type="checkbox"] {
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
}

input[type="radio"] {
  cursor: pointer;
  height: 16px;
  width: 16px;
  margin: 0px 7px 0px 0px;
  border: 2px solid var(--select-border);
  border-radius: 50%;
  background-color: var(--radio-bg-color);
  position: relative;
}

input[type="radio"]:checked {
  background-color: var(--highlight-color);
  border-color: var(--highlight-color);
}

input[type="radio"]:checked::before {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 6px;
  height: 6px;
  background-color: var(--radio-inside-color);
  border-radius: 50%;
}

.inputs p {
  margin: 5px 43px 5px 0px;
  width: 170px;
  display: flex;
  align-items: center;
  color: var(--text-primary);
}

input[type="text"] {
  height: 24px;
  width: 64px;
  margin: 2px 100px 0px 0px;
  border-radius: 10px;
  border-width: 2px;
  border-style: solid;
  color: var(--text-primary);
  border-color: var(--select-border);
  background-color: var(--bg-primary);
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

input[type="button"] {
  width: 220px;
  height: 42px;
  cursor: pointer;
  background: var(--highlight-color);
  border-radius: 10px;
  border: none;
  margin-left: 50px;
  bottom: 10px;
  position: absolute;
  color: var(--text-button-able);
  box-shadow: 0px 0px 10px 10px var(--highlight-shadow);
  font-size: 17px;
}

input:disabled[type="button"] {
  background: var(--button-disabled);
  color: var(--text-button-disable);
}

.page-content {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.graph{
  display: block;
  width: 100%;
}

</style>