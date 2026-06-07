<template>
  <HiddingPanel @panel-toggle="handlePanelToggle">
    <Panel width='340px' :height="firstPanelHeight" class="first-panel">
      <Accordion width="320px">
        <template #header>
          <h3>{{ $t('orbit.header1') }}</h3>
        </template>

        <template #content>
          <div class="horizontal-group">
            <text class="text-description">{{ $t('orbit.graph_type') }}</text>

            <CustomSelect
              v-model="selectedType"
              :options="Object.keys(graphTypeOptions)"
              width="185px"
            ></CustomSelect>
          </div>

          <div class="vertical-group">
            <text class="text-description">{{ $t('orbit.initial_coordinates') }}</text>
            <div class="coordinates-group">
              <div class="horizontal-group">
                <text class="text-description">X({{ $t('common.km') }})</text>
                <validatedInput :defaultValue="formData.x" placeholder="100 000" fields="x" @input-changed="updateFormdata" width="70px"/>
              </div>
              <div class="horizontal-group">
                <text class="text-description">Z({{ $t('common.km') }})</text>
                <validatedInput :defaultValue="formData.z" placeholder="100 000" fields="z"  @input-changed="updateFormdata" width="70px"/>
              </div>
            </div>
          </div>

          <div v-if="selectedType === $t('orbit.graph_poincare')" class="horizontal-group">
            <text class="text-description">{{ $t('orbit.plane') }}</text>
            <CustomSelect
              v-model="formData.plane"
              :options="planeOptions"
              width="185px"
            ></CustomSelect>
          </div>
        </template>
      </Accordion>

      <Accordion width="320px" style="padding: 0">
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
            <CustomSelect v-if="selectedType === $t('orbit.graph_projections')"
              v-model="graphSettings.parameter"
              :options="Object.keys(highlightionParameters)"
              width="292px"
            ></CustomSelect>
            <CustomSelect v-else-if="selectedType === $t('orbit.graph_3d')"
              v-model="graphSettings.parameter"
              :options="Object.keys(highlightionParameters).slice(0, -1)"
              width="292px"
            ></CustomSelect>
            <CustomSelect v-else
              v-model="graphSettings.parameter"
              :options="Object.keys(highlightionParameters).slice(0, -2)"
              width="292px"
            ></CustomSelect>
          </div>
        </template>
      </Accordion>

      <input v-if="selectedType === $t('orbit.graph_projections')" type="button" :value="$t('common.build')" @click="fetchTrajectoryData(true)" :disabled="isDisabled()" style="bottom: 10px">
      <input v-else-if="selectedType === $t('orbit.graph_3d')" type="button" :value="$t('common.build')" @click="fetchTrajectoryData(true)" :disabled="isDisabled()" style="bottom: 170px">
      <input v-else-if="selectedType === $t('orbit.graph_poincare')" type="button" :value="$t('common.build')" @click="fetchPoincareData(true)" :disabled="isDisabled()" style="bottom: 10px">
    </Panel>
      
    <Panel height="120px" width="340px" v-if="selectedType === $t('orbit.graph_3d')">
      <h4>{{ $t('orbit.header2') }}</h4>

      <div class="vertical-group" style="padding: 5px 0 0 0">
        <div class="checkbox-container">
          <input type="checkbox" :checked="graph3DSettings.charAt(0) === '1'" @change="inputChanged($event.target.checked, 0)"/>
          <text class="checkbox-text">{{ $t('orbit.trajectory') }}</text>
        </div>
        <div class="checkbox-container">
          <input type="checkbox" :checked="graph3DSettings.charAt(1) === '1'"  @change="inputChanged($event.target.checked, 1)">
          <text class="checkbox-text">{{ $t('orbit.projection_onto') }} XY</text>
        </div>
        <div class="checkbox-container">
          <input type="checkbox" :checked="graph3DSettings.charAt(2) === '1'"  @change="inputChanged($event.target.checked, 2)"/>
          <text class="checkbox-text">{{ $t('orbit.projection_onto') }} XZ</text>
        </div>
        <div class="checkbox-container">
          <input type="checkbox" :checked="graph3DSettings.charAt(3) === '1'"  @change="inputChanged($event.target.checked, 3)"/>
          <text class="checkbox-text">{{ $t('orbit.projection_onto') }} YZ</text>
        </div>
      </div>
    </Panel>

  </HiddingPanel>

  <HiddingPanel @panel-toggle="handlePanelToggle" :onTheRight="true">

    <Panel height="auto" width="340px">
      <h4 style="color: var(--text-primary);">{{ $t('orbit.header3') }}</h4>

      <orbitInfo
        :orbitInfo="this.orbitInfo"
      ></orbitInfo>
      
    </Panel>

    <transferFromPage2 
      :transferInfo="transferInfo" 
      :prevNextOrbit="prevNextOrbit" 
      :graphType="selectedType"
      :graphSettings="graphSettings"
      :graphParams="getGraphParams"
      @update-graph="drawGraphs">
    </transferFromPage2>

    <Tip2/>

  </HiddingPanel>
  
  <div v-if="selectedType === $t('orbit.graph_projections')" class="page-content">

    <div class="graph-container">
      <div class="graph-section">
        <Graph 
          :data="xyProjection"
          :gradientName=graphSettings.gradientName
          :shift=labelsShift
          width="100%" 
          height="100%"
          x-axes-name="X"
          y-axes-name="Y"
          @point-clicked="(eventData) => updateOnClickData(eventData, 'projection', 'XY')"
        />
      </div>
      <div class="graph-section" style="border: solid var(--graphs-border-color); border-width: 0 3px 0 3px">
        <Graph 
          :data="xzProjection" 
          :gradientName=graphSettings.gradientName
          width="100%" 
          height="100%"
          x-axes-name="X"
          y-axes-name="Z"
          @point-clicked="(eventData) => updateOnClickData(eventData, 'projection', 'XZ')"
        />
      </div>
      <div class="graph-section">
        <Graph 
          :data="yzProjection" 
          :gradientName=graphSettings.gradientName
          width="100%" 
          height="100%"
          x-axes-name="Y"
          y-axes-name="Z"
          @point-clicked="(eventData) => updateOnClickData(eventData, 'projection', 'YZ')"
        />
      </div>
    </div>
  </div>

  <div v-if="selectedType === $t('orbit.graph_3d')" class="page-content">
    <Graph3D 
      :data="orbitTrajectory" 
      :settings="graph3DSettings"
      :gradientName=graphSettings.gradientName
      width="100%" 
      height="100%"
    />
  </div>

  <div v-if="selectedType === $t('orbit.graph_poincare')" class="page-content">
    <Graph 
      :data="fetchedData" 
      :shift=labelsShift
      width="100%" 
      height="100%"
      :x-axes-name="getAxisNames()[0]"
      :y-axes-name="getAxisNames()[1]"
      :show-line="false"
      @point-clicked="(eventData) => updateOnClickData(eventData, 'poincare', '')"
    />
  </div>

  <Notification :newState="pageState"></Notification>
  <popUpPage2 :popUp="popUp"></popUpPage2>
