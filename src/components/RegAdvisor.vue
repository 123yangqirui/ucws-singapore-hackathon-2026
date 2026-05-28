<script setup lang="ts">
import { ref } from 'vue'
import StepPage from './StepPage.vue'
import SummaryPage from './SummaryPage.vue'

export interface StepData {
  id: string
  title: string
  icon: string
  options: StepOption[]
}

export interface StepOption {
  label: string
  summary: string
  detail: string
  recommended?: boolean
}

export interface BusinessScope {
  main: string
  others: string[]
}

export interface BaseFormData {
  business: string
  people: number | null
  shareholder: number | null
  companyType: string
  namePref: string
  name: string
  scope: BusinessScope | ''
  capital: string
  address: string
  org: string
}

const currentStep = ref(0)
const steps = ref<StepData[]>([])

const EMPTY_FORM: BaseFormData = {
  business: '',
  people: null,
  shareholder: null,
  companyType: '',
  namePref: '',
  name: '',
  scope: '',
  capital: '',
  address: '',
  org: '',
}

const formData = ref<BaseFormData>({ ...EMPTY_FORM })


function onAnswer(stepId: string, answer: string | BusinessScope) {
  (formData.value as any)[stepId] = answer
}

function onUpdateFormData(patch: Partial<BaseFormData>) {
  formData.value = { ...formData.value, ...patch }
}

function goNext() {
  if (currentStep.value < steps.value.length - 1) {
    currentStep.value++
  } else {
    currentStep.value = steps.value.length
  }
}

function goPrev() {
  if (currentStep.value > 0) currentStep.value--
}

function goToStep(i: number) {
  if (i <= currentStep.value || (formData.value as any)[steps.value[i - 1]?.id]) {
    currentStep.value = i
  }
}

const STEP_SKELETONS = [
  { id: 'name',    title: '公司名称核准',  icon: '🔍' },
  { id: 'scope',   title: '经营范围拟定',  icon: '📋' },
  { id: 'type',    title: '公司类型选择',  icon: '🏢' },
  { id: 'capital', title: '注册资本认缴',  icon: '💰' },
  { id: 'address', title: '注册地址选择',  icon: '📍' },
  { id: 'org',     title: '组织架构设计',  icon: '🏗️' },
]

steps.value = STEP_SKELETONS.map(s => ({ ...s, options: [] }))
</script>

<template>
  <SummaryPage
    v-if="steps.length > 0 && currentStep === steps.length"
    :steps="steps"
    :form-data="formData"
    @restart="currentStep = 0; formData = { ...{ business: '', people: null, shareholder: null, companyType: '', namePref: '', name: '', scope: '', capital: '', address: '', org: '' } }"
  />

  <div v-else-if="steps.length" class="advisor-layout">
    <div class="progress-sidebar">
      <button
        v-for="(s, i) in steps"
        :key="s.id"
        class="prog-step"
        :class="{
          active: i === currentStep,
          done: i < currentStep,
          reachable: i <= currentStep || !!(formData as any)[steps[i-1]?.id]
        }"
        @click="goToStep(i)"
      >
        <div class="prog-dot-wrap">
          <span class="prog-dot">
            <span v-if="(formData as any)[s.id] !== undefined && (formData as any)[s.id] !== '' && i !== currentStep">✓</span>
            <span v-else>{{ i + 1 }}</span>
          </span>
          <span class="prog-line" v-if="i < steps.length - 1" />
        </div>
        <span class="prog-label">{{ s.title }}</span>
      </button>
    </div>

    <StepPage
      class="advisor-content"
      :step="steps[currentStep]"
      :step-index="currentStep"
      :total-steps="steps.length"
      :selected="(formData as any)[steps[currentStep]?.id]"
      :is-last="currentStep === steps.length - 1"
      :form-data="formData"
      @answer="onAnswer"
      @update-form-data="onUpdateFormData"
      @next="goNext"
      @prev="goPrev"
    />
  </div>
</template>

<style scoped>
.advisor-layout {
  display: flex;
  gap: 20px;
  align-items: flex-start;
  width: 100%;
}
.progress-sidebar {
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: var(--radius);
  border: 1px solid var(--border-light);
  padding: 32px 28px;
  min-width: 140px;
  flex-shrink: 0;
}
.advisor-content {
  flex: 1;
  min-width: 0;
}
.prog-step {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  gap: 10px;
  background: none;
  border: none;
  cursor: default;
  padding: 0;
  text-align: left;
}
.prog-step.reachable { cursor: pointer; }
.prog-dot-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex-shrink: 0;
}
.prog-line {
  width: 2px;
  height: 54px;
  background: var(--border-light);
  margin: 2px 0;
}
.prog-step.done .prog-line,
.prog-step.active .prog-line {
  background: var(--primary);
}
.prog-dot {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  border: 2px solid var(--border);
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
  color: var(--text-secondary);
  transition: all 0.2s;
}
.prog-step.active .prog-dot {
  border-color: var(--primary);
  background: var(--primary);
  color: white;
}
.prog-step.done .prog-dot {
  border-color: var(--primary);
  background: #e6f4ff;
  color: var(--primary);
}
.prog-label {
  font-size: 12px;
  color: var(--text-secondary);
  padding-top: 5px;
  line-height: 1.3;
}
.prog-step.active .prog-label { color: var(--primary); font-weight: 600; }
.prog-step.done .prog-label { color: var(--text); }
</style>
