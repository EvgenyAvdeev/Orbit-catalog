<template>
  <HiddingPanel @panel-toggle="handlePanelToggle">
    <Panel :height="PanelHeight" width="336px" class="panel-with-scroll">

      <Accordion width="320px">
        <template #header>
          <h3>{{ $t('orbit_family.header') }}</h3>
        </template>
        
        <template #content>
          <div class="vertical-group">
            <text class="text-description">{{ $t('common.graph_type') }}</text>
            <CustomSelect
              v-model="selectedType"
              :options="Object.keys(graphTypeOptions)"
              width="290px"
            ></CustomSelect>
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

          <div class="vertical-group">
            <text class="text-description">{{ $t('common.family') }}</text>
            <CustomSelect v-if="formData.point==='L1'"
              v-model="formData.selectedFamily"
              :options="Object.keys(familyToTagL1)"
              width="290px"
            ></CustomSelect>
            <CustomSelect v-else
              v-model="formData.selectedFamily"
              :options="Object.keys(familyToTagL2)"
              width="290px"
            ></CustomSelect>
          </div>

          <div v-if="selectedType === t('orbit_family.params')" class="vertical-group">
            <text class="text-description">{{ $t('orbit_family.horizontal_param') }}</text>
            <CustomSelect
              v-model="formData.horizontal"
              :options="Object.keys(axesOptions)"
              width="290px"
            ></CustomSelect>
          </div>

          <div v-if="selectedType === t('orbit_family.params')" class="vertical-group">
            <text class="text-description">{{ $t('orbit_family.vertical_param') }}</text>
            <CustomSelect
              v-model="formData.vertical"
              :options="Object.keys(axesOptions)"
              width="290px"
            ></CustomSelect>
          </div>
        </template>
      </Accordion>

      <Accordion width="320px" style="padding: 10px 0 100px 0">
        <template #header>
          <h3>{{ $t('common.graph_settings') }}</h3>
        </template>
        
        <template #content>
          <div class="horizontal-group" style="padding-bottom: 5px; align-items: center;">
            <text style="color: var(--text-primary)">{{ $t('common.palette') }}</text>
            <GradientSelect v-model="graphSettings.gradientName"/>
          </div>

          <div class="vertical-group" style="margin-bottom: 110px">
            <text class="text-description">{{ $t('common.color_param') }}</text>
            <CustomSelect
              v-model="graphSettings.parameter"
              :options="Object.keys(axesOptions)"
              width="290px"
            ></CustomSelect>
          </div>
        </template>
      </Accordion>

      <input v-if="selectedType === t('orbit_family.params')" type="button" :value="$t('common.build')" @click="fetchParams(true)">
      <input v-else type="button" :value="$t('common.build')" @click="fetchBroucke(true)">
    </Panel>
  </HiddingPanel>

  <div v-if="selectedType === t('orbit_family.params')" class="page-content">
    <Graph
      :data="fetchedData" 
      :shift=labelsShift
      :gradientName=graphSettings.gradientName
      :selectedPoints="graphSettings.selectedPoints"
      width="100%" 
      height="100%"
      :x-axes-name="this.axesOptions[this.formData.horizontal]"
      :y-axes-name="this.axesOptions[this.formData.vertical]"
      @point-clicked="updateOnClickData"
    />
  </div>

  <div v-if="selectedType === t('orbit_family.broucke')" class="page-content">
    <BrouckeDiagram
      :data="fetchedData" 
      :shift=labelsShift
      :gradientName=graphSettings.gradientName
      width="100%" 
      height="100%"
      @point-clicked="updateOnClickData"
    />
  </div>

   <Notification :newState="pageState"></Notification>
   <transferPopUp :popUp="popUp" :currPageNumber="3"></transferPopUp>
</template>

