# 创业助手 AI

## 快速开始

### 1. 安装依赖
```bash
pip install fastapi uvicorn pydantic pydantic-settings python-dotenv openai httpx
```

### 2. 配置环境变量
创建 `.env` 文件：
```bash
LLM_API_KEY=your_api_key
LLM_BASE_URL=https://api.deepseek.com/v1
LLM_MODEL_NAME=deepseek-v4-flash
```

### 3. 启动服务
```bash
python start.py
```

访问 http://localhost:8000/docs 查看 API 文档

## API 接口

所有业务接口都在 `/api/v1` 路径下，**仅支持 POST 请求**

### 1. 生成公司名称
```bash
POST /api/v1/page1/generate-names
{
  "namePref": "星河云创",
  "desc": "软件开发"
}
```

### 2. 查询审批信息
```bash
POST /api/v1/page2/check-approval
{
  "industry": "I - 信息传输、软件和信息技术服务业",
  "desc": "软件开发"
}
```

### 3. 生成经营范围
```bash
POST /api/v1/page3/business-scope
{
  "formData": {
    "business": "信息传输、软件和信息技术服务业",
    "people": 10,
    "shareholder": 3,
    "namePref": "星河云创",
    "name": "星河云创科技有限公司"
  }
}
```

### 4. 推荐公司类型
```bash
POST /api/v1/page4/company-type
{
  "people": 10,
  "shareholder": 3,
  "formData": {
    "business": "信息传输、软件和信息技术服务业",
    "namePref": "星河云创",
    "name": "星河云创科技有限公司",
    "scope": {
      "main": "软件开发",
      "others": ["技术服务", "技术咨询"]
    }
  }
}
```

### 5. 评估注册资本
```bash
POST /api/v1/page5/capital-estimate
{
  "capitalIntention": 100,
  "formData": {
    "business": "信息传输、软件和信息技术服务业",
    "people": 10,
    "shareholder": 3,
    "companyType": "有限责任公司",
    "namePref": "星河云创",
    "name": "星河云创科技有限公司",
    "scope": {
      "main": "软件开发",
      "others": ["技术服务"]
    }
  }
}
```

### 6. 推荐注册地址
```bash
POST /api/v1/page6/address-recommend
{
  "province": "北京市",
  "formData": {
    "business": "信息传输、软件和信息技术服务业",
    "people": 10,
    "shareholder": 3,
    "companyType": "有限责任公司",
    "namePref": "星河云创",
    "name": "星河云创科技有限公司",
    "scope": {
      "main": "软件开发",
      "others": ["技术服务"]
    },
    "capital": "100"
  }
}
```

## 其他命令

```bash
# 直接运行
python main.py

# 或使用 uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 响应格式

成功：
```json
{
  "code": 200,
  "status": "success",
  "message": "操作成功",
  "data": { ... }
}
```

错误：
```json
{
  "detail": "错误信息"
}
```