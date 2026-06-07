<template>
  <div ref="graphContainer" style="width: 100%; height: 100%"></div>
</template>

<script>
import { Gradients } from "../../constants/gradients.js"
import { common3DAxis, common3DLabels, visualMap } from "../../constants/graphSettings.js"

export default {
  props: {
    data: {
      type: Array,
      default: () => []
    },
    settings: {
      type: String,
      default: '1111'
    },
    gradientName: {
      type: String,
      default: 'Winter'
    },
    width: {
      type: String,
      default: '1000px'
    },
    height: {
      type: String,
      default: '500px'
    }
  },
  data() {
    return {
      chart: null,
      options: undefined
    }
  },
  inject: ['theme'],
  watch: {
    data: {
      handler(newData) {
        this.updateChart(newData, this.settings, this.gradientName);
      },
      deep: true
    },
    settings: {
      handler(newSettings) {
        this.updateChart(this.data, newSettings, this.gradientName);
      },
      deep: true
    },
    gradientName: {
      handler(gradientName) {
        this.updateChart(this.data, this.settings, gradientName);
      },
      deep: true
    },
    'theme.currentTheme': {
      handler() {
        this.updateChart(this.data, this.settings, this.gradientName);
      },
      deep: true,
      immediate: true
    }
  },
  mounted() {
    this.initChart();
  },    
  beforeUnmount() {
    if (this.chart) {
      this.chart.dispose();
    }
  },
  methods: {
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
      
      this.updateChart(this.data, this.settings, this.gradientName);
    },
    updateChart(points, settings, gradientName) {
      if (!this.chart) return;
      
      if(points.length>0){
        var [xAxis3D, yAxis3D, zAxis3D, valueMin, valueMax] = this.calculate(points);
        var pointSize = 3;
      }
      else{
          var xAxis3D = yAxis3D = zAxis3D = { min: 0, max: 1 };
          var valueMin = valueMax = 0;
          var points = [[0,0]];
          var pointSize = 0;
      }

      xAxis3D = {...xAxis3D, axisLabel: { 
          formatter: function(value) {
              if (xAxis3D.min == value || xAxis3D.max == value) {
                  return '';
              }
              return value;
          },
          ...common3DLabels()
        },
        ...common3DAxis()
      }
      yAxis3D = {...yAxis3D, axisLabel: { 
          formatter: function(value) {
              if (yAxis3D.min == value || yAxis3D.max == value) {
                  return '';
              }
              return value;
          },
          ...common3DLabels()
        },
        ...common3DAxis()
      }
      zAxis3D = {...zAxis3D, axisLabel: { 
          formatter: function(value) {
              if (zAxis3D.min == value || zAxis3D.max == value) {
                  return '';
              }
              return value;
          },
          ...common3DLabels()
        },
         ...common3DAxis()
      }
        
      var projectedPoints = this.getProjectedPoints(points, settings, xAxis3D.min, yAxis3D.min, zAxis3D.min);

      if(settings[0] === "0"){
        points = [];
      }
      
      var baseOptions = {
          grid3D: {
            left: 0,
            right: 0,
            top: 0,
            bottom: 0,
            containLabel: true,
            width: this.width, 
            height: this.height,
            viewControl: {
              beta: 130
            },
            axisPointer: {
              show: false
            }
          },
          xAxis3D: xAxis3D,
          yAxis3D: yAxis3D,
          zAxis3D: zAxis3D,
          series: [
            {
            data: projectedPoints,
            type: 'scatter3D',
            symbolSize: pointSize,
            large: true,
            largeThreshold: 0,
            clip: false,
            itemStyle: {
              color: '#909090'
            }
          },  
          {
            data: points,
            type: 'scatter3D',
            symbolSize: pointSize,
            largeThreshold: 0,
            clip: false
          }
        ],
        visualMap: {
          ...visualMap(),
          dimension: 3,
          min: valueMin,
          max: valueMax,
          inRange: {
            color: Gradients[gradientName]
          }
        },
      };
      
      this.options = baseOptions;
      this.chart.setOption(baseOptions);
    },
    calculate(points){
      var xAxis3D = {min: points[0][0], max: points[0][0]};
      var yAxis3D = {min: points[0][1], max: points[0][1]};
      var zAxis3D = {min: points[0][2], max: points[0][2]};
      var valueMin = points[0][3], valueMax = points[0][3];

      for(let i = 0; i<points.length; i++){
          xAxis3D.min = Math.min(xAxis3D.min, points[i][0]);
          xAxis3D.max = Math.max(xAxis3D.max, points[i][0]);
          yAxis3D.min = Math.min(yAxis3D.min, points[i][1]);
          yAxis3D.max = Math.max(yAxis3D.max, points[i][1]);
          zAxis3D.min = Math.min(zAxis3D.min, points[i][2]);
          zAxis3D.max = Math.max(zAxis3D.max, points[i][2]);
          valueMin = Math.min(valueMin, points[i][3]);
          valueMax = Math.max(valueMax, points[i][3]);
      }

      var axis = [xAxis3D, yAxis3D, zAxis3D];
      for(var i = 0; i < axis.length; ++i){
          if(axis[i].min == axis[i].max){
              if(axis[i].min == 0){
                  axis[i].min = -1;
                  axis[i].max = 1;
              }
              else if(axis[i].min<0){
                  axis[i].min = axis[i].min * 1.15;
                  axis[i].max = axis[i].max * 0.85;
              }
              else{
                  axis[i].min = axis[i].min * 0.85;
                  axis[i].max = axis[i].max * 1.15;
              }
          }
          else{
              axis[i].min = axis[i].min - (axis[i].max - axis[i].min) * 0.15;
              axis[i].max = (axis[i].max - axis[i].min) * 0.15 + axis[i].max;
          }
      }
      return [xAxis3D, yAxis3D, zAxis3D, valueMin, valueMax];
    },
    getProjectedPoints(points, settings, xMin, yMin, zMin){
      var projectedPoints = new Array(points.length * (settings.slice(1).split('1').length-1)); 

      var addedProjections = 0;
      
      if(settings[1] === "1"){ //XY
        for(var i = 0; i < points.length; ++i){
          projectedPoints[i] = [points[i][0], points[i][1], zMin, points[i][3]];
        }
        ++addedProjections;
      }

      if(settings[2] === "1"){ //XZ
        for(var i = 0; i < points.length; ++i){
          let ind = addedProjections * points.length + i;
          projectedPoints[ind] = [points[i][0], yMin, points[i][2], points[i][3]];
        }
        ++addedProjections;
      }

      if(settings[3] === "1"){ //YZ
        for(var i = 0; i < points.length; ++i){
          let ind = addedProjections * points.length + i;
          projectedPoints[ind] = [xMin, points[i][1], points[i][2], points[i][3]];
        }
      }

      return projectedPoints;
    }
  }
}
</script>

<style scoped>
</style>