<script>
import HiddingPanel from './common/HiddingPanel.vue'
import Panel from './common/Panel.vue'
import CustomSelect from './common/CustomSelect.vue'
import Graph from './common/Graph.vue'
import BrouckeDiagram from './common/BrouckeDiagram.vue'
import Accordion from './common/Accordion.vue'
import GradientSelect from './common/GradientSelect.vue'
import Notification from './common/Notification.vue'
import transferPopUp from './common/transferPopUp.vue'
import { checkGradient, checkIncludes, checkPoints, checkIncludesReversed } from '../utils/checkers.js'
import { useOrbitNames } from '../constants/familiesAndTags.js'
import { processFamilyParams, processFamilyBroucke } from "../utils/dataProcessing.js"
import { getForParamsPage, getForBrouckePage } from "../utils/dataProcForTransfers.js"
import { ParamsArrayTemplate, BrouckeArrayTemplate, OrbitTemplate } from '@/utils/validation.js';
import { z } from 'zod';
import { useI18n } from 'vue-i18n'
import { computed } from 'vue'
import { useTimerStore } from '@/store/timer'

export default {
  components: { HiddingPanel, CustomSelect, Panel, Graph, BrouckeDiagram, GradientSelect, Accordion, Notification, transferPopUp },
  setup() {
    const { t, locale } = useI18n()

    const graphTypeOptions = computed(() => ( {
      [t('orbit_family.params')]: "params",
      [t('orbit_family.broucke')]: "broucke"
    }))

    const axesOptions = computed(() => ({
        [t('parameters.t')]: 't',
        [t('parameters.ax')]: 'ax',
        [t('parameters.ay')]: 'ay',
        [t('parameters.az')]: 'az',
        [t('parameters.earth_dist')]: 'dist_primary',
        [t('parameters.moon_dist')]: 'dist_secondary',
        [t('parameters.jacobi')]: 'cj',
        [t('parameters.max_floke')]: 'floke',
        [t('parameters.initial_x')]: 'x',
        [t('parameters.initial_z')]: 'z',
        [t('parameters.initial_speed_y')]: 'vy',
        [t('parameters.stability_index')+' 1']: 'stability_ind_1',
        [t('parameters.stability_index')+' 2']: 'stability_ind_2',
        [t('parameters.stability_index')+' 3']: 'stability_ind_3',
        [t('parameters.stability')]: 'stable'
    }))

    const { tagToFamilyName, familyToTagL1, familyToTagL2 } = useOrbitNames()

    return { t, locale, graphTypeOptions, axesOptions, tagToFamilyName, familyToTagL1, familyToTagL2 }
  },
  data() {
    return {
      timerStore: useTimerStore(),
      selectedType: this.t('orbit_family.params'),
      formData: {
        point: 'L1',
        selectedFamily: this.tagToFamilyName["L1.L"], 
        horizontal: this.t('parameters.ax'),
        vertical: this.t('parameters.ay'),
      },
      graphSettings: {
        gradientName: 'Winter',
        parameter: this.t('parameters.t'),
        selectedPoints: []
      },
      labelsShift: 380,
      fetchedData: [[],[],[]],
      popUp: undefined,
      pageState: 'OK',
      canUpdateURL: true
    }
  },
  mounted() {
    this.drawGraphs();
  },
  computed: {
    PanelHeight() { //настраиваем высоту панели в зависимости от выбранного графика
      if (this.selectedType === this.t('orbit_family.params')) return 'calc(100vh - 175px)'
      return '500px'
    }
  },
  watch: {
    'formData.point': {
      handler(newPoint) {
        if(newPoint === 'L1' & this.familyToTagL1[this.formData.selectedFamily] === undefined){
          this.formData.selectedFamily = this.tagToFamilyName["L1.L"]
        }
        if(newPoint === 'L2' & this.familyToTagL2[this.formData.selectedFamily] === undefined){
          this.formData.selectedFamily = this.tagToFamilyName["L2.L"]
        }
      },
      immediate: true
    },
    '$route.query': {
      handler() {
        this.loadParams();
      },
      deep: true,
      immediate: true
    },
    'selectedType': {
      handler() {
        if(this.$route.query.graph === this.graphTypeOptions[this.selectedType]) return;

        this.updateUrl();
        this.drawGraphs();
      },
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
    'graphTypeOptions': {
      handler(newValue, oldValue) {
        if(oldValue === undefined) return;

        let param_tag = oldValue[this.selectedType];

        let keys = Object.keys(newValue);
        for(let i = 0; i<keys.length; ++i){
          if(newValue[keys[i]] === param_tag){
            this.selectedType = keys[i];
            break;
          }
        }
      },
      immediate: true,
      deep: true
    },
    'axesOptions': {
      handler(newValue, oldValue) {
        if(oldValue === undefined) return;

        let horiz_tag = oldValue[this.formData.horizontal];
        let vert_tag = oldValue[this.formData.vertical];
        let color_tag = oldValue[this.graphSettings.parameter];

        let keys = Object.keys(newValue);
        for(let i = 0; i<keys.length; ++i){
          if(newValue[keys[i]] === horiz_tag){
            this.formData.horizontal = keys[i];
          }
          if(newValue[keys[i]] === vert_tag){
            this.formData.vertical = keys[i];
          }
          if(newValue[keys[i]] === color_tag){
            this.graphSettings.parameter = keys[i];
          }
        }
      },
      immediate: true,
      deep: true
    },
    'familyToTagL1': {
      handler(newValue, oldValue) {
        if(this.formData.point !== 'L1') return
        if(oldValue === undefined) return;

        let tag = oldValue[this.formData.selectedFamily];

        this.formData.selectedFamily = this.tagToFamilyName[`${this.formData.point}.${tag}`]
      },
      immediate: true,
      deep: true
    },
    'familyToTagL2': {
      handler(newValue, oldValue) {
        if(this.formData.point !== 'L2') return
        if(oldValue === undefined) return;

        let tag = oldValue[this.formData.selectedFamily];

        this.formData.selectedFamily = this.tagToFamilyName[`${this.formData.point}.${tag}`]
      },
      immediate: true,
      deep: true
    }
  },
  methods: {
    updateUrl() {
      if(!this.canUpdateURL) return
      this.canUpdateURL = false

      let fam_tag;
      if(this.formData.point === 'L1'){
        fam_tag = this.familyToTagL1[this.formData.selectedFamily];
      }
      else{
        fam_tag = this.familyToTagL2[this.formData.selectedFamily];
      }

      var common = {
        graph: this.graphTypeOptions[this.selectedType],
        point: this.formData.point,
        family: fam_tag,
        gradient: this.graphSettings.gradientName,
        color_param: this.axesOptions[this.graphSettings.parameter]
      };
      var specific = {};

      if(this.selectedType === this.t('orbit_family.params')){
        specific.param_x = this.axesOptions[this.formData.horizontal];
        specific.param_y = this.axesOptions[this.formData.vertical];
      }

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

      setTimeout(() => this.canUpdateURL = true, 10);
    },
    loadParams() {
      if(!this.canUpdateURL) return
      
      const { graph, point, family, param_x, param_y, gradient, color_param, selected_points } = this.$route.query;

      this.selectedType = checkIncludesReversed(graph, this.graphTypeOptions);
      this.formData.point = checkIncludes(point, ['L1', 'L2']);
      this.graphSettings.gradientName = checkGradient(gradient);
      this.graphSettings.selectedPoints = checkPoints(selected_points);

      if(this.formData.point === 'L1'){
        this.formData.selectedFamily = checkIncludesReversed(family, this.familyToTagL1);
      }
      else{
        this.formData.selectedFamily = checkIncludesReversed(family, this.familyToTagL2);
      }

      if(this.selectedType === this.t('orbit_family.params')){
        this.formData.horizontal = checkIncludesReversed(param_x, this.axesOptions, 0);
        this.formData.vertical = checkIncludesReversed(param_y, this.axesOptions, 6);
        this.graphSettings.parameter = checkIncludesReversed(color_param, this.axesOptions, 1);
      }
      else{
        this.graphSettings.parameter = checkIncludes(color_param, Object.keys(this.axesOptions));
      }

      if(this.$route.fullPath === '/orbit_family') this.updateUrl();
    },
    handlePanelToggle(isHidden){ //следим за движением панели
      if(isHidden){
        this.labelsShift = 0;
      }
      else{
        this.labelsShift = 360;
      }
    },
    getFilterParams(){ //получаем фильтры для запроса
      let point = this.formData.point;

      if(point === 'L1'){
        var family_tag = this.familyToTagL1[this.formData.selectedFamily];
      }
      else{
        var family_tag = this.familyToTagL2[this.formData.selectedFamily];
      }

      let param_x = this.axesOptions[this.formData.horizontal];
      let param_y = this.axesOptions[this.formData.vertical];
      let param_z = this.axesOptions[this.graphSettings.parameter];
      return `lib_point=${point}&family_tag=${family_tag}&param_name_x=${param_x}&param_name_y=${param_y}&param_name_z=${param_z}`;
    },
    getFilterBroucke(){
      let point = this.formData.point;

      if(point === 'L1'){
        var family_tag = this.familyToTagL1[this.formData.selectedFamily];
      }
      else{
        var family_tag = this.familyToTagL2[this.formData.selectedFamily];
      }

      return `filter_groups=[{"log_op":"AND", "filters":[{"field":"lib_point", "op":"like", "value":"${point}"},
      {"field":"family_tag", "op":"like", "value":"${family_tag}"}]}]`;
    },
    async fetchParams(resetSelectedPoints=false) { //запрашиваем данные(для параметров семейства)
      if(resetSelectedPoints) this.graphSettings.selectedPoints = []

      this.pageState = 'Loading';    
      try {
        const filter = this.getFilterParams();
        const response = await fetch(`${this.$AppURL}/orbit_view/get_family_param?${filter}`);
        
        if (!response.ok) {
          throw new Error(`статус запроса: ${response.status}`);
        }
        
        const data = await response.json();
        this.fetchedData = ParamsArrayTemplate.parse(data);
        this.dataForTransfer = getForParamsPage(this.fetchedData);
        this.fetchedData = processFamilyParams(this.fetchedData);

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
    async fetchBroucke(resetSelectedPoints=false){
      if(resetSelectedPoints) this.graphSettings.selectedPoints = []

      this.pageState = 'Loading';
      try {
        this.timerStore.start()

        const filter = this.getFilterBroucke();
        const response = await fetch(`${this.$AppURL}/orbit_view/get_Broucke?${filter}`);
        
        if (!response.ok) {
          throw new Error(`статус запроса: ${response.status}`);
        }
        
        const data = await response.json();
        this.fetchedData = BrouckeArrayTemplate.parse(data);
        this.dataForTransfer = getForBrouckePage(this.fetchedData);
        this.fetchedData = processFamilyBroucke(this.fetchedData, this.axesOptions[this.graphSettings.parameter]);

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
    drawGraphs(){
      if(this.selectedType === this.t('orbit_family.params')){
        this.fetchParams();
      }
      else {
        this.fetchBroucke();
      }
    },
    async updateOnClickData(newPopUpData){
      let d = this.dataForTransfer[`${newPopUpData.dataX}:${newPopUpData.dataY}`];

      try{
        let response = await fetch(`${this.$AppURL}/orbit_view/get_nearest_orbit?x=${d.x}&z=${d.z}`);
        
        if (!response.ok) {
          throw new Error(`статус запроса: ${response.status}`);
        }
      
        let data = await response.json();
        let orbitInfo = OrbitTemplate.parse(data);

        newPopUpData = { ...newPopUpData, cj: d.cj, x: d.x, z: d.z, family_tag: orbitInfo.family_tag, ...orbitInfo };
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
      this.popUp = newPopUpData;
    }
  }
}
</script>

<style scoped>

.panel-with-scroll{
  overflow-y: auto; 
  scrollbar-color: var(--scrollbar) transparent;
}

h3 {
  margin: 0;
  padding: 0;
  font-size: 20px;
  color: var(--text-primary);
}

.vertical-group {
  padding-bottom: 5px;
  display: flex;
  flex-direction: column;
  gap: 0px;
}

.horizontal-group {
  display: flex;
  justify-content: space-between;
  gap: 7px; 
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
  margin: 5px 63px 5px 0px;
  display: flex;
  align-items: center;
  color: var(--text-primary);
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
  z-index: 50;
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