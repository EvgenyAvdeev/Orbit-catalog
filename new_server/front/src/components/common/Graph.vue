<template>
  <div class="chart-container">
    <div @click="captureElement" class="save-btn"></div>
    <div ref="graphContainer" class="graph"></div>
    <canvas ref="overlayCanvas" @click="handleCanvasClick"></canvas>
  </div>
</template>

<script>
import { commonAxisSettings, grid, commonTitles, series, lineSeries, datazoom, visualMap, brush, toolboxFeature, toolbox, background } from "../../constants/graphSettings.js"
import { Gradients } from "../../constants/gradients.js"
import html2canvas from 'html2canvas';

export default {
  emits: ['point-clicked', 'brush-cleared'],
  props: {
    data: {
      type: Array,
      default: () => []
    },
    shift: {
      type: Number,
      default: 0
    },
    gradientName: {
      type: String,
      default: 'Winter'
    },
    selectedPoints: {
      type: Array,
      default: []
    },
    width: {
      type: String,
      default: '1000px'
    },
    height: {
      type: String,
      default: '500px'
    },
    xAxesName: {
      type: String,
      default: ''
    },
    yAxesName: {
      type: String,
      default: ''
    },
    gaps: {
      type: Array,
      default: []
    },
    showLine: {
      type: Boolean,
      default: true
    },
    factor: {
      type: Number,
      default: 10
    }
  },
  data() {
    return {
      chart: null,
      densityArrays: [],
      xAxis: { min: 0, max: 0 },
      yAxis: { min: 0, max: 0 },
      valuesLimits: { min: 0, max: 0 },
      currZoomLvl: 7,
      nearestPoint: undefined,
      options: undefined,
      hasBrushSelection: false
    }
  },
  inject: ['theme'],
  watch: {
    data: {
      handler(data) {
        this.currZoomLvl = 7;
        if(data[0].length>=0) {
          if(this.showLine){
            this.processDataIfLine(data);
          }
          else{
            this.processDataNoLine(data);
          }
        }

        this.hasBrushSelection = false;
        this.updateChart(this.shift, this.gradientName, true);
        this.$nextTick(() => {
          this.setInitialZoom();
        });
      },
      deep: true
    },
    shift: {
      handler(shift) {
        this.updateChart(shift, this.gradientName);
      },
      deep: true
    },
    gradientName: {
      handler(gradientName) {
        this.updateChart(this.shift, gradientName);
      },
      deep: true
    },
    'theme.currentTheme': {
      handler() {
        this.updateChart(this.shift, this.gradientName);
      },
      deep: true,
      immediate: true
    }
  },
  mounted() {
    this.start = Date.now();
    this.initOverlay();
    this.initChart();
    window.addEventListener("resize", this.updateSizes);
  },  
  beforeUnmount() {
    if (this.chart) {
      this.chart.dispose();
      window.removeEventListener("resize", this.updateSizes);
    }
  },
  methods: {
    async captureElement() {
      try {
        const element = this.$refs.graphContainer;
        
        const canvas = await html2canvas(element, {
          scale: 2, 
          backgroundColor: null, 
          useCORS: true,
          logging: false
        });

        const imageData = canvas.toDataURL('image/png');
        this.capturedImage = imageData;
        
        const link = document.createElement('a');
        link.href = imageData;
        link.download = 'graph.png';
        
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
      } catch (error) {
        console.error('Ошибка при создании скриншота:', error);
      }
    },
    updateSizes() {
      this.chart.resize();

      let canvas = this.$refs.overlayCanvas;
      const container = this.$refs.graphContainer;
      const rect = container.getBoundingClientRect();
      
      canvas.width = rect.width;
      canvas.height = rect.height;
      canvas.style.width = rect.width + 'px';
      canvas.style.height = rect.height + 'px';
    },
    initChart() {
      if (this.chart) {
        this.chart.dispose();
      }
      
      const container = this.$refs.graphContainer;
      if (!container) return;
      
      this.chart = echarts.init(container, null, { 
        renderer: 'webgl',
        devicePixelRatio: 1
      });

      this.chart.on('dataZoom', (params) => { 
        if (this.hasBrushSelection) {
          this.clearBrushSelection();
          this.hasBrushSelection = false;
        }

        let x_zoom = params['batch'][0]['end'] - params['batch'][0]['start'], y_zoom;
        if(params['batch'][1] !== undefined) y_zoom = params['batch'][1]['end'] - params['batch'][1]['start'];
        else y_zoom = 100;
        
        var zoom = (Math.abs(x_zoom));
        
        var startZoom = [0, 0.01, 0.03, 0.1, 0.3, 1, 2, 4, 9, 15, 40, 70];
        var endZoom = [0.01, 0.03, 0.1, 0.3, 1, 2, 4, 9, 15, 40, 70, 100];

        if(!zoom){
          zoom = (params['batch'][0]['endValue'] - params['batch'][0]['startValue'])/(this.xAxis.max - this.xAxis.min)
          zoom *= 100
        }

        if((this.currZoomLvl != 7) && (endZoom[this.currZoomLvl+4] < zoom*162)){
          this.currZoomLvl+=1;
          this.updateChart(this.shift, this.gradientName);
          return;
        }
        else if((this.currZoomLvl != -4) && (startZoom[this.currZoomLvl+4] > zoom*162)){
          this.currZoomLvl-=1;
          this.updateChart(this.shift, this.gradientName);
          return;
        }

        if(this.showLine){
          const newPoints = this.updateLineByViewport()

          this.chart.setOption({
            series: [{
              id: 'line',
              data: newPoints,
              connectNulls: false
            }]
          }, { lazyUpdate: true })
        }
      });
      
      this.chart.on('brushEnd', (params) => {
        if (params.areas && params.areas.length > 0) {
          this.hasBrushSelection = true;
        }

        if (params.command === 'clear') {
          this.hasBrushSelection = false;
          this.$emit('brush-cleared');
        }
      });

      container.addEventListener('contextmenu', this.handleCanvasClick);

      this.updateChart(this.shift, this.gradientName);
    },
    initOverlay() {
      const canvas = this.$refs.overlayCanvas;
      if (!canvas) return;
      
      this.updateOverlaySize();
    },
    updateOverlaySize() {
      let canvas = this.$refs.overlayCanvas;
      if (!canvas || !this.$refs.graphContainer) return;
      
      const container = this.$refs.graphContainer;
      const rect = container.getBoundingClientRect();
      
      canvas.width = rect.width;
      canvas.height = rect.height;
      canvas.style.width = rect.width + 'px';
      canvas.style.height = rect.height + 'px';
    },
    handleCanvasClick(event) {
      let largest = this.densityArrays[0];
      if (!this.chart || largest.length === 0) return;

      event.preventDefault();
      
      const rect = this.$refs.overlayCanvas.getBoundingClientRect();
      const clickX = event.clientX - rect.left;
      const clickY = event.clientY - 60;
      const [x, y] = this.chart.convertFromPixel({ seriesIndex: 0 }, [clickX, clickY]);

      //ищем ближайшую точку из имеющихся
      var width = this.xAxis.max - this.xAxis.min;
      var height = this.yAxis.max - this.yAxis.min;
      var proportion = this.$refs.overlayCanvas.width / this.$refs.overlayCanvas.height;

      var [ nearX, nearY, value ] = largest[0];
      let shrtDist = Math.sqrt((((nearX-x)/width)*proportion)**2+((nearY-y)/height)**2);

      for(let i = 1; i < largest.length; ++i){
        let dist = Math.sqrt((((largest[i][0]-x)/width)*proportion)**2+((largest[i][1]-y)/height)**2);

        if(dist<shrtDist){
          shrtDist = dist;
          nearX = largest[i][0];
          nearY = largest[i][1];
          value = largest[i][2];
        }
      }

      this.nearestPoint = [ nearX, nearY, value ];

      let pointInPixels = this.chart.convertToPixel({
        xAxisIndex: 0,
        yAxisIndex: 0
      }, [nearX, nearY]);

      pointInPixels = [pointInPixels[0] + rect.left, pointInPixels[1]+60];
      
      this.$emit('point-clicked', { dataX: nearX, dataY: nearY, dataXInPixels: pointInPixels[0], dataYInPixels: pointInPixels[1],
                    popUpX: event.clientX, popUpY: event.clientY, xAxesName: this.xAxesName, yAxesName: this.yAxesName, color_value: value });
      
      this.updateChart(this.shift, this.gradientName);
    },
    clearBrushSelection() {
      if (this.chart) {
        this.chart.dispatchAction({
          type: 'brush',
          areas: []
        });
      }
    },
    updateLineByViewport() {
      const opt = this.chart.getOption()
      if(!opt) return;

      const dz = opt.dataZoom[0]
      const dz2 = opt.dataZoom[1]

      const xMin = dz.startValue
      const xMax = dz.endValue

      var yMin, yMax;
      if(dz2){
        yMin = dz2.startValue
        yMax = dz2.endValue
      }
      else{
        yMin = -1000000000
        yMax = 1000000000
      }

      if(this.densityArrays.length > 0){
        if(this.currZoomLvl===-4){
          var src = this.densityArrays[0];
        }
        else{
          var src = this.densityArrays[4+this.currZoomLvl-1];
        }
      }
      if(src.length === 0) return []

      const visible = []

      for (let i = 0; i < src.length; i++) {
        const x = src[i][0]
        const y = src[i][1]

        if(!x) visible.push(src[i])

        if (x >= xMin && x <= xMax && y >= yMin && y <= yMax) {
          visible.push(src[i])
        }
      }

      let points = this.insertNullsByDistance(visible, this.factor)
      return points
    },
    insertNullsByDistance(points, factor) {
      if (!points || points.length < 5) return points

      const xRange = this.xAxis.max - this.xAxis.min
      const yRange = this.yAxis.max - this.yAxis.min
      if (!xRange || !yRange) return points

      let distances = []
      for (let i = 1; i < points.length; i++) {
        const p1 = points[i - 1]
        const p2 = points[i]
        if (!p1 || !p2 || p1[0] == null || p2[0] == null) continue

        const dx = (p2[0] - p1[0])
        const dy = (p2[1] - p1[1])
        distances.push(Math.sqrt(dx * dx + dy * dy))
      }

      if (!distances.length) return points

      distances = [...distances].sort((a, b) => a - b);
      let middle = Math.floor(distances.length / 2);

      const threshold = distances[middle] * factor

      const result = [points[0]]
      for (let i = 1; i < points.length; i++) {
        const prev = points[i - 1]
        const curr = points[i]

        if (prev && curr && prev[0] != null &&curr[0] != null) {
          const dx = (curr[0] - prev[0])
          const dy = (curr[1] - prev[1])
          const dist = Math.sqrt(dx * dx + dy * dy)

          if (dist > threshold) {
            result.push([undefined, undefined])
          }
        }
        
        result.push(curr)
      }

      return result
    },
    updateChart(shift, gradientName, dataChanged = false) {
        if (!this.chart) return;
        if(dataChanged) {
          this.nearestPoint = undefined;

          this.chart.dispatchAction({
            type: 'dataZoom',
            xAxisIndex: 0, 
            start: 30,     
            end: 70,
            batch: [
              { start: 0, end: 100},
              { start: 0, end: 100}
            ] 
          });
        }

        if(this.densityArrays.length > 0){
          var points = this.densityArrays[4+this.currZoomLvl];
        }
        else {
          var points = [];
        }

        if(points.length<=10) var pointSize = 6;
        else var pointSize = 4;
        
        var xAxis = Object.assign({}, this.xAxis, structuredClone(commonAxisSettings()));
        var yAxis = Object.assign({}, this.yAxis, structuredClone(commonAxisSettings()));
        yAxis.axisLabel.padding = [0, 0, 0, shift];
        const hasData = points.length > 0;

        if(xAxis.min != 0){
          xAxis.axisLabel.showMinLabel = false
        }
        if(yAxis.min != 0){
          yAxis.axisLabel.showMinLabel = false
        }

        let seriesArray = [{
            data: this.selectedPoints,
            large: true,
            symbolSize: pointSize+6,
            itemStyle: {
              color: 'red',
              opacity: 0.7
            },
            dimensions: ['x', 'y'],
            type: 'scatterGL',
            zlevel: 50,
            z: 50,
            ...series,
          },
          {
            data: points,
            symbolSize: pointSize,
            clip: true,
            emphasis: {
                disabled: true
            },
            largeThreshold: 50000,
            progressive: 50000,
            progressiveThreshold: 50000,
            zlevel: 2,
            type: 'scatterGL',
            dimensions: ['x', 'y', 'value'],
            ...series
          },
          {
            data: this.nearestPoint === undefined ? [] : [ this.nearestPoint ],
            symbolSize: pointSize+4,
            dimensions: ['x', 'y', 'value'],
            ...series,
            itemStyle: {
              opacity: 1
            },
            type: 'scatterGL',
            zlevel: 40,
            z: 40,
          }
        ]

        if (this.showLine) {
          const currColors = this.theme.getCurrentValues()
         
          const linePoints = this.updateLineByViewport()
          seriesArray.push({
            id: 'line',
            data: linePoints,
            showSymbol: false,
            lineStyle:{ width: pointSize, color: currColors['--line-color'] },
            ...lineSeries
          })
        }

        const baseOptions = {
          animation: false,
          ...background(),
          grid: {
              ...grid,
              width: this.width, 
              height: this.height 
          },
          xAxis: xAxis,
          yAxis: yAxis,
          title: [{
              text: this.xAxesName,
              right: '5px',
              bottom: '15px',
              ...commonTitles()
            }, {
              padding: [0, 0, 0, shift],
              text: this.yAxesName,
              
              left: '10px',
              top: '7px',
              ...commonTitles()
            }
          ],
          series: seriesArray,
          brush: brush,

          dataZoom: [
                        {
            ...datazoom,
            filterMode: 'filter',
            xAxisIndex: 0,
            zoomLock: !hasData,
            disabled: !hasData,
            seriesIndex: [0, 1, 2]
          }, {
            ...datazoom,
            filterMode: 'filter',
            yAxisIndex: 0,
            zoomLock: !hasData,
            disabled: !hasData,
            seriesIndex: [0, 1, 2]
          },
        {
            ...datazoom,
            filterMode: 'none',
            xAxisIndex: 0,
            zoomLock: !hasData,
            disabled: !hasData,
            seriesIndex: [3]
          }, {
            ...datazoom,
            filterMode: 'none',
            yAxisIndex: 0,
            zoomLock: !hasData,
            disabled: !hasData,
            seriesIndex: [3]
          }
        ],

          toolbox: {
            show: hasData,
            feature: toolboxFeature,
            ...toolbox()
          },
          visualMap: {
            ...visualMap(),
            dimension: [2],
            min: this.valuesLimits.min,
            max: this.valuesLimits.max,
            inRange: {
              color: Gradients[gradientName]
            },
            seriesIndex: [1, 2]
          }
        };
      this.options = baseOptions;
      
      this.chart.setOption(baseOptions);
    },
    calculate(data){
      var x = data[0], y = data[1];

      if(data.length > 2){
        var values = data[2];
      }
      else{
        var values = y;
      }

      if(values.length>0){
        var valuesMin = values[0], valuesMax = values[0];
      }
      else{
        var valuesMin = 0, valuesMax = 0;
      }

      var xAxis = {min: x[0], max: x[0]}, yAxis = {min: y[0], max: y[0]};

      for(let i = 0; i<x.length; ++i){        
        valuesMin = Math.min(valuesMin, values[i]);
        valuesMax = Math.max(valuesMax, values[i]);
        xAxis.min = Math.min(xAxis.min, x[i]);
        xAxis.max = Math.max(xAxis.max, x[i]);
        yAxis.min = Math.min(yAxis.min, y[i]);
        yAxis.max = Math.max(yAxis.max, y[i]);
      }

      if(xAxis.min == xAxis.max){
        if(xAxis.min == 0){
          xAxis.min = -1;
          xAxis.max = 1;
        }
        else if(xAxis.min<0){
          xAxis.min = xAxis.min * 1.15;
          xAxis.max = xAxis.max * 0.85;
        }
        else{
          xAxis.min = xAxis.min * 0.85;
          xAxis.max = xAxis.max * 1.15;
        }
      }
      else{
        let dist = xAxis.max - xAxis.min;
        xAxis.min = xAxis.min - dist * 104.5;
        xAxis.max = dist * 104.5 + xAxis.max;
      }
      if(yAxis.min == yAxis.max){
        if(yAxis.min == 0){
          yAxis.min = -1;
          yAxis.max = 1;
        }
        else if(yAxis.min<0){
          yAxis.min = yAxis.min * 1.15;
          yAxis.max = yAxis.max * 0.85;
        }
        else{
          yAxis.min = yAxis.min * 0.85;
          yAxis.max = yAxis.max * 1.15;
        }
      }
      else{
        let dist = yAxis.max - yAxis.min;
        yAxis.min = yAxis.min - dist * 104.5;
        yAxis.max = dist * 104.5 + yAxis.max;
      }

      this.xAxis = xAxis;
      this.yAxis = yAxis;
      this.valuesLimits = { min: valuesMin, max: valuesMax };
    },
    processDataIfLine(data) {
      this.calculate(data);
      if(data[0].length===0){
        for(let i = 0; i<12; ++i){
          this.densityArrays[i] = new Array();
        }
        return
      }
      var dataWithGaps = new Array(data[0].length + this.gaps.length);
      let p = 0;
      for(var i = 0; i < data[0].length; ++i){
        if(this.gaps.includes(i)){
          dataWithGaps[p] = [undefined, undefined, undefined];
          ++p;
        }
        dataWithGaps[p] = [ data[0][i], data[1][i], data[2][i] ];
        p++;
      }

      this.densityArrays = new Array(12);
      for(let i = 0; i<12; ++i){
        this.densityArrays[i] = new Array(dataWithGaps.length);
        this.densityArrays[i][0] =  dataWithGaps[0];
      }

      let pointers = new Array(12).fill(1)
      let dists = [0, 0.0000001, 0.0000002, 0.0000004, 0.000001, 0.0000025, 0.000006, 0.00001, 0.000015, 0.00002, 0.00005, 0.00007]

      var width = this.xAxis.max - this.xAxis.min;
      var height = this.yAxis.max - this.yAxis.min;
      var proportion = this.$refs.overlayCanvas.width / this.$refs.overlayCanvas.height;

      var flags = new Array(12).fill(0);
      for(let i = 1; i<dataWithGaps.length; ++i){
        const [ x, y, val ] = dataWithGaps[i];

        for(let j = 0; j<12; ++j){
          if(x===undefined && y===undefined && val===undefined){
            this.densityArrays[j][pointers[j]] = [x, y, val];
            pointers[j]+=1;
            continue;
          }

          let prev_x, prev_y;
          if(this.densityArrays[j][pointers[j]-1][0]===undefined){
            let s = Math.max(j-6, 0)
            if(Math.floor(i/2)%(2**Math.floor((j+1)/2)) === 0 ){
              this.densityArrays[j][pointers[j]] = [x, y, val]
              pointers[j]+=1
              flags[j]+=1
            }
            continue
          }
          else{
            prev_x = this.densityArrays[j][pointers[j]-1][0];
            prev_y = this.densityArrays[j][pointers[j]-1][1];
          }

          var dist = Math.sqrt(((x-prev_x)/width*proportion)**2 + ((y-prev_y)/height)**2);

          if(dist >= dists[j]){
            this.densityArrays[j][pointers[j]] = [x, y, val]
            pointers[j]+=1
          }
        }
      }

      for(let i = 0; i<this.densityArrays.length; ++i){
        this.densityArrays[i].length = pointers[i]
        console.log(flags[i])
      }
    },
    processDataNoLine(data) {
      this.calculate(data);
      
      const densityLevels = [
        { step: 0.00001, array: [] },
        { step: 0.00002, array: [] },
        { step: 0.00005, array: [] },
        { step: 0.0001, array: [] },
        { step: 0.0002, array: [] },
        { step: 0.0005, array: [] },
        { step: 0.001, array: [] },
        { step: 0.002, array: [] },
        { step: 0.005, array: [] },
        { step: 0.01, array: [] },
        { step: 0.02, array: [] }
      ];
      
      var largest = [];
      
      const width = (this.xAxis.max - this.xAxis.min)/210;
      const height = (this.yAxis.max - this.yAxis.min)/210;
      
      //будем использовать квадродерево для прореживания по плотности
      const quadTrees = densityLevels.map(() => new Map());
      
      for (let i = 0; i < data[0].length; ++i) {
        const x = data[0][i];
        const y = data[1][i];
        const val = data[2][i];
        
        largest.push([x, y, val]);
        
        for (let j = 0; j < densityLevels.length; ++j) {
          const level = densityLevels[j];
          const quadTree = quadTrees[j];
          
          //получаем координату ячейки
          const coordx = Math.floor(x / (level.step * width));
          const coordy = Math.floor(y / (level.step * height));
          const key = `${coordx},${coordy}`;
          
          if (!quadTree.has(key)) { //если в этой ячейке еще нет точек, то добавим текущую
            level.array.push([x, y, val]);
            quadTree.set(key, [x, y]);
          } 
        }
      }
      
      this.densityArrays = [largest].concat(densityLevels.map(level => level.array));
    },
    setInitialZoom(){
      if (!this.chart) return;
      
      this.chart.dispatchAction({
        type: 'dataZoom',
        batch: [
          { xAxisIndex: 0, start: 49.690476, end: 50.309523 },
          { yAxisIndex: 0, start: 49.690476, end: 50.309523 }
        ] 
      });
    }
  }
}
</script>

<style scoped>

.save-btn{
  cursor: pointer; 
  background-color: rgba(255,0,0,0);
  height: 21px;
  width: 21px;
  position: absolute;
  top: 5px;
  right: 86px;
  z-index: 1000;
}
  
.chart-container {
  position: relative; 
  width: 100%; 
  height: 100%
}

.graph{
  width: 100%; 
  height: 100%
}

.chart-container canvas {
  position: absolute;
  top: 0%;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  cursor: pointer;
}
</style>
