import { reactive } from 'vue'
import type { BaseFormData } from './components/RegAdvisor.vue'

export const sharedFormData = reactive<{ value: BaseFormData | null }>({ value: null })
