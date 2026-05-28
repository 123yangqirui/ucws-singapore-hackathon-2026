import http from 'node:http'

const PORT = 3001

interface BusinessScope {
  main: string
  others: string[]
}

interface BaseFormData {
  business?: string
  people?: number | null
  shareholder?: number | null
  companyType?: string
  namePref?: string
  name?: string
  scope?: BusinessScope | ''
  capital?: string
  address?: string
  org?: string
}

const APPROVAL_INDUSTRIES: Record<string, { type: string; details: string }> = {
  '食品': { type: '前置审批', details: '经营食品相关业务需在工商登记前取得《食品经营许可证》（食品药品监督管理局颁发）。涉及食品生产的还需取得《食品生产许可证》（SC认证）。\n\n所需材料：\n• 经营场所平面图及卫生设施说明\n• 食品安全管理人员资质证明\n• 食品安全管理制度文件\n\n办理时限：约15-30个工作日' },
  '医疗': { type: '前置审批', details: '医疗器械、药品、医疗服务等业务需在工商登记前取得相应许可。\n\n• 医疗器械经营：《医疗器械经营许可证》（市级药监局）\n• 药品经营：《药品经营许可证》（省级药监局）\n• 医疗机构：《医疗机构执业许可证》（卫生健康委）\n\n办理时限：30-90个工作日，建议提前咨询当地主管部门' },
  '金融': { type: '前置审批', details: '金融相关业务受严格监管，需在工商登记前取得金融监管部门批准。\n\n• 银行/保险/证券：中国人民银行或银保监会/证监会审批\n• 小额贷款：省级金融监管局审批\n• 融资担保：省级金融监管局审批\n\n注意：未经批准不得在名称或经营范围中使用"金融"、"贷款"、"理财"等字样' },
  '教育': { type: '后置审批', details: '教育培训类业务工商登记后需取得相应许可方可开展经营。\n\n• 学科类培训（K12）：教育局审批，受"双减"政策严格限制\n• 非学科类培训（体育/艺术/科技）：主管部门审批后在教育局备案\n• 职业技能培训：人力资源和社会保障局审批\n\n办理时限：约20-45个工作日' },
  '互联网': { type: '后置审批', details: '互联网信息服务业务需在工商登记后办理ICP备案或许可证。\n\n• 一般网站：ICP备案（工业和信息化部，免费，约20个工作日）\n• 经营性互联网信息服务：ICP许可证（省级通信管理局）\n• 互联网新闻信息服务：互联网新闻信息服务许可证\n• 网络出版：网络出版服务许可证（国家新闻出版总署）' },
  '建筑': { type: '后置审批', details: '建筑施工及相关业务需在工商登记后取得资质证书方可承接工程。\n\n• 建筑施工：建筑业企业资质证书（住房和城乡建设部门）\n• 工程设计：工程设计资质证书\n• 工程监理：工程监理企业资质证书\n\n资质申请需满足注册资本、技术人员、业绩等要求，办理时限约60个工作日' },
}

function checkApproval(industry: string, desc: string) {
  const text = `${industry} ${desc ?? ''}`
  for (const [key, val] of Object.entries(APPROVAL_INDUSTRIES)) {
    if (text.includes(key)) return { needsApproval: true, ...val }
  }
  return { needsApproval: false, type: '', details: '' }
}

function generateNames(namePref: string, desc: string) {
  const text = desc ?? ''
  const isTech = /科技|技术|软件|研发|数字/.test(text)
  const isEcom = /电商|零售|直播|代运营/.test(text)
  const isService = /咨询|服务|管理|策划/.test(text)
  const suffixes = isTech
    ? ['科技有限公司', '数字科技有限公司', '智能科技有限公司']
    : isEcom
    ? ['网络有限公司', '电子商务有限公司', '科技有限公司']
    : isService
    ? ['商务咨询有限公司', '管理咨询有限公司', '企业管理有限公司']
    : ['科技有限公司', '商务有限公司', '网络有限公司']
  return suffixes.map(s => `${namePref}${s}`)
}

function generateBusinessScope(formData: BaseFormData) {
  const selectedBusiness = formData.business || '未选择'
  const contextText = `${selectedBusiness} ${formData.name ?? ''} ${formData.companyType ?? ''}`
  if (/农|林|牧|渔|种植|谷物/.test(contextText))
    return { main: '谷物种植', others: ['油料种植', '人民币种植', '豆类种植', '农副产品销售'] }
  if (/电商|零售|直播|代运营|网络/.test(contextText))
    return { main: '互联网销售', others: ['数字技术服务', '电子商务', '品牌管理', '市场营销策划'] }
  if (/科技|技术|软件|研发|信息/.test(contextText))
    return { main: '软件开发', others: ['信息系统集成服务', '技术服务', '技术咨询', '数据处理服务'] }
  if (/咨询|服务|管理|商务/.test(contextText))
    return { main: '企业管理咨询', others: ['商务代理代办服务', '市场主体登记注册代理', '财务咨询', '市场营销策划'] }
  return { main: selectedBusiness, others: ['企业管理咨询', '商务代理代办服务', '市场营销策划'] }
}

