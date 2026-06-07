import { useTheme } from '../setTheme.js'

export function commonAxisSettings() {
  const themeManager = useTheme()
  const currColors = themeManager.getCurrentValues()
  
  return {
    axisLabel: { 
        inside: true, 
        fontSize: 12,
        textBorderColor: currColors['--labels-shadow-color'], 
        textBorderWidth: 3,         
        textBorderType: 'solid', 
        showMaxLabel: false,
        color: currColors['--labels-color'],
    },
    axisLine: {
        show: true,
        lineStyle: {
            color: currColors['--axis-color'],    
            width: 1.5,         
            type: 'solid', 
        }
    },
    splitLine: {
      lineStyle: {
        color: currColors['--grid-color']
      }
    },
    minorTick: { 
        show: true
    },
    minorSplitLine: { 
        show: true,
        lineStyle: {
            color: currColors['--minor-grid-color']
        }
    }
  };
}

export function background() {
  const themeManager = useTheme()
  const currColors = themeManager.getCurrentValues()
  
  return {
    backgroundColor: currColors['--bg-primary']
  }
}

export function commonTitles() {
  const themeManager = useTheme()
  const currColors = themeManager.getCurrentValues()
  
  return {
    textStyle: {
        fontSize: 15,
        fontWeight: '500',
        color: currColors['--labels-color']
    },
    zlevel: 10
  }
}

export function visualMap() {
  const themeManager = useTheme()
  const currColors = themeManager.getCurrentValues()
  
  return {
    orient: 'vertical',
    zlevel: 99,
    z: 99,
    right: 10,
    top: 'center',
    text: ['Max', 'Min'],
    calculable: true,
    textStyle: {
        color: currColors['--labels-color'],
        textBorderColor: currColors['--labels-shadow-color'], 
        textBorderWidth: 3
    },
    formatter: function (value) {
        return value.toFixed(2);
    }
  }
}

export function toolbox() {
  const themeManager = useTheme()
  const currColors = themeManager.getCurrentValues()
  
  return {
    iconStyle: {
      borderColor: currColors['--icons-color']
    }
  }
}

export function common3DAxis() {
  const themeManager = useTheme()
  const currColors = themeManager.getCurrentValues()
  
  return {
    axisLine: {
        lineStyle: {
        color: currColors['--axis-color'],    
        }
    },
    splitLine: {
        lineStyle: {
            color: currColors['--grid-color']
        }
    }
  }
}

export function common3DLabels() {
  const themeManager = useTheme()
  const currColors = themeManager.getCurrentValues()
  
  return {
    fontWeight: '100',
    color: currColors['--labels-color']
  }
}

export function lineStyle() {
  const themeManager = useTheme()
  const currColors = themeManager.getCurrentValues()
  
  return {
    type: 'line',
    showSymbol: false,
    clip: false,
    xAxisIndex: 1,
    yAxisIndex: 1,
    itemStyle: { color: currColors['--broucke-lines-color'] }
  }
}

export const grid = {
    left: '5px',
    right: 0,
    top: '-5px',
    bottom: 0,
    containLabel: true
}

export const series = {
    connectNulls: false,
    dimensions: ['x', 'y', 'value'],
}

export const lineSeries = {
    connectNulls: false,
    dimensions: ['x', 'y', 'value'],
    // clip: true,
    emphasis: {
        disabled: true,
        itemStyle: {
            color: 'transparent'
        }
    },
    largeThreshold: 50000,
    progressive: 50000,
    progressiveThreshold: 50000,
    zlevel: 1,
    type: 'line'
}

export const datazoom = {
    type: 'inside',
}

export const brush = {
    throttleType: 'debounce',
    throttleDelay: 300,
    toolbox: ['rect', 'polygon', 'clear'],
    xAxisIndex: [0],
    yAxisIndex: [0]
}

export const toolboxFeature = {
    dataZoom: [
        {
            xAxisIndex: [0],
            yAxisIndex: [0],
        },
        {
            xAxisIndex: [1],
            yAxisIndex: [1], 
        }
    ],
    saveAsImage: {
        name: 'Graph',
        type: 'png',
        title: 'Save Image',
        excludeComponents: ['toolbox', 'dataZoom', 'visualMap'],
        pixelRatio: 2
    }
}