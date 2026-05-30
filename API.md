# API 文档

Base URL: `http://localhost:8080`

> 约定：`formData` 始终表示"截至当前步骤之前已保存的所有字段"，本步骤新输入的字段放在请求体顶层。

---

## GET /api/documents

获取“高频合同与文书”可下载文件目录。

**Response 200**

```json
{
  "documents": [
    {
      "id": "labor-contract",
      "title": "劳动合同",
      "filename": "劳动合同.docx",
      "downloadUrl": "/api/documents/labor-contract/download",
      "available": true
    }
  ]
}
```

## GET /api/documents/{document_id}/download

下载指定文书文件。`document_id` 使用 `/api/documents` 返回的 `id`。

## GET /api/documents/download-all

打包下载全部可用文书模板，返回 zip 文件。

---

## POST /api/generate-names

根据用户填写的公司名称偏好（字号）和业务描述，生成候选公司全称。

**Request**

```json
{
  "namePref": "星禾云创",
  "desc": "面向中小企业的 SaaS 协同办公平台"
}
```

| 字段           | 类型   | 说明                                       |
| -------------- | ------ | ------------------------------------------ |
| `namePref`     | string | 公司名称偏好                               |
| `desc`（可选） | string | 公司业务描述，用于 AI 生成更贴合业务的后缀 |

**Response 200**

```json
{
  "names": [
    "星禾云创科技有限公司",
    "星禾云创商务有限公司",
    "星禾云创网络有限公司"
  ],
  "recommendedBusiness": "(I) 信息传输、软件和信息技术服务业"
}
```

| 字段                  | 类型     | 说明                                                                            |
| --------------------- | -------- | ------------------------------------------------------------------------------- |
| `names`               | string[] | AI 生成的公司全称候选列表                                                        |
| `recommendedBusiness` | string   | AI 推荐的主营业务（国民经济行业分类大类，A~T，与前端行业列表一致），前端默认选中 |

---

## POST /api/check-approval

根据所选行业大类，返回该行业是否涉及前置/后置审批及具体说明。

**Request**

```json
{
  "industry": "(E) 建筑业",
  "desc":"我开发了一个软件，用于xxxxx...."
}
```

| 字段           | 类型   | 说明                              |
| -------------- | ------ | --------------------------------- |
| `industry`     | string | 行业大类（国民经济行业分类，A~T） |
| `desc`（可选） | string | 公司业务描述，用于辅助 AI 判断    |

**Response 200**

```json
{
  "needsApproval": true,
  "type": "后置审批",
  "details": "建筑施工及相关业务需在工商登记后取得资质证书方可承接工程。\n\n• 建筑施工：建筑业企业资质证书（住房和城乡建设部门）\n• 工程设计：工程设计资质证书\n• 工程监理：工程监理企业资质证书\n\n资质申请需满足注册资本、技术人员、业绩等要求，办理时限约60个工作日"
}
```

| 字段            | 类型    | 说明                                                       |
| --------------- | ------- | ---------------------------------------------------------- |
| `needsApproval` | boolean | 是否涉及审批                                               |
| `type`          | string  | 审批类型，取值：`前置审批`、`后置审批`，无审批时为空字符串 |
| `details`       | string  | 审批说明详情，支持换行符 `\n`                              |

---

## POST /api/business-scope

根据前面已填写的完整信息，生成主营业务和其他经营范围。

**Request**

```json
{
  "formData": {
    "business": "(I) 信息传输、软件和信息技术服务业",
    "namePref": "星禾云创",
    "name": "星禾云创科技有限公司"
  }
}
```

**Response 200**

```json
{
  "main": "软件开发",
  "others": ["信息系统集成服务", "技术服务", "技术咨询", "数据处理服务"]
}
```

| 字段               | 类型     | 说明                     |
| ------------------ | -------- | ------------------------ |
| `selectedBusiness` | string   | 前面已经选择的主营业务   |
| `main`             | string   | 拟定出的主营业务（一个） |
| `others`           | string[] | 其他经营范围（多个）     |

