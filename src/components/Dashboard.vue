<template>
  <div class="dashboard-container">
    <!-- Header Section -->
    <div class="dashboard-header">
      <h1>📊 管理仪表盘</h1>
      <p class="subtitle">实时数据概览 | 最后更新: {{ lastUpdateTime }}</p>
    </div>

    <!-- Stats Cards -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6" v-for="stat in statsCards" :key="stat.title">
        <el-card class="stat-card" :class="`stat-${stat.type}`">
          <div class="stat-icon">
            <el-icon :size="32"><component :is="stat.icon" /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stat.value.toLocaleString() }}</div>
            <div class="stat-label">{{ stat.title }}</div>
          </div>
          <div class="stat-trend" :class="stat.trend > 0 ? 'up' : 'down'">
            {{ stat.trend > 0 ? '↑' : '↓' }} {{ Math.abs(stat.trend) }}%
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- Charts Section -->
    <el-row :gutter="20" class="charts-row">
      <el-col :span="16">
        <el-card class="chart-card">
          <template #header>
            <span>📈 活动趋势</span>
          </template>
          <div ref="lineChartRef" class="chart-container"></div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="chart-card">
          <template #header>
            <span>🥧 任务分布</span>
          </template>
          <div ref="pieChartRef" class="chart-container"></div>
        </el-card>
      </el-col>
    </el-row>

    <!-- Recent Activity -->
    <el-card class="activity-card">
      <template #header>
        <span>🕐 最近活动</span>
      </template>
      <el-timeline>
        <el-timeline-item
          v-for="(activity, index) in recentActivities"
          :key="index"
          :timestamp="activity.time"
          :type="activity.type"
          placement="top"
        >
          <div class="activity-content">
            <strong>{{ activity.user }}</strong> {{ activity.action }}
            <el-tag size="small" :type="activity.tagType">{{ activity.tag }}</el-tag>
          </div>
        </el-timeline-item>
      </el-timeline>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { User, Document, ChatDotRound, TrendCharts } from '@element-plus/icons-vue'
import * as echarts from 'echarts'

// Reactive state
const statsCards = ref([
  { title: '总用户数', value: 12847, icon: User, type: 'primary', trend: 12.5 },
  { title: '活跃任务', value: 234, icon: Document, type: 'success', trend: 8.3 },
  { title: '代码提交', value: 1893, icon: ChatDotRound, type: 'warning', trend: -2.1 },
  { title: '完成率', value: 87.6, icon: TrendCharts, type: 'danger', trend: 5.7 }
])

const recentActivities = ref([
  { user: '张三', action: '完成了登录模块开发', tag: '功能开发', tagType: 'success', time: '10分钟前', type: 'primary' },
  { user: '李四', action: '修复了认证中间件Bug', tag: 'Bug修复', tagType: 'danger', time: '25分钟前', type: 'warning' },
  { user: '王五', action: '优化了数据库查询性能', tag: '性能优化', tagType: 'info', time: '1小时前' }
])

const lastUpdateTime = ref(new Date().toLocaleString('zh-CN'))

// Chart refs
const lineChartRef = ref(null)
const pieChartRef = ref(null)
let lineChart = null
let pieChart = null

// Initialize charts
const initCharts = () => {
  // Line chart
  if (lineChartRef.value) {
    lineChart = echarts.init(lineChartRef.value)
    lineChart.setOption({
      tooltip: { trigger: 'axis' },
      xAxis: {
        type: 'category',
        data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
      },
      yAxis: { type: 'value' },
      series: [{
        name: '活动量',
        type: 'line',
        data: [120, 200, 150, 80, 70, 110, 130],
        smooth: true,
        areaStyle: { opacity: 0.3 }
      }]
    })
  }

  // Pie chart
  if (pieChartRef.value) {
    pieChart = echarts.init(pieChartRef.value)
    pieChart.setOption({
      tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' },
      series: [{
        type: 'pie',
        radius: ['40%', '70%'],
        data: [
          { value: 735, name: '已完成' },
          { value: 310, name: '进行中' },
          { value: 234, name: '待开始' },
          { value: 135, name: '已阻塞' }
        ]
      }]
    })
  }
}

// Handle resize
const handleResize = () => {
  lineChart?.resize()
  pieChart?.resize()
}

onMounted(() => {
  initCharts()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  lineChart?.dispose()
  pieChart?.dispose()
})
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
}

.dashboard-header {
  margin-bottom: 30px;
}

.dashboard-header h1 {
  font-size: 28px;
  color: #303133;
  margin-bottom: 8px;
}

.subtitle {
  color: #909399;
  font-size: 14px;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  text-align: center;
  transition: transform 0.3s;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-icon {
  margin-bottom: 10px;
  color: #409EFF;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 5px;
}

.stat-trend {
  font-size: 12px;
  margin-top: 5px;
}

.stat-trend.up {
  color: #67C23A;
}

.stat-trend.down {
  color: #F56C6C;
}

.charts-row {
  margin-bottom: 20px;
}

.chart-card {
  height: 400px;
}

.chart-container {
  height: 320px;
}

.activity-card {
  margin-top: 20px;
}

.activity-content {
  display: flex;
  align-items: center;
  gap: 10px;
}
</style>
