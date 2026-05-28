<script setup lang="ts">
import { ref, computed } from 'vue'

const today = new Date()
const currentYear = ref(today.getFullYear())
const currentMonth = ref(today.getMonth()) // 0-indexed

const monthName = computed(() => {
  return `${currentYear.value}年${currentMonth.value + 1}月`
})

function prevMonth() {
  if (currentMonth.value === 0) { currentMonth.value = 11; currentYear.value-- }
  else currentMonth.value--
}
function nextMonth() {
  if (currentMonth.value === 11) { currentMonth.value = 0; currentYear.value++ }
  else currentMonth.value++
}

// Compliance event days: 1, 15, last day of month
const eventDays = computed(() => {
  const daysInMonth = new Date(currentYear.value, currentMonth.value + 1, 0).getDate()
  return new Set([1, 15, daysInMonth])
})

function daysUntil(month: number, day: number): number {
  const todayMs = new Date(today.getFullYear(), today.getMonth(), today.getDate()).getTime()
  let target = new Date(today.getFullYear(), month, day)
  if (target.getTime() < todayMs) target = new Date(today.getFullYear() + 1, month, day)
  return Math.round((target.getTime() - todayMs) / 86400000)
}

const reminders = computed(() => {
  const nextMonth15 = (() => {
    const d = new Date(today.getFullYear(), today.getMonth(), 15)
    if (d.getTime() <= new Date(today.getFullYear(), today.getMonth(), today.getDate()).getTime())
      return new Date(today.getFullYear(), today.getMonth() + 1, 15)
    return d
  })()
  const taxDays = Math.round((nextMonth15.getTime() - new Date(today.getFullYear(), today.getMonth(), today.getDate()).getTime()) / 86400000)
  return [
    { label: '工商年报截止', date: '6月30日', days: daysUntil(5, 30), icon: '🏢' },
    { label: '申报纳税截止', date: '每月15日', days: taxDays, icon: '💰' },
    { label: '社保汇缴申报', date: '每月15日', days: taxDays, icon: '🛡️' },
  ]
})

const calendarDays = computed(() => {
  const year = currentYear.value
  const month = currentMonth.value
  const firstDow = new Date(year, month, 1).getDay() // 0=Sun
  const daysInMonth = new Date(year, month + 1, 0).getDate()
  const isCurrentMonth = year === today.getFullYear() && month === today.getMonth()
  const todayDate = today.getDate()

  const cells: Array<{ day: number | null; hasEvent: boolean; isToday: boolean }> = []
  for (let i = 0; i < firstDow; i++) cells.push({ day: null, hasEvent: false, isToday: false })
  for (let d = 1; d <= daysInMonth; d++) {
    cells.push({ day: d, hasEvent: eventDays.value.has(d), isToday: isCurrentMonth && d === todayDate })
  }
  return cells
})

const features = [
  {
    icon: '👤',
    title: '招人才',
    items: ['Offer letter', '录用条件确认书', '入职信息登记表'],
  },
  {
    icon: '📄',
    title: '签合同',
    items: ['劳动合同', '兼职协议', '劳务协议'],
  },
  {
    icon: '⚙️',
    title: '做管理',
    items: ['工资表', '考勤表', '考勤休假管理制度', '职工名册', '保密协议', '竞业限制协议', '员工手册/用工管理制度模板', '绩效评估报告'],
  },
  {
    icon: '🚪',
    title: '办离职',
    items: ['员工离职审批表', '离职证明', '终止劳动合同通知书'],
  },
]
</script>

<template>
  <div class="legal-page">
    <div class="two-col">
      <!-- Contract generation -->
      <section>
        <h2 class="section-title">高频合同与文书</h2>
        <div class="contract-list">
          <div v-for="f in features" :key="f.title" class="contract-card">
            <div class="group-header">
              <span class="group-icon">{{ f.icon }}</span>
              <span class="group-title">{{ f.title }}</span>
            </div>
            <div class="pill-row">
              <button v-for="item in f.items" :key="item" class="pill">{{ item }}</button>
            </div>
          </div>
        </div>
      </section>

      <!-- Compliance calendar -->
      <section>
        <div class="section-header">
          <h2 class="section-title" style="margin:0">合规日历</h2>
          <button class="link-btn">查看全部</button>
        </div>
        <div class="calendar-card">
          <div class="cal-nav">
            <span class="cal-month">{{ monthName }}</span>
            <div class="cal-btns">
              <button class="cal-btn" @click="prevMonth">‹</button>
              <button class="cal-btn" @click="nextMonth">›</button>
            </div>
          </div>
          <div class="cal-grid">
            <div v-for="d in ['日','一','二','三','四','五','六']" :key="d" class="cal-weekday">{{ d }}</div>
            <div
              v-for="(cell, i) in calendarDays"
              :key="i"
              :class="['cal-day', { event: cell.hasEvent && !cell.isToday, today: cell.isToday, empty: !cell.day }]"
            >
              {{ cell.day ?? '' }}
            </div>
          </div>
          <div class="cal-legend">
            <span class="legend-item"><span class="dot event-dot"></span>待办事项</span>
            <span class="legend-item"><span class="dot today-dot"></span>今日</span>
            <span class="legend-note">状态标记：已完成 / 进行中 / 已逾期</span>
          </div>
          <div class="reminders">
            <div v-for="r in reminders" :key="r.label" class="reminder-item">
              <span class="reminder-icon">{{ r.icon }}</span>
              <div class="reminder-info">
                <span class="reminder-label">{{ r.label }}</span>
                <span class="reminder-date">{{ r.date }}</span>
              </div>
              <span :class="['reminder-days', r.days <= 7 ? 'urgent' : r.days <= 15 ? 'soon' : '']">
                {{ r.days === 0 ? '今天截止' : `还有 ${r.days} 天` }}
              </span>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<style scoped>
