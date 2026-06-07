<template>
  <HiddingPanel @panel-toggle="handlePanelToggle">
    <Panel height="calc(100vh - 140px)" width="390px" class="panel-with-scroll">
      <Accordion width="370px">
        <template #header>
          <h3>{{ $t('map.header') }}</h3>
          <infoIcon></infoIcon>
        </template>
        <template #content>
          <div class="horizontal-group" style="width: 370px; padding-top: 0px">
            <text class="text-description">{{ $t('map.point') }}</text>
            <div class="inputs" style="display: flex; justify-content: space-between; gap: 12px; ">
              <div class="input-and-text">
                <input type="radio" name="point" value="L1" checked v-model="formData.point" @change="updateGridMinMax"/>{{ $t('map.system') }} L1
              </div>
              <div class="input-and-text">
                <input type="radio" name="point" value="L2" v-model="formData.point"  @change="updateGridMinMax"/>{{ $t('map.system') }} L2
              </div>
            </div>
          </div>

          <div class="horizontal-group">
            <CustomMultipleSelect v-if="formData.point=='L1'"
              @change-options="updateSelectedFamilies"
              :defaultOptions="new Set(formData.selectedFamilies)"
              :options="Object.keys(this.familyToTagL1)"
              :currentPoint="this.formData.point"
              width="371px"
            ><text class="text-description" style="margin-top: 6px">{{ $t('common.family') }}</text>
            </CustomMultipleSelect>
            <CustomMultipleSelect v-else
              @change-options="updateSelectedFamilies"
              :defaultOptions="new Set(formData.selectedFamilies)"
              :options="Object.keys(this.familyToTagL2)"
              :currentPoint="this.formData.point"
              width="371px"
            ><text class="text-description" style="margin-top: 6px">{{ $t('common.family') }}</text>
            </CustomMultipleSelect>
          </div>
          
          <inputGrid @input-changed="updateFormdata" :formData="formData" :minMax="MinMaxValues"> </inputGrid> <!-- Поля-фильтры -->
          
          <div class="stability-group">
            <div class="input-and-text">
              <input type="radio" name="stability" value="1" v-model="formData.stable"/>{{ $t('map.stable') }}
            </div>
            <div class="input-and-text">
              <input type="radio" name="stability" value="0" v-model="formData.stable"/>{{ $t('map.not_stable') }}
            </div>
            <div class="input-and-text">
              <input type="radio" name="stability" value="2" v-model="formData.stable"/>{{ $t('map.both_types') }}
            </div>
          </div>

        </template>
      </Accordion>

      <Accordion width="370px" style="padding: 10px 0 100px 0">
        <template #header>
          <h3>{{ $t('common.graph_settings') }}</h3>
        </template>
        
        <template #content>
          <div class="horizontal-group" style="padding: 0 0 5px 0">
            <text style="color: var(--text-primary)">{{ $t('common.palette') }}</text>
            <GradientSelect v-model="graphSettings.gradientName"/>
          </div>

          <div class="vertical-group">
            <text class="text-description">{{ $t('common.color_param') }}</text>
            <CustomSelect
              v-model="graphSettings.parameter"
              :options="Object.keys(highlightionParameters)"
              width="342px"
            ></CustomSelect>
          </div>

          <div class="group-center">
            <text class="text-description" style="width: 165px">{{ $t('map.coord_center') }}</text>
            <div class="inputs">
              <div class="input-and-text">
                <input type="radio" name="center" value="BC" v-model="graphSettings.center"/>{{ $t('map.barycenter') }}
              </div>
              <div class="input-and-text">
                <input type="radio" name="center" value="L1" v-model="graphSettings.center"/>{{ $t('map.point') }} L1
              </div>
              <div class="input-and-text">
                <input type="radio" name="center" value="L2" v-model="graphSettings.center"/>{{ $t('map.point') }} L2
              </div>
              <div class="input-and-text">
                <input type="radio" name="center" value="MN" v-model="graphSettings.center"/>{{ $t('map.moon') }}
              </div>
            </div>
          </div>

          <div class="group-center">
            <text style="color: var(--text-primary); width: 163px">{{ $t('map.plane') }}</text>
            <div class="vertical-group" style="align-items: none;">
              <div class="input-and-text">
                <input type="radio" name="plane" value="XZ" v-model="graphSettings.plane"/>X - Z
              </div>
              <div class="input-and-text">
                <input type="radio" name="plane" value="XV" v-model="graphSettings.plane"/>X - |V|
              </div>
            </div>
          </div>
        </template>
      </Accordion>
      <input type="button" :value="$t('common.build')" @click="fetchMapData(true)">
    </Panel>
  </HiddingPanel>

  <Tip1/>
  <div class="page-content">
    <Graph
      :data="trajectoryData"
      :shift=labelsShift
      :gradientName=graphSettings.gradientName
      :selectedPoints="graphSettings.selectedPoints"
      :gaps="graphSettings.gaps"
      :factor="20"
      width="100%" 
      height="100%"
      x-axes-name="X"
      :y-axes-name= "graphSettings.plane === 'XZ' ? 'Z' : '|V|'"
      @point-clicked="updateOnClickData"
    />
  </div>
  
  <Notification :newState="pageState"></Notification>
  <transferPopUp :popUp="popUp" :currPageNumber="1"></transferPopUp>
