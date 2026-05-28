<script setup lang="ts">
import type { StepData, BaseFormData } from './RegAdvisor.vue'

const props = defineProps<{
  steps: StepData[]
  formData: BaseFormData
}>()

const emit = defineEmits<{ restart: [] }>()

const STEP_LABELS: Record<string, string> = {
  name: '公司名称',
  type: '公司类型',
  scope: '经营范围',
  capital: '注册资本',
  address: '注册地址',
  org: '组织架构',
}

function getStepValue(stepId: string): string {
  const key = stepId === 'type' ? 'companyType' : stepId
  const v = (props.formData as any)[key]
  if (v == null || v === '') return '—'
  if (stepId === 'scope' && typeof v === 'object') {
    const others = Array.isArray(v.others) ? v.others.join('、') : ''
    return others ? `主：${v.main}；其他：${others}` : `主：${v.main}`
  }
  return String(v)
}

const NON_ORG_STEPS = ['name', 'type', 'scope', 'capital', 'address']

const FULL_FLOW: { id: string; title: string; icon: string; desc: string }[] = [
  { id: 'name',    title: '公司名称核准', icon: '🔍', desc: '确定公司字号并通过名称核准' },
  { id: 'scope',   title: '经营范围拟定', icon: '📋', desc: '确定主营业务及其他经营范围' },
  { id: 'type',    title: '公司类型选择', icon: '🏢', desc: '根据股东与规模选择公司组织形式' },
  { id: 'capital', title: '注册资本认缴', icon: '💰', desc: '确定认缴金额并写入公司章程' },
  { id: 'address', title: '注册地址选择', icon: '📍', desc: '选择并确认合规的注册地址' },
  { id: 'org',     title: '组织架构设计', icon: '🏗️', desc: '设置法定代表人、董事、监事等岗位' },
  { id: 'license', title: '领取营业执照', icon: '📄', desc: '提交工商登记申请并领取营业执照' },
  { id: 'seal',    title: '刻章与备案',   icon: '🔏', desc: '刻制公章、财务章、法人章等并到公安备案' },
]

function exportPdf() {
  window.print()
}
</script>

<template>
  <div class="summary-wrap">
    <!-- Header -->
    <div class="header-card">
      <div class="header-left">
        <div class="header-badge">✦ 方案已生成</div>
        <h1 class="header-title">您的工商注册方案</h1>
        <p class="header-sub">根据您的选择定制生成，可导出为 PDF 存档备用</p>
      </div>
      <div class="header-actions">
        <button class="btn-ghost no-print" @click="emit('restart')">重新配置</button>
        <button class="btn-export no-print" @click="exportPdf">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
          导出 PDF
        </button>
      </div>
    </div>

    <!-- Info + Org layout (vertical stack) -->
    <div class="main-layout">
      <!-- step results -->
      <div class="info-panel">
        <div class="panel-title">注册方案详情</div>
        <div
          v-for="step in steps.filter(s => NON_ORG_STEPS.includes(s.id))"
          :key="step.id"
          class="info-row"
        >
          <div class="row-meta">
            <span class="row-icon">{{ step.icon }}</span>
            <span class="row-label">{{ STEP_LABELS[step.id] ?? step.title }}</span>
          </div>
          <div class="row-value">{{ getStepValue(step.id) }}</div>
        </div>
      </div>

      <!-- org chart -->
      <div class="org-panel">
        <div class="panel-title">组织架构设计</div>
        <div class="org-img-wrap">
          <img src="/c_arch.jpg" alt="组织架构图" class="org-img" />
        </div>
      </div>
    </div>

    <!-- Full registration flow (8 steps) -->
    <div class="flow-panel">
      <div class="panel-title">完整注册流程</div>
      <div class="flow-list">
        <template v-for="(step, i) in FULL_FLOW" :key="step.id">
          <div class="flow-card">
            <div class="flow-num">{{ i + 1 }}</div>
            <div class="flow-head">
              <span class="flow-icon">{{ step.icon }}</span>
              <span class="flow-title">{{ step.title }}</span>
            </div>
            <div class="flow-desc">{{ step.desc }}</div>
          </div>
          <div v-if="i < FULL_FLOW.length - 1" class="flow-arrow" aria-hidden="true">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="9 6 15 12 9 18" />
            </svg>
          </div>
        </template>
      </div>
    </div>

    <!-- Footer -->
    <div class="footer-note">
      <span class="note-dot">💡</span>
      以上方案仅供参考，具体注册流程请以当地工商局要求为准。建议在正式提交前咨询专业顾问。
    </div>
  </div>
</template>

<style scoped>
.summary-wrap {
  display: flex;
  flex-direction: column;
  gap: 20px;
  width: 100%;
  max-width: 1080px;
  margin: 0 auto;
}

