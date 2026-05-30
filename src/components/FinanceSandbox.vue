<script setup lang="ts">
import { ref, computed } from 'vue'

const SOC_MIN = 7310, SOC_MAX = 36549, CORP_RATE = 0.2716, IND_RATE = 0.105, BASE_OPS = 2000
const ROLES = ['创始人/CEO', '研发技术', '产品设计', '销售/BD', '运营/市场', '行政人事']
const LEVELS = ['初级', '中级', '高级', '总监级']

interface Employee { id: number; role: string; level: string; salary: number }

const industry = ref('tech')
const capital = ref(100)
const empCount = ref(3)

const employees = ref<Employee[]>(
  Array.from({ length: 3 }, (_, idx) => ({
    id: idx,
    role: idx === 0 ? ROLES[0] : ROLES[1],
    level: idx === 0 ? LEVELS[3] : LEVELS[1],
    salary: idx === 0 ? 20000 : 10000,
  }))
)

function syncEmpCount(n: number) {
  empCount.value = n
  const cur = employees.value.length
  if (n > cur) {
    for (let i = cur; i < n; i++)
      employees.value.push({ id: Date.now() + i, role: ROLES[1], level: LEVELS[1], salary: 10000 })
  } else {
    employees.value.splice(n)
  }
}

function socBase(salary: number) { return Math.min(Math.max(salary, SOC_MIN), SOC_MAX) }

const totals = computed(() => {
  let salary = 0, corp = 0
  employees.value.forEach(e => { salary += e.salary; corp += socBase(e.salary) * CORP_RATE })
  return { salary, corp, burn: BASE_OPS + salary + corp }
})

const isGeneral = computed(() => capital.value >= 500)

const adviceMap: Record<string, string> = {
  tech: '推荐注册于高新区。符合条件的科技企业可申请"双软认证"，享受企业所得税优惠及研发加计扣除。',
  trade: '推荐保税区或自贸区。涉及进出口必须办理进出口权备案，并建立规范的出口退税财务台账。',
  service: '推荐经济园区。通常提供免费虚拟注册地址，并有一定比例的地方财政税收返还政策。',
  food: '必须以实际商铺地址注册。正式营业前需向市监局申请《食品经营许可证》，并在选址阶段考虑环评。',
}

const chartBars = computed(() => {
  const t = totals.value.burn || 1
  return [
    { label: '基础运营', value: BASE_OPS, pct: BASE_OPS / t * 100, color: '#faad14' },
    { label: '税前工资', value: totals.value.salary, pct: totals.value.salary / t * 100, color: '#1677ff' },
    { label: '企业社保', value: totals.value.corp, pct: totals.value.corp / t * 100, color: '#ff4d4f' },
  ]
})

function fmt(n: number) { return '¥ ' + n.toLocaleString('zh-CN', { minimumFractionDigits: 2 }) }
</script>