</template>

<script>
import Tip2 from './Tip2.vue'
import HiddingPanel from './../common/HiddingPanel.vue'
import Graph from './../common/Graph.vue'
import Graph3D from './../common/3DGraph.vue'
import Panel from './../common/Panel.vue'
import CustomSelect from './../common/CustomSelect.vue'
import Accordion from './../common/Accordion.vue'
import GradientSelect from './../common/GradientSelect.vue'
import orbitInfo from './orbitInfo.vue'
import Notification from '../common/Notification.vue'
import validatedInput from '../common/validatedInput.vue'
import transferFromPage2 from './transferFromPage2.vue'
import popUpPage2 from './popUpPage2.vue'
import { checkFloat, checkGradient, checkParameter, checkIncludes, checkIncludesReversed } from '../../utils/checkers.js'
import { processPointsForPoincare, processProjections, processOrbit } from "../../utils/dataProcessing.js"
import { getAbsVFor2ndPageProjections, getAbsVFor2ndPagePoincare } from "../../utils/dataProcForTransfers.js"
import { PoincareTemplate, OrbitTemplate, ChunkArrayTemplate, NeighbourOrbitTemplate } from '../../utils/validation.js';
import { useOrbitNames } from '../../constants/familiesAndTags.js'
import { z } from 'zod';
import { useI18n } from 'vue-i18n'
import { computed } from 'vue'

