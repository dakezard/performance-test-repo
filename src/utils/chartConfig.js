/**
 * Chart Configuration Utilities
 * Author: dakezard
 * Date: 2026-05-02
 *
 * Provides reusable chart configurations for ECharts
 */

export const chartColors = {
  primary: '#409EFF',
  success: '#67C23A',
  warning: '#E6A23C',
  danger: '#F56C6C',
  info: '#909399'
}

export const defaultTooltip = {
  trigger: 'axis',
  backgroundColor: 'rgba(50, 50, 50, 0.9)',
  borderColor: '#ccc',
  borderWidth: 1,
  textStyle: {
    color: '#fff'
  }
}

export const createLineChartOption = (xData, yData, title = '') => ({
  tooltip: defaultTooltip,
  title: {
    text: title,
    left: 'center'
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: xData
  },
  yAxis: {
    type: 'value'
  },
  series: [{
    name: title || '数据',
    type: 'line',
    data: yData,
    smooth: true,
    areaStyle: {
      color: {
        type: 'linear',
        x: 0,
        y: 0,
        x2: 0,
        y2: 1,
        colorStops: [
          { offset: 0, color: 'rgba(64, 158, 255, 0.3)' },
          { offset: 1, color: 'rgba(64, 158, 255, 0.05)' }
        ]
      }
    },
    itemStyle: { color: chartColors.primary }
  }]
})

export const createPieChartOption = (data, title = '') => ({
  tooltip: {
    trigger: 'item',
    formatter: '{b}: {c} ({d}%)'
  },
  legend: {
    orient: 'vertical',
    left: 'left'
  },
  series: [{
    name: title || '分布',
    type: 'pie',
    radius: ['35%', '65%'],
    avoidLabelOverlap: false,
    label: {
      show: true,
      formatter: '{b}\n{d}%'
    },
    emphasis: {
      label: {
        show: true,
        fontSize: 14,
        fontWeight: 'bold'
      }
    },
    data: data
  }]
})

export const createBarChartOption = (categories, values, title = '') => ({
  tooltip: defaultTooltip,
  title: {
    text: title,
    left: 'center'
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    data: categories
  },
  yAxis: {
    type: 'value'
  },
  series: [{
    name: title || '数值',
    type: 'bar',
    data: values,
    itemStyle: {
      color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
        { offset: 0, color: '#83bff6' },
        { offset: 1, color: '#06f' }
      ])
    },
    emphasis: {
      itemStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: '#2378f7' },
          { offset: 1, color: '#00bfff' }
        ])
      }
    }
  }]
})

console.log('Chart configuration utilities loaded!')