function generateCompanyType(people: number, shareholder: number, formData: BaseFormData) {
  const teamSize = Math.max(0, Number(people) || 0)
  const shareholders = Math.max(0, Number(shareholder) || 0)
  const isFinance = /金融/.test(formData.business || '')

  if (shareholders === 1) {
    return {
      companyType: '一人有限责任公司',
      explanation: `仅有 1 名股东，适合一人有限责任公司。该形式由一名自然人或法人股东独资设立，决策灵活；但需注意股东个人财产与公司财产的混同风险，必要时承担连带责任。`,
    }
  }
  if (teamSize >= 50 || shareholders >= 50 || isFinance) {
    return {
      companyType: '股份有限公司',
      explanation: `公司人数 ${teamSize} 人、股东人数 ${shareholders} 人${isFinance ? '，且涉及金融业' : ''}，规模较大或后续可能引入更多投资人，建议采用股份有限公司形式，便于股权流转和未来融资上市。`,
    }
  }
  return {
    companyType: '有限责任公司',
    explanation: `公司人数 ${teamSize} 人、股东人数 ${shareholders} 人，规模适中，推荐有限责任公司。它兼顾治理灵活与有限责任保护，是中小型企业最常用的组织形式。`,
  }
}

function generateCapitalEstimate(capitalIntention: number, formData: BaseFormData) {
  const amount = Math.max(0, Number(capitalIntention) || 0)
  const isJointStock = (formData.companyType || '').includes('股份')
  const teamBase = formData.people >= 50 ? 500 : formData.people >= 20 ? 100 : 10
  const clientBase = 30
  const pressureBase = 50
  const legalBase = isJointStock ? 500 : 0
  return { estimatedAmount: Math.max(amount, teamBase, clientBase, pressureBase, legalBase) }
}

function generateAddressRecommendations(province: string, formData: BaseFormData) {
  const isStrictCity = /北京市|上海市|深圳|广州市/.test(province)
  const recommendation = isStrictCity ? '商用办公地址' : '园区/孵化器/集中办公区地址'
  const explanation = isStrictCity
    ? `${province}对注册地址核查较严，住宅地址通常不被接受；同时考虑到您选定的业务（${formData.business || '所选行业'}）和公司类型（${formData.companyType || '—'}），推荐使用商用办公地址，便于工商和税务核查。`
    : `${province}对初创企业较友好，推荐使用园区/孵化器/集中办公区地址。可享受地址托管、政策扶持及税收优惠，且能满足工商核验要求，性价比更高。`
  return { province, recommendation, explanation }
}

function readBody(req: http.IncomingMessage): Promise<unknown> {
  return new Promise((resolve, reject) => {
    let data = ''
    req.on('data', chunk => { data += chunk })
    req.on('end', () => { try { resolve(JSON.parse(data)) } catch { reject(new Error('Invalid JSON')) } })
    req.on('error', reject)
  })
}

function send(res: http.ServerResponse, body: unknown) {
  res.writeHead(200, { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' })
  res.end(JSON.stringify(body))
}

const server = http.createServer(async (req, res) => {
  if (req.method === 'OPTIONS') {
    res.writeHead(204, { 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': 'Content-Type', 'Access-Control-Allow-Methods': 'POST' })
    res.end()
    return
  }
  if (req.method !== 'POST') { res.writeHead(405); res.end(); return }

  try {
    const body = await readBody(req) as Record<string, unknown>

    if (req.url === '/api/generate-names') {
      const { namePref, desc } = body as { namePref: string; desc?: string }
      await new Promise(r => setTimeout(r, 600))
      send(res, { names: generateNames(namePref, desc ?? '') })

    } else if (req.url === '/api/check-approval') {
      const { industry, desc } = body as { industry: string; desc?: string }
      await new Promise(r => setTimeout(r, 300))
      send(res, checkApproval(industry, desc ?? ''))

    } else if (req.url === '/api/business-scope') {
      const { formData } = body as { formData: BaseFormData }
      await new Promise(r => setTimeout(r, 400))
      send(res, generateBusinessScope(formData))

    } else if (req.url === '/api/company-type') {
      const { people, shareholder, formData } = body as { people: number; shareholder: number; formData: BaseFormData }
      await new Promise(r => setTimeout(r, 350))
      send(res, generateCompanyType(people, shareholder, formData))

    } else if (req.url === '/api/capital-estimate') {
      const { capitalIntention, formData } = body as { capitalIntention: number; formData: BaseFormData }
      await new Promise(r => setTimeout(r, 300))
      send(res, generateCapitalEstimate(capitalIntention, formData))

    } else if (req.url === '/api/address-recommendations') {
      const { province, formData } = body as { province: string; formData: BaseFormData }
      await new Promise(r => setTimeout(r, 300))
      send(res, generateAddressRecommendations(province, formData))

    } else {
      res.writeHead(404); res.end()
    }
  } catch {
    res.writeHead(400); res.end()
  }
})

server.listen(PORT, () => console.log(`Mock API server running on http://localhost:${PORT}`))
