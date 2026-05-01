<template>
  <div class="dashboard">
    <h1>Dashboard</h1>
    <div class="stats-grid">
      <div class="stat-card">
        <h3>Total Users</h3>
        <p>{{ stats.totalUsers }}</p>
      </div>
      <div class="stat-card">
        <h3>Active Sessions</h3>
        <p>{{ stats.activeSessions }}</p>
      </div>
      <div class="stat-card">
        <h3>Revenue</h3>
        <p>${{ stats.revenue }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const stats = ref({
  totalUsers: 0,
  activeSessions: 0,
  revenue: 0
})

onMounted(async () => {
  const response = await fetch('/api/dashboard/stats')
  stats.value = await response.json()
})
</script>

<style scoped>
.dashboard { padding: 20px; }
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; }
.stat-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
</style>