---

## POST /api/company-type

根据公司人数和股东人数，结合前面已填写的基础信息，推荐公司类型并给出说明。

**Request**

```json
{
  "people": 10,
  "shareholder": 3,
  "formData": {
    "business": "(E) 建筑业",
    "namePref": "星禾云创",
    "name": "星禾云创科技有限公司",
    "scope": {
      "main": "软件开发",
      "others": [
        "信息系统集成服务",
        "技术服务",
        "技术咨询",
        "数据处理服务"
      ]
    }
  }
}
```

| 字段          | 类型   | 说明                                           |
| ------------- | ------ | ---------------------------------------------- |
| `people`      | number | 公司人数                                       |
| `shareholder` | number | 股东人数                                       |
| `formData`    | object | 前面步骤已保存的字段（业务、字号、公司全称等） |

**Response 200**

```json
{
  "companyType": "有限责任公司",
  "explanation": "这里是为什么选择'有限责任公司'的说明。"
}
```

| 字段          | 类型   | 说明                     |
| ------------- | ------ | ------------------------ |
| `companyType` | string | 推荐的公司类型           |
| `explanation` | string | 选择该公司类型的理由说明 |

---

## POST /api/capital-estimate

根据用户输入的注册资本意向（认缴金额）和前面已填写的完整信息，返回预估金额。

**Request**

```json
{
  "capitalIntention": 100,
  "formData": {
    "business": "(C) 制造业",
    "people": 10,
    "shareholder": 3,
    "companyType": "有限责任公司",
    "namePref": "星禾云创",
    "name": "星禾云创科技有限公司",
    "scope": {
      "main": "软件开发",
      "others": [
        "信息系统集成服务",
        "技术服务",
        "技术咨询",
        "数据处理服务"
      ]
    }
  }
}
```

| 字段               | 类型   | 说明                           |
| ------------------ | ------ | ------------------------------ |
| `capitalIntention` | number | 用户输入的认缴金额，单位：万元 |
| `formData`         | object | 前面步骤已保存的字段           |

**Response 200**

```json
{
  "estimatedAmount": 100
}
```

| 字段              | 类型   | 说明                     |
| ----------------- | ------ | ------------------------ |
| `estimatedAmount` | number | 后端预估金额，单位：万元 |

---

## POST /api/address-recommendations

根据用户选择的注册省份和前面已填写的完整信息，从"商用办公地址、园区/孵化器/集中办公区地址、虚拟地址、住宅地址"中返回推荐注册地址类型并给出说明。

**Request**

```json
{
  "province": "北京市",
  "formData": {
    "business": "(C) 制造业",
    "people": 10,
    "shareholder": 3,
    "companyType": "有限责任公司",
    "namePref": "星禾云创",
    "name": "星禾云创科技有限公司",
    "scope": {
      "main": "软件开发",
      "others": [
        "信息系统集成服务",
        "技术服务",
        "技术咨询",
        "数据处理服务"
      ]
    },
    "capital": "认缴金额：100 万元；预估金额：100 万元"
  }
}
```

| 字段       | 类型   | 说明                           |
| ---------- | ------ | ------------------------------ |
| `province` | string | 用户选择的注册省份，不含港澳台 |
| `formData` | object | 前面步骤已保存的字段           |

**Response 200**

```json
{
  "province": "北京市",
  "recommendation": "商用办公地址",
  "explanation": "这里是为什么推荐'商用办公地址'的说明。"
}
```

| 字段             | 类型   | 说明                       |
| ---------------- | ------ | -------------------------- |
| `province`       | string | 用户选择的注册省份         |
| `recommendation` | string | 推荐的注册地址类型，四选一 |
| `explanation`    | string | 推荐该地址类型的理由说明   |

---

## 错误响应

| 状态码 | 说明                 |
| ------ | -------------------- |
| 400    | 请求体 JSON 解析失败 |
| 404    | 接口路径不存在       |
| 405    | 非 POST 请求         |

---