.legal-page { display: flex; flex-direction: column; gap: 24px; }
.two-col { display: grid; grid-template-columns: 1fr 570px; gap: 20px; align-items: stretch; }
.two-col > section { display: flex; flex-direction: column; }
.two-col > section:last-child .calendar-card { flex: 1; }

.section-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px; }
.section-title { font-size: 15px; font-weight: 600; color: var(--text); margin: 0 0 14px; }
.link-btn { background: none; border: none; color: var(--primary); font-size: 13px; cursor: pointer; font-weight: 500; padding: 0; }

.contract-list { display: flex; flex-direction: column; gap: 12px; flex: 1; }
.contract-card {
  background: white;
  border: 1px solid var(--border-light);
  border-radius: var(--radius);
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.group-header {
  display: flex; align-items: center; gap: 8px;
  padding-left: 10px;
  border-left: 3px solid var(--primary);
  font-size: 14px; font-weight: 600; color: var(--text);
}
.group-icon { font-size: 15px; }
.group-title { font-weight: 600; }
.pill-row { display: flex; flex-wrap: wrap; gap: 8px; }
.pill {
  padding: 5px 12px;
  background: #f0f5ff;
  border: 1px solid #d6e4ff;
  border-radius: 20px;
  font-size: 13px;
  color: var(--text);
  cursor: pointer;
  transition: all 0.15s;
  white-space: nowrap;
}
.pill:hover { background: #e6f4ff; border-color: var(--primary); color: var(--primary); }

.calendar-card {
  background: white;
  border: 1px solid var(--border-light);
  border-radius: var(--radius);
  padding: 16px;
}
.cal-nav { display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px; }
.cal-month { font-weight: 600; font-size: 14px; color: var(--text); }
.cal-btns { display: flex; gap: 4px; }
.cal-btn {
  width: 28px; height: 28px;
  background: none; border: 1px solid var(--border-light);
  border-radius: 6px; cursor: pointer;
  font-size: 16px; color: var(--text-secondary);
  display: flex; align-items: center; justify-content: center;
  line-height: 1;
}
.cal-btn:hover { color: var(--text); border-color: #aaa; }

.cal-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 4px; }
.cal-weekday { text-align: center; font-size: 12px; color: var(--text-secondary); font-weight: 500; padding: 6px 0; }
.cal-day {
  aspect-ratio: 1;
  display: flex; align-items: center; justify-content: center;
  font-size: 13px; color: var(--text-secondary);
  border-radius: 6px;
}
.cal-day.event { background: #fff7ed; color: #c2410c; font-weight: 500; }
.cal-day.today { background: var(--primary); color: white; font-weight: 600; }
.cal-day.empty { pointer-events: none; }

.cal-legend { display: flex; align-items: center; gap: 16px; margin-top: 14px; flex-wrap: wrap; }
.legend-item { display: flex; align-items: center; gap: 6px; font-size: 12px; color: var(--text-secondary); }
.dot { width: 10px; height: 10px; border-radius: 50%; }
.event-dot { background: #fff7ed; border: 1px solid #fed7aa; }
.today-dot { background: var(--primary); }
.legend-note { font-size: 12px; color: var(--text-secondary); margin-left: auto; }

.reminders { display: flex; flex-direction: column; gap: 8px; margin-top: 14px; border-top: 1px solid var(--border-light); padding-top: 14px; }
.reminder-item { display: flex; align-items: center; gap: 10px; padding: 8px 12px; background: #f8fafc; border-radius: 8px; }
.reminder-icon { font-size: 16px; flex-shrink: 0; }
.reminder-info { display: flex; flex-direction: column; flex: 1; }
.reminder-label { font-size: 13px; font-weight: 500; color: var(--text); }
.reminder-date { font-size: 11px; color: var(--text-secondary); }
.reminder-days { font-size: 13px; font-weight: 600; color: #52c41a; white-space: nowrap; }
.reminder-days.soon { color: #fa8c16; }
.reminder-days.urgent { color: #f5222d; }
</style>