<template>
  <div class="grid">
    <!-- Left -->
    <div class="left">
      <div class="card">
        <div class="card-header">全局业务参数配置</div>
        <div class="form-row">
          <div class="form-item">
            <label>主营业务类型</label>
            <select v-model="industry" class="input">
              <option value="tech">科技/互联网服务</option>
              <option value="trade">进出口及一般贸易</option>
              <option value="service">企业服务/咨询</option>
              <option value="food">实体门店/餐饮</option>
            </select>
          </div>
        </div>
        <div class="form-row">
          <div class="form-item">
            <label>拟注册资本（影响纳税人身份认定）</label>
            <div class="slider-row">
              <input type="range" v-model.number="capital" min="10" max="1000" step="10" />
              <span class="slider-val">{{ capital }} 万元</span>
            </div>
          </div>
        </div>
        <div class="form-row">
          <div class="form-item">
            <label>拟定员工总数</label>
            <div class="slider-row">
              <input type="range" :value="empCount" min="1" max="15" step="1" @input="syncEmpCount(+($event.target as HTMLInputElement).value)" />
              <span class="slider-val">{{ empCount }} 人</span>
            </div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <span>动态薪酬结构与社保测算明细</span>
          <span class="sub">* 以上海社保基数为例：下限 ¥7310，上限 ¥36549</span>
        </div>
        <div class="table">
          <div class="t-head">
            <div>岗位角色</div><div>职级</div><div>税前月薪</div>
            <div class="r">企业社保</div><div class="r">个人代扣</div>
          </div>
          <div v-for="emp in employees" :key="emp.id" class="t-row">
            <select v-model="emp.role" class="input-sm">
              <option v-for="r in ROLES" :key="r">{{ r }}</option>
            </select>
            <select v-model="emp.level" class="input-sm">
              <option v-for="l in LEVELS" :key="l">{{ l }}</option>
            </select>
            <input type="number" v-model.number="emp.salary" class="input-sm" min="1000" step="1000" />
            <div class="r err">{{ fmt(socBase(emp.salary) * CORP_RATE) }}</div>
            <div class="r suc">{{ fmt(socBase(emp.salary) * IND_RATE) }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Right -->
    <div class="right">
      <div class="card">
        <div class="card-header">成本结构剖析（Burn Rate）</div>
        <div class="burn-center">
          <div class="burn-label">每月总硬性现金流出预估</div>
          <div class="burn-amount">{{ fmt(totals.burn) }}</div>
        </div>
        <div class="chart-bars">
          <div v-for="bar in chartBars" :key="bar.label" class="bar-row">
            <div class="bar-label">{{ bar.label }}</div>
            <div class="bar-track">
              <div class="bar-fill" :style="{ width: bar.pct + '%', background: bar.color }"></div>
            </div>
            <div class="bar-val">{{ fmt(bar.value) }}</div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-header">财税合规落地方案</div>
        <div class="tags">
          <span class="tag blue">{{ isGeneral ? '一般纳税人' : '小规模纳税人' }}</span>
          <span class="tag green">{{ isGeneral ? '增值税按月申报' : '增值税按季度申报' }}</span>
        </div>
        <div class="advice-box">💡 {{ adviceMap[industry] }}</div>
        <ul class="notes">
          <li><strong>基础运营费：</strong>模型内含 ¥2,000，涵盖基础财务代账、银行账户年费及报税维护杂费。</li>
          <li><strong>个税提示：</strong>个人代扣部分仅包含社保公积金（约10.5%），未计算专项附加扣除及个人所得税。</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
.grid { display: grid; grid-template-columns: 1fr; gap: 20px; }
@media (min-width: 1100px) { .grid { grid-template-columns: 3fr 2fr; } }
.left, .right { display: flex; flex-direction: column; gap: 20px; }

.card { background: white; border-radius: var(--radius); box-shadow: var(--shadow); padding: 24px; }
.card-header { font-size: 15px; font-weight: 600; margin-bottom: 20px; padding-bottom: 12px; border-bottom: 1px solid var(--border-light); display: flex; justify-content: space-between; align-items: center; }
.sub { font-size: 12px; font-weight: 400; color: var(--text-secondary); }

.form-row { margin-bottom: 16px; }
.form-item { display: flex; flex-direction: column; gap: 8px; }
label { font-size: 13px; font-weight: 500; color: var(--text); }
.input { height: 34px; padding: 0 10px; border: 1px solid var(--border); border-radius: 6px; font-size: 13px; color: var(--text); outline: none; }
.input:focus { border-color: var(--primary); }
.slider-row { display: flex; align-items: center; gap: 12px; }
.slider-row input[type=range] { flex: 1; accent-color: var(--primary); }
.slider-val { font-size: 13px; font-weight: 500; min-width: 70px; text-align: right; }

.table { border: 1px solid var(--border-light); border-radius: 6px; overflow: hidden; }
.t-head, .t-row { display: grid; grid-template-columns: 1.5fr 1fr 1.2fr 1.3fr 1.3fr; gap: 8px; padding: 10px 14px; align-items: center; }
.t-head { background: #fafafa; font-size: 12px; color: var(--text-secondary); font-weight: 500; border-bottom: 1px solid var(--border-light); }
.t-row { border-bottom: 1px solid var(--border-light); }
.t-row:last-child { border-bottom: none; }
.t-row:hover { background: #fafafa; }
.input-sm { height: 30px; padding: 0 8px; border: 1px solid var(--border); border-radius: 4px; font-size: 12px; width: 100%; outline: none; }
.r { text-align: right; font-size: 13px; font-variant-numeric: tabular-nums; }
.err { color: var(--error); }
.suc { color: var(--success); }

.burn-center { text-align: center; padding: 16px 0 20px; }
.burn-label { font-size: 13px; color: var(--text-secondary); margin-bottom: 8px; }
.burn-amount { font-size: 32px; font-weight: 700; color: var(--text); font-variant-numeric: tabular-nums; }

.chart-bars { display: flex; flex-direction: column; gap: 12px; }
.bar-row { display: flex; align-items: center; gap: 10px; }
.bar-label { font-size: 12px; color: var(--text-secondary); width: 60px; flex-shrink: 0; }
.bar-track { flex: 1; height: 8px; background: #f0f0f0; border-radius: 4px; overflow: hidden; }
.bar-fill { height: 100%; border-radius: 4px; transition: width 0.4s ease; }
.bar-val { font-size: 12px; color: var(--text); font-variant-numeric: tabular-nums; width: 110px; text-align: right; flex-shrink: 0; }

.tags { display: flex; gap: 8px; margin-bottom: 14px; flex-wrap: wrap; }
.tag { font-size: 12px; padding: 3px 10px; border-radius: 4px; font-weight: 500; }
.tag.blue { background: #e6f4ff; color: var(--primary); border: 1px solid #91caff; }
.tag.green { background: #f6ffed; color: #389e0d; border: 1px solid #b7eb8f; }

.advice-box { background: #fffbe6; border: 1px solid #ffe58f; padding: 12px 14px; border-radius: 6px; font-size: 13px; color: #d46b08; line-height: 1.6; margin-bottom: 14px; }
.notes { padding-left: 16px; font-size: 12px; color: var(--text-secondary); line-height: 1.7; display: flex; flex-direction: column; gap: 4px; }
</style>