/* ── Header ── */
.header-card {
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, #0f52ba 0%, #1677ff 55%, #4096ff 100%);
  border-radius: var(--radius);
  padding: 32px 36px;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 24px;
  color: white;
  box-shadow: 0 6px 24px rgba(22,119,255,0.35);
}
.header-card::before {
  content: '';
  position: absolute;
  top: -40px; right: -40px;
  width: 200px; height: 200px;
  border-radius: 50%;
  background: rgba(255,255,255,0.06);
  pointer-events: none;
}
.header-card::after {
  content: '';
  position: absolute;
  bottom: -60px; right: 80px;
  width: 160px; height: 160px;
  border-radius: 50%;
  background: rgba(255,255,255,0.04);
  pointer-events: none;
}
.header-badge {
  display: inline-flex;
  align-items: center;
  height: 22px;
  padding: 0 12px;
  background: rgba(255,255,255,0.18);
  border: 1px solid rgba(255,255,255,0.3);
  border-radius: 999px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.8px;
  margin-bottom: 10px;
}
.header-title { font-size: 24px; font-weight: 800; margin: 0 0 6px; line-height: 1.2; }
.header-sub { font-size: 13px; opacity: 0.8; margin: 0; }
.header-actions { display: flex; gap: 10px; flex-shrink: 0; align-items: center; position: relative; z-index: 1; }

.btn-ghost {
  background: rgba(255,255,255,0.12);
  border: 1px solid rgba(255,255,255,0.35);
  color: white;
  padding: 0 16px;
  height: 36px;
  border-radius: 8px;
  font-size: 13px;
  cursor: pointer;
  transition: background 0.2s;
}
.btn-ghost:hover { background: rgba(255,255,255,0.22); }
.btn-export {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  background: white;
  color: #1677ff;
  border: none;
  padding: 0 20px;
  height: 36px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 2px 10px rgba(0,0,0,0.15);
  transition: box-shadow 0.2s, transform 0.15s;
}
.btn-export:hover { transform: translateY(-1px); box-shadow: 0 4px 16px rgba(0,0,0,0.2); }

/* ── Main layout (vertical stack) ── */
.main-layout {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* ── Org panel: constrain image width so it doesn't stretch full-width ── */
.org-img-wrap {
  padding: 20px;
  background: #f8fafc;
  display: flex;
  justify-content: center;
}
.org-img {
  display: block;
  max-width: 560px;
  width: 100%;
  border-radius: 8px;
  border: 1px solid var(--border-light);
  object-fit: contain;
}

/* ── Shared panel ── */
.info-panel,
.org-panel,
.flow-panel {
  background: white;
  border-radius: var(--radius);
  border: 1px solid var(--border-light);
  box-shadow: var(--shadow);
  overflow: hidden;
}
.panel-title {
  font-size: 13px;
  font-weight: 700;
  color: var(--text-secondary);
  letter-spacing: 0.4px;
  padding: 16px 22px 14px;
  border-bottom: 1px solid var(--border-light);
  background: #fafbfc;
}

/* ── Info rows ── */
.info-row {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 16px 22px;
  border-bottom: 1px solid var(--border-light);
  transition: background 0.15s;
}
.info-row:last-child { border-bottom: none; }
.info-row:hover { background: #f8faff; }
.row-meta {
  display: flex;
  align-items: center;
  gap: 7px;
}
.row-icon { font-size: 14px; }
.row-label {
  font-size: 11.5px;
  font-weight: 600;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.row-value {
  font-size: 14px;
  font-weight: 600;
  color: var(--text);
  line-height: 1.6;
  padding-left: 21px;
  word-break: break-all;
}

/* ── Flow timeline (horizontal cards) ── */
.flow-list {
  display: flex;
  flex-wrap: wrap;
  align-items: stretch;
  gap: 6px;
  padding: 22px 22px 22px;
}
.flow-card {
  flex: 1 1 130px;
  min-width: 130px;
  background: #fafbff;
  border: 1px solid var(--border-light);
  border-radius: 10px;
  padding: 14px 12px 14px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  transition: border-color 0.15s, box-shadow 0.15s, transform 0.15s;
}
.flow-card:hover {
  border-color: #91caff;
  box-shadow: 0 4px 12px rgba(22,119,255,0.1);
  transform: translateY(-1px);
}
.flow-num {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  height: 18px;
  padding: 0 8px;
  border-radius: 999px;
  background: #e6f4ff;
  color: var(--primary);
  font-size: 10.5px;
  font-weight: 700;
  letter-spacing: 0.5px;
  margin-bottom: 10px;
}
.flow-num::before {
  content: 'STEP';
  font-size: 9px;
  opacity: 0.7;
}
.flow-icon {
  font-size: 18px;
  line-height: 1;
}
.flow-head {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  margin-bottom: 6px;
}
.flow-title {
  font-size: 13px;
  font-weight: 700;
  color: var(--text);
  line-height: 1.3;
}
.flow-desc {
  font-size: 11.5px;
  color: var(--text-secondary);
  line-height: 1.5;
}
.flow-arrow {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  flex-shrink: 0;
  color: var(--primary);
  font-size: 20px;
  font-weight: 700;
  line-height: 1;
}
@media (max-width: 900px) {
  .flow-arrow { display: none; }
}

/* ── Footer ── */
.footer-note {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 13px 18px;
  background: #fffbe6;
  border: 1px solid #ffe58f;
  border-radius: 8px;
  font-size: 12px;
  color: #8c6d1f;
  line-height: 1.7;
}
.note-dot { flex-shrink: 0; }

/* ── Print ── */
@media print {
  .no-print { display: none !important; }
  .header-card {
    background: #1677ff !important;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
  .info-panel, .org-panel, .flow-panel { box-shadow: none; border: 1px solid #ddd; break-inside: avoid; }
}
</style>