export default {
  components: { Tip2, HiddingPanel, Graph, Panel, CustomSelect, Graph3D, Notification, Accordion, GradientSelect, orbitInfo, validatedInput, transferFromPage2, popUpPage2 },
  setup() {
    const { t, locale } = useI18n()

    const graphTypeOptions = computed(() => ( {
      [t('orbit.graph_projections')]: "projections",
      [t('orbit.graph_3d')]: "3d_graph",
      [t('orbit.graph_poincare')]: "graph_poincare"
    }))

    const highlightionParameters = computed(() => ({
      [t('parameters.abs_v')]: "abs_v",
      [t('parameters.t')]: 't',
      [t('parameters.3rd_coord')]: '3rd_coord',
    }))

    const { tagToFamilyName } = useOrbitNames()

    return { t, locale, graphTypeOptions, highlightionParameters, tagToFamilyName }
  },
  data() {
    return {
      formData: {
        x: '0',
        z: '0',
        plane: 'x = 0'
      },
      planeOptions: [
        "x = 0",
        "y = 0",
        "z = 0",
        "vx = 0",
        "vy = 0",
        "vz = 0"
      ],
      selectedType: this.t('orbit.graph_projections'),
      fetchedData: [[],[]],
      xyProjection: [[],[]],
      xzProjection: [[],[]],
      yzProjection: [[],[]],
      orbitTrajectory: [],
      orbitInfo: {
        x: 0,
        z: 0,
        t: 0,
        cj: 0
      },
      prevNextOrbit: {
        prev: { },
        next: { }
      },
      popUp: undefined,
      labelsShift: 370,
      pageState: 'OK',
      graphSettings: {
        gradientName: 'Winter',
        parameter: this.t('parameters.abs_v')
      },
      graph3DSettings: "1111",
      canUpdateURL: true
    }
  },
  computed: {
    firstPanelHeight() { //настраиваем высоту панели в зависимости от выбранного графика
      if (this.selectedType === this.t('orbit.graph_poincare')) return "400px"
      return "350px"
    },
    transferInfo(){
      return { ...this.orbitInfo, family_tag: this.orbitInfo.family_tag }
    },
    getGraphParams(){
      let graphType = this.graphTypeOptions[this.selectedType];
      let settings = graphType === '3d_graph' ? this.graph3DSettings : undefined
      let plane = graphType === 'graph_poincare' ? this.formData.plane : undefined

      return { 
        gradientName: this.graphSettings.gradientName,
        parameter: this.highlightionParameters[this.graphSettings.parameter],
        graphType: graphType,
        settings: settings,
        plane: plane
      }
    }
  },
  mounted() {
    this.drawGraphs();
  },
  watch: {
    '$route.query': {
      handler() {
        this.loadParams();
      },
      deep: true,
      immediate: true
    },
    'selectedType': {
      handler(newValue) {
        if(this.$route.query.graph === this.graphTypeOptions[this.selectedType]) return;

        if(newValue === this.t('orbit.graph_3d') && this.graphSettings.parameter === this.t('parameters.3rd_coord')){
          this.graphSettings.parameter = this.t('parameters.abs_v');
        }
        if(newValue === this.t('orbit.graph_poincare') && this.graphSettings.parameter !== this.t('parameters.abs_v')){
          this.graphSettings.parameter = this.t('parameters.abs_v');
        }

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
        if(this.selectedType === this.t('orbit.graph_poincare')) return
        this.updateUrl();
      },
      immediate: true,
      deep: true
    },
    'graph3DSettings': {
      handler() {
        if(this.selectedType !== this.t('orbit.graph_3d')) return
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
  methods: {
    inputChanged(newVal, pos){
      this.graph3DSettings = this.graph3DSettings.slice(0, pos) + String(Number(newVal)) + this.graph3DSettings.slice(pos + 1);
    },
    updateUrl() {
      if(!this.canUpdateURL) return
      this.canUpdateURL = false

      var common = {
        graph: this.graphTypeOptions[this.selectedType],
        x: this.formData.x,
        z: this.formData.z,
      };
      var specific = {};

      if(this.selectedType === this.t('orbit.graph_projections')){
        specific.gradient = this.graphSettings.gradientName,
        specific.color_param = this.highlightionParameters[this.graphSettings.parameter]
      }
      else if(this.selectedType === this.t('orbit.graph_3d')){
        specific.gradient = this.graphSettings.gradientName,
        specific.color_param = this.highlightionParameters[this.graphSettings.parameter]
        specific.settings = this.graph3DSettings
      }
      else{
        specific.plane = this.formData.plane;
        specific.color_param = this.highlightionParameters[this.graphSettings.parameter]
        specific.gradient = this.graphSettings.gradientName
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

      const { graph, x, z, gradient, color_param, plane, settings } = this.$route.query;
      
      if(x !== '' & checkFloat(x)) {
        let i = x.indexOf(".")
        this.formData.x = x.slice(0, i+4);
      }
      if(z !== '' & checkFloat(z)) {
        let i = z.indexOf(".")
        this.formData.z = z.slice(0, i+4);
      }

      this.selectedType = checkIncludesReversed(graph, this.graphTypeOptions);
      this.graphSettings.gradientName = checkGradient(gradient);

      if(this.selectedType !== this.t('orbit.graph_poincare')){
        this.graphSettings.parameter = checkParameter(color_param, this.highlightionParameters);

        if(this.graphSettings.parameter === this.t('parameters.3rd_coord') && this.selectedType === this.t('orbit.graph_3d')){
          this.graphSettings.parameter = this.t('parameters.abs_v');
        }
      }
      else{
        this.formData.plane = checkIncludes(plane, this.planeOptions);
      }
      if(this.selectedType === this.t('orbit.graph_3d')){
        var isBinary = 1; 
        for(var i = 0; i < settings.length; ++i){
          if(settings.charAt(i) !== '0' & settings.charAt(i) !== '1'){
            isBinary = 0;
          }
        }
        if(isBinary & settings.length === 4){
          this.graph3DSettings = settings;
        }
        else{
          this.graph3DSettings = '1111';
        }
      }

      if(this.$route.fullPath === '/orbit') this.updateUrl();
    },
    handlePanelToggle(isHidden){ //следим за движением панели
      if(isHidden){
        this.labelsShift = 0;
      }
      else{
        this.labelsShift = 370;
      }
    },
    getAxisNames(){ //для выбранной плоскости получаем подписи осей(для Пуанкаре)
      var plane = this.formData.plane;
      if(plane == 'x = 0'){ return ['Y', 'Z']; }
      if(plane == 'y = 0'){ return ['X', 'Z']; }
      if(plane == 'z = 0'){ return ['X', 'Y']; }
      if(plane == 'vx = 0'){ return ['Vy', 'Vz']; }
      if(plane == 'vy = 0'){ return ['Vx', 'Vz']; }
      if(plane == 'vz = 0'){ return ['Vx', 'Vy']; }
      return ['', ''];
    },
    isDisabled(){ //блокируем состояние кнопки, пока необходимые поля не заполнены
      if(this.formData.x === '' || this.formData.z === ''){
        return true;
      }

      if(this.selectedType !== this.t('orbit.graph_poincare') && this.graphSettings.parameter === undefined){
        return true;
      }

      if(this.selectedType === this.t('orbit.graph_poincare') && this.formData.plane === ''){
        return true;
      }

      return false;
    },
    async fetchTrajectoryData(resetSelectedPoints=false) { //запрашиваем данные для проекций и графика в 3D
      if(resetSelectedPoints) this.graphSettings.selectedPoints = []

      this.pageState = 'Loading';   
      try {
        let response = await fetch(`${this.$AppURL}/orbit_view/get_nearest_orbit?x=${this.formData.x}&z=${this.formData.z}`);
        
        if (!response.ok) {
          throw new Error(`статус запроса: ${response.status}`);
        }
      
        let data = await response.json();
        this.orbitInfo = OrbitTemplate.parse(data);
        let filter = `[{"log_op":"NONE", "filters":[{"field":"orbit_id","op":"==", "value": ${this.orbitInfo.orbit_id}}]}]`

        response = await fetch(`${this.$AppURL}/trajectory_points/get_chunk?filter_groups=${filter}`);

        if (!response.ok) {
          throw new Error(`статус запроса: ${response.status}`);
        }

        data = await response.json();
        let points = ChunkArrayTemplate.parse(data);

        if(points.length === 0){
          this.pageState = 'noPointsError';
        }
        
        var parameter = this.highlightionParameters[this.graphSettings.parameter]
        if(this.selectedType === this.t('orbit.graph_projections')){
          this.infoForPopUp = getAbsVFor2ndPageProjections(points);
          let processedPoints = processProjections(points, parameter);
          this.xyProjection = processedPoints[0];
          this.xzProjection = processedPoints[1];
          this.yzProjection = processedPoints[2];
        }
        else{
          this.orbitTrajectory = processOrbit(points, parameter);
        }
        this.getPrevNextOrbits();
        this.pageState = 'OK';
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
    async fetchPoincareData(resetSelectedPoints=false) { //запрашиваем данные для сечения Пуанкаре
      if(resetSelectedPoints) this.graphSettings.selectedPoints = []

      this.pageState = 'Loading';
      try {
        const filter = `x=${this.formData.x}&z=${this.formData.z}&plane=${this.formData.plane}`;
        let response = await fetch(`${this.$AppURL}/orbit_poincare_view/get_nearest_section?${filter}`);
        
        if (!response.ok) {
          throw new Error(`статус запроса: ${response.status}`);
        }

        let data = await response.json();
        data = PoincareTemplate.parse(data);
        this.infoForPopUp = getAbsVFor2ndPagePoincare(this.formData.plane, data);
        this.fetchedData = processPointsForPoincare(data, this.formData.plane);
        let paramValue = data[this.highlightionParameters[this.graphSettings.parameter]];
        this.fetchedData = [...this.fetchedData, new Array(data.points_count).fill(paramValue)];

        //получаем еще информацию об орбите
        response = await fetch(`${this.$AppURL}/orbit_view/get_nearest_orbit?x=${this.formData.x}&z=${this.formData.z}`);
        
        if (!response.ok) {
          throw new Error(`статус запроса: ${response.status}`);
        }
      
        data = await response.json();
        this.orbitInfo = OrbitTemplate.parse(data);
        this.getPrevNextOrbits();
        this.pageState = 'OK';
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
    async getPrevNextOrbits(){
      let family_tag = this.orbitInfo.family_tag;
      let point = this.orbitInfo.lib_point;
      let id = this.orbitInfo.orbit_id;

      let response = await fetch(`${this.$AppURL}/orbit_view/get_next_orbit?lib_point=${point}&family_tag=${family_tag}&id=${id}`);

      if (!response.ok) {
        throw new Error(`статус запроса: ${response.status}`);
      }

      let data = await response.json();
      this.prevNextOrbit.next = NeighbourOrbitTemplate.parse(data);

      response = await fetch(`${this.$AppURL}/orbit_view/get_prev_orbit?lib_point=${point}&family_tag=${family_tag}&id=${id}`);

      if (!response.ok) {
        throw new Error(`статус запроса: ${response.status}`);
      }

      data = await response.json();
      this.prevNextOrbit.prev = NeighbourOrbitTemplate.parse(data);
    },
    updateFormdata(field, newValue){
      this.formData[field] = newValue;
    },
    drawGraphs(){
      if(this.isDisabled()) return;

      if(this.selectedType === this.t('orbit.graph_poincare')){
        this.fetchPoincareData();
      }
      else{
        this.fetchTrajectoryData();
      }
    },
    async updateOnClickData(newPopUpData, graph_type, plane){
      let x, y, z, abs_v, info;

      if(graph_type === 'projection'){
        if(plane === 'XY'){ 
          x = newPopUpData.dataX
          y = newPopUpData.dataY

          info = this.infoForPopUp['XY'][`${x}:${y}`]
          z = info.z
        }
        else if(plane === 'XZ'){ 
          x = newPopUpData.dataX
          z = newPopUpData.dataY

          info = this.infoForPopUp['XZ'][`${x}:${z}`]
          y = info.y
        }
        else {
          y = newPopUpData.dataX
          z = newPopUpData.dataY

          info = this.infoForPopUp['YZ'][`${y}:${z}`]
          x = info.x
        }
        abs_v = info.abs_v

      }
      else{
        let info = this.infoForPopUp[`${newPopUpData.dataX}:${newPopUpData.dataY}`]
        x = info['x']
        y = info['y']
        z = info['z']
        abs_v = info['abs_v']
      }

      this.popUp = {
        ...newPopUpData,
        x: x,
        y: y,
        z: z,
        abs_v: abs_v
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

h4 {
  margin: 0 0 0px 0;
  font-size: 18px;
  font-weight: 500;
  color: var(--text-primary);
}

.panel-with-scroll{
  overflow-y: auto; 
  scrollbar-color: var(--scrollbar) transparent;
}

.vertical-group {
  padding-bottom: 6px;
  display: flex;
  flex-direction: column;
  gap: 0px;
}

.horizontal-group {
  padding-bottom: 7px;
  display: flex;
  justify-content: space-between;
  gap: 7px; 
}

.coordinates-group {
  display: flex;
  justify-content: space-between;
  width: 320px;
}

.text-description{
  font-size: 16px;
  margin: 5px 0;
  color: var(--text-primary);
}

input[type="text"] {
  height: 24px;
  width: 70px;
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

input[type="button"] {
  width: 220px;
  height: 42px;
  cursor: pointer;
  background: var(--highlight-color);
  border-radius: 10px;
  border: none;
  margin-left: 50px;
  color: var(--text-button-able);
  font-size: 17px;
  position: absolute;
  box-shadow: 0px 0px 10px 10px var(--highlight-shadow);
}

input:disabled[type="button"] {
  background: var(--button-disabled);
  color: var(--text-button-disable);
}

input[type="radio"],
input[type="checkbox"] {
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
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

.checkbox-container{
  display: flex;
  justify-content: left; 
  gap: 7px;
  margin-bottom: 5px;
}

.checkbox-text{
  color: var(--text-primary);
}

.page-content {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.graph-container{
  width: 100%; 
  height: 100%;
  display: flex;
  justify-content: space-between;
}

.graph-section {
  width:  33.3333%;
  height: 100%;
}

</style>