</template>

<script>
import Tip1 from './Tip1.vue'
import HiddingPanel from '../common/HiddingPanel.vue'
import Graph from '../common/Graph.vue'
import Panel from '../common/Panel.vue'
import CustomMultipleSelect from '../common/CustomMultipleSelect.vue'
import CustomSelect from '../common/CustomSelect.vue'
import Notification from '../common/Notification.vue'
import Accordion from '../common/Accordion.vue'
import GradientSelect from '../common/GradientSelect.vue'
import inputGrid from './inputGrid.vue'
import transferPopUp from '../common/transferPopUp.vue'
import infoIcon from './infoIcon.vue'
import { checkGradient, checkIncludes, checkFamilies, checkFloat, checkPoints, checkIncludesReversed } from '../../utils/checkers.js'
import { useOrbitNames } from '../../constants/familiesAndTags.js'
import { processPointsForMap, processMinMax } from "../../utils/dataProcessing.js"
import { PointArrayTemplate, MinMaxArrayTemplate, OrbitTemplate } from '../../utils/validation.js';
import { z } from 'zod';
import { useI18n } from 'vue-i18n'
import { computed } from 'vue'

export default {
  components: { Tip1, HiddingPanel, Graph, Panel, CustomMultipleSelect, Notification, Accordion, 
    GradientSelect, CustomSelect, inputGrid, transferPopUp, infoIcon },
  setup() {
    const { t, locale } = useI18n()

    const highlightionParameters = computed(() => ({
      [t('parameters.initial_speed_y')]: "vy",
      [t('parameters.ax')]: 'ax',
      [t('parameters.ay')]: 'ay',
      [t('parameters.az')]: 'az',
      [t('parameters.jacobi')]: 'cj',
      [t('parameters.earth_dist')]: 'dist_primary',
      [t('parameters.moon_dist')]: 'dist_secondary'
    }))

    const { tagToFamilyName, familyToTagL1, familyToTagL2 } = useOrbitNames()

    return { t, locale, highlightionParameters, tagToFamilyName, familyToTagL1, familyToTagL2 }
  },
  data() {
    return {
      formData: {
        point: 'L1',
        selectedFamilies: [],
        amplitudeX: { min: '', max: '' },
        amplitudeY: { min: '', max: '' },
        amplitudeZ: { min: '', max: '' },
        earthDistance: { min: '', max: '' },
        moonDistance: { min: '', max: '' },
        period: { min: '', max: '' },
        jacobiConst: { min: '', max: '' },
        stability_ind_1: { min: '', max: '' },
        stability_ind_2: { min: '', max: '' },
        stability_ind_3: { min: '', max: '' },
        stable: "2"
      },
      graphSettings: {
        gradientName: 'Winter',
        parameter: this.t('parameters.initial_speed_y'),
        center: 'BC',
        selectedPoints: [],
        gaps: [],
        plane: 'XZ'
      },
      MinMaxValues: {},
      popUp: undefined,
      trajectoryData: [[],[],[]],
      labelsShift: 430,
      pageState: 'OK',
      canUpdateURL: true
    }
  },
  mounted(){
    this.updateGridMinMax();
    this.fetchMapData();
  },
  watch: {
    'formData.point': {
      handler() {
        this.formData.selectedFamilies = [];
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
    'formData': {
      handler() {
        this.updateUrl();
      },
      immediate: true,
      deep: true
    },
    'graphSettings': {
      handler(newValue) {
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
    },
    'tagToFamilyName': {
      async handler(newValue, oldValue) {
        if(this.formData.selectedFamilies.length === 0) return;

        var families = this.formData.selectedFamilies;
        var fam_tags = new Array();

        let keys = Object.keys(oldValue);

        for(let i = 0; i<keys.length; ++i){
          if(families.includes( oldValue[keys[i]] )){
            fam_tags.push(keys[i])
          }
        }

        for(let i = 0; i<fam_tags.length; ++i){
          families[i] = newValue[fam_tags[i]];
        }
        this.formData.selectedFamilies = families;
      }
    }
  },
  methods: {
    updateUrl() {
      if(!this.canUpdateURL) return
      this.canUpdateURL = false
      
      var optionalForQuery = {};
      var optionalParams = ['amplitudeX', 'amplitudeY', 'amplitudeZ', 'earthDistance', 'moonDistance', 'period', 'jacobiConst', 
                            'stability_ind_1', 'stability_ind_2', 'stability_ind_3'];
      var paramsCuts = ['ax', 'ay', 'az', 'ed', 'md', 't', 'cj', 'stab_ind_1', 'stab_ind_2', 'stab_ind_3'];

      for(var i = 0; i < optionalParams.length; ++i){
        var param = this.formData[optionalParams[i]];
        if(param.min !== ''){
          optionalForQuery[`${paramsCuts[i]}_min`] = param.min;
        }
        if(param.max !== ''){
          optionalForQuery[`${paramsCuts[i]}_max`] = param.max;
        }
      }

      var families = this.formData.selectedFamilies;
      var fam_tags = new Array(families.length);

      if(this.formData.selectedFamilies.length > 0){
        if(this.formData.point === 'L1'){
          for(let i = 0; i<families.length; ++i){
            fam_tags[i] = this.familyToTagL1[families[i]];
          }
        }
        else {
          for(let i = 0; i<families.length; ++i){
            fam_tags[i] = this.familyToTagL2[families[i]];
          }
        }
        optionalForQuery.families = fam_tags.join(';')
      }

      if(this.graphSettings.selectedPoints.length>0){

        var points = this.graphSettings.selectedPoints;
        var preparedPoints = [];
        for(var i = 0; i<points.length; ++i){
          preparedPoints.push(`[${points[i].join(';')}]`);
        }
        optionalForQuery.selected_points = `[${preparedPoints.join(';')}]`
      }

      let color_param = this.highlightionParameters[this.graphSettings.parameter];

      this.$router.replace({
        query: {
          point: this.formData.point,
          ...optionalForQuery,
          stable: this.formData.stable,
          gradient: this.graphSettings.gradientName,
          color_param: color_param,
          center: this.graphSettings.center,
          plane: this.graphSettings.plane
        }
      })

      setTimeout(() => this.canUpdateURL = true, 10);
    },
    loadParams() {
      if(!this.canUpdateURL) return

      const { point, families, gradient, center, color_param, selected_points, ax_min, ax_max, ay_min, ay_max, az_min,
         az_max, ed_min, ed_max, md_min, md_max, t_min, t_max, cj_min, cj_max, stab_ind_1_min, stab_ind_1_max, stab_ind_2_min,
        stab_ind_2_max, stab_ind_3_min, stab_ind_3_max, stable, plane } = this.$route.query;

      this.formData.point = checkIncludes(point, ['L1', 'L2']);
      this.graphSettings.gradientName = checkGradient(gradient);
      this.graphSettings.parameter = checkIncludesReversed(color_param, this.highlightionParameters);
      this.graphSettings.center = checkIncludes(center, ['BC', 'L1', 'L2', 'MN']);
      this.graphSettings.plane = checkIncludes(plane, ['XZ', 'XV']);
      this.graphSettings.selectedPoints = checkPoints(selected_points);
      
      if(families && this.formData.point === 'L1'){
        this.formData.selectedFamilies = checkFamilies(families.split(';'), Object.values(this.familyToTagL1), this.tagToFamilyName, 'L1');
      }
      if(families && this.formData.point === 'L2'){
        this.formData.selectedFamilies = checkFamilies(families.split(';'), Object.values(familyToTagL2), this.tagToFamilyName, 'L2');
      }

      if(["0", "1", "2"].includes(stable)){
        this.formData.stable = stable;
      }
      
      //сначала идет min значение, потом max - обязательно
      var recParams = [ax_min, ax_max, ay_min, ay_max, az_min, az_max, ed_min, ed_max, md_min, md_max, t_min, t_max, cj_min, cj_max,
                       stab_ind_1_min, stab_ind_1_max, stab_ind_2_min, stab_ind_2_max, stab_ind_3_min, stab_ind_3_max ];
      var formDataParams = ['amplitudeX', 'amplitudeY', 'amplitudeZ', 'earthDistance', 'moonDistance', 'period', 'jacobiConst', 
                            'stability_ind_1', 'stability_ind_2', 'stability_ind_3' ];

      for(var i = 0; i < recParams.length; ++i){
        if(recParams[i] && checkFloat(recParams[i])){
          var paramName = formDataParams[Math.floor(i/2)];
          if(i%2==0){
            this.formData[paramName].min = recParams[i];
          }
          else{
            this.formData[paramName].max = recParams[i];
          }
        }
      }

      if(this.$route.fullPath === '/map') this.updateUrl();
    },
    handlePanelToggle(isHidden){ //следим за движением панели
      if(isHidden){
        this.labelsShift = 0;
      }
      else{
        this.labelsShift = 430;
      }
    },
    getFilters(formData){ //получаем фильтры для запроса
      var filters = Array();
      filters.push(`{"log_op":"NONE", "filters":[{"field":"lib_point","op":"like","value":"${formData.point}"}]}`);
      var family_filters = '';
      var familyArray;

      if(formData.selectedFamilies.length>0){
        familyArray = formData.selectedFamilies;
      }
      else if(formData.point=='L1'){
        familyArray = Object.keys(this.familyToTagL1);
      }
      else{
        familyArray = Object.keys(this.familyToTagL2);
      }

      //фильтры по семьям
      for(var i = 0; i < familyArray.length; ++i){
        if(formData.point=='L1'){
          var family_name = this.familyToTagL1[familyArray[i]];
        }
        else{
          var family_name = this.familyToTagL2[familyArray[i]];
        }
        family_filters += `{"field":"family_tag","op":"like","value":"${family_name}"}`

        if(i < familyArray.length - 1){
          family_filters += ',';
        }
      }

      filters.push(`{"log_op":"OR","filters":[${family_filters}]}`)

      //фильтр по устойчивости
      if(this.formData.stable !== "2"){
        let stable;
        if(this.formData.stable == "1"){ stable = "true" }
        else { stable = "false" }
        filters.push(`{"log_op":"NONE","filters":[{"field":"stable","op":"==", "value":${stable}}]}`)
      }
      
      //фильтры по другим параметрам
      var parametrs = [formData.amplitudeX, formData.amplitudeY, formData.amplitudeZ, formData.earthDistance, formData.moonDistance,
        formData.period, formData.jacobiConst, formData.stability_ind_1, formData.stability_ind_2, formData.stability_ind_3];
      var columns = ['ax','ay','az','dist_primary','dist_secondary','t','cj', 'stability_ind_1', 'stability_ind_2', 'stability_ind_3'];

      for(var i = 0; i < parametrs.length; ++i){
        if(parametrs[i].min!=''){
          filters.push(`{"log_op":"NONE","filters":[{"field":"${columns[i]}","op":">", "value":${parametrs[i].min}}]}`)
        }
        if(parametrs[i].max!=''){
          filters.push(`{"log_op":"NONE","filters":[{"field":"${columns[i]}","op":"<", "value":${parametrs[i].max}}]}`)
        }
      }

      return '[' + filters.toString() + ']';
    },
    async fetchMapData(resetSelectedPoints=false){ //запрашиваем точки с бэкенда
      if(resetSelectedPoints) this.graphSettings.selectedPoints = []

      this.pageState = 'Loading';
      try {
        const filter_groups = this.getFilters(this.formData);
        const response = await fetch(`${this.$AppURL}/orbit_view/get_map?filter_groups=${filter_groups}`);

        if (!response.ok) {
          throw new Error(`статус запроса: ${response.status}`);
        }

        const data = await response.json();
        this.trajectoryData = PointArrayTemplate.parse(data);
        let parameter = this.highlightionParameters[this.graphSettings.parameter];
        this.setGaps(data);

        var shift;
        if(this.graphSettings.center === 'L1'){
          shift = 321696.11828659114;
        }
        else if(this.graphSettings.center === 'L2'){
          shift = 444255.2104148698;
        }
        else if(this.graphSettings.center === 'MN'){
          shift = 379726.45778546645;
        }
        else{
          shift = 0;
        }
        this.trajectoryData = processPointsForMap(this.trajectoryData, parameter, shift, this.graphSettings.plane);

        if(this.trajectoryData[0].length === 0){
          this.pageState = 'noPointsError';
        }
        else this.pageState = 'OK';
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
    setGaps(data){
      this.graphSettings.gaps = [];
      for(let i = 1; i < data.length; ++i){
        if(data[i-1]['family_tag'] !== data[i]['family_tag'] || data[i]['family_tag']==='Q'){
          this.graphSettings.gaps.push(i);
        }
      }
    },
    updateSelectedFamilies(selectedOptions){ //обновляем поле выбранных семейств
      this.formData.selectedFamilies = selectedOptions;
      this.updateGridMinMax();
    },
    async updateGridMinMax(){
      const filter_groups = this.getFilters(this.formData);
      const response = await fetch(`${this.$AppURL}/orbit_families/get_families?filter_groups=${filter_groups}`);

      if (!response.ok){
          throw new Error(`статус запроса: ${response.status}`);
      }
      
      const data = await response.json();
      let MinMaxValidated = MinMaxArrayTemplate.parse(data);
      if(MinMaxValidated.length>0){
        this.MinMaxValues = processMinMax(MinMaxValidated);
      }
    },
    updateFormdata(fields, newValue){ //обновляем остальные поля формы
      var [field1, field2] = fields.split('.');
      this.formData[field1][field2] = newValue;
    },
    async updateOnClickData(newPopUpData){
      try{
        newPopUpData.x = newPopUpData.dataX;
        newPopUpData.z = newPopUpData.dataY;

        let response = await fetch(`${this.$AppURL}/orbit_view/get_nearest_orbit?x=${newPopUpData.x}&z=${newPopUpData.z}`);
        
        if (!response.ok) {
          throw new Error(`статус запроса: ${response.status}`);
        }
      
        let data = await response.json();
        let orbitInfo = OrbitTemplate.parse(data);
        orbitInfo.point = orbitInfo.lib_point;

        this.popUp = { ...newPopUpData, ...orbitInfo, family_tag: orbitInfo.family_tag };
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

.panel-with-scroll{
  overflow-y: auto; 
  scrollbar-color: var(--scrollbar) transparent;
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

input[type="checkbox"] {
  height: 20px;
  width: 20px;
  cursor: pointer;
  margin: 0;
  padding: 0;
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

.input-and-text {
  margin: 5px 0px;
  display: flex;
  align-items: center;
  color: var(--text-primary);
}

.vertical-group {
  padding-bottom: 5px;
  display: flex;
  flex-direction: column;
  gap: 0px;
}

.horizontal-group {
  padding-top: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 7px; 
}

.stability-group {
  padding-top: 5px;
  display: flex;
  justify-content: left;
  align-items: center;
  width: 370px;
  gap: 9px; 
}

.group-center{
  padding-top: 5px;
  display: flex;
  gap: 25px; 
  width: 370px; 
}

input[type="button"] {
  width: 220px;
  height: 42px;
  cursor: pointer;
  background: var(--highlight-color);
  border-radius: 10px;
  border: none;
  margin-left: 75px;
  bottom: 10px;
  position: absolute;
  color: var(--text-button-able);
  font-size: 17px;
  box-shadow: 0px 0px 10px 10px var(--highlight-shadow);
  z-index: 50;
}

input[type="checkbox"]{
  height: 20px;
  width: 20px;
  cursor: pointer;
  margin: 0;
  padding: 0;
}

.checkbox-container{
  display: flex;
  justify-content: left; 
  gap: 7px;
  margin-bottom: 5px;
}

.page-content {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.data-container{
  width: 300px; 
  text-align: left;
  margin: 0 auto;
}

</style>