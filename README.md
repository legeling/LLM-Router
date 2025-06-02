# LLM网关服务

一个基于FastAPI的大模型网关服务，用于统一管理和调用不同的大模型服务，提供标准的OpenAI兼容API。

## 功能特性

- ✅ **多模型支持**: 支持OpenAI标准格式和自定义Request服务
- ✅ **统一接口**: 提供标准的OpenAI兼容API
- ✅ **智能路由**: 根据模型名称自动路由到对应服务
- ✅ **Token缓存**: Request服务token自动缓存8小时
- ✅ **双模式运行**: 支持网络服务和本地调用两种模式
- ✅ **健康检查**: 模型可用性监控和测试
- ✅ **配置文件**: 通过YAML文件灵活配置模型
- ✅ **API认证**: 内置API密钥验证机制

## 项目结构

```
LLM网关/
├── app/                      # 主应用目录
│   ├── __init__.py
│   ├── main.py              # FastAPI应用入口
│   ├── config.py            # 配置管理
│   ├── models.py            # 数据模型定义
│   ├── auth.py              # 认证模块
│   ├── api/                 # API路由
│   │   ├── __init__.py
│   │   ├── chat.py          # 聊天接口
│   │   └── models.py        # 模型管理接口
│   └── services/            # 业务服务
│       ├── __init__.py
│       └── llm_service.py   # LLM服务调用
├── config/                  # 配置文件目录
│   └── models.yaml          # 模型配置文件
├── client.py               # 极简客户端
├── simple_demo.py          # 极简使用示例
├── requirements.txt         # 依赖包
├── run.py                  # 运行脚本
├── test_basic.py           # 基本测试脚本
├── QUICKSTART.md           # 快速开始指南
└── README.md               # 项目说明
```

## 安装部署

### 1. 环境要求

- Python 3.8+
- pip

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置模型

编辑 `config/models.yaml` 文件，配置您的模型服务：

```yaml
# 示例配置
models:
  openai:
    - name: "gpt-3.5-turbo"
      type: "openai"
      base_url: "https://api.openai.com/v1"
      api_key: "your-openai-api-key"
      max_tokens: 4096
      enabled: true

  request:
    - name: "custom-model"
      type: "request"
      base_url: "https://your-api.com"
      auth_url: "https://your-api.com/auth"
      username: "your-username"
      password: "your-password"
      model_name: "custom-model-name"
      max_tokens: 4096
      enabled: true

auth:
  api_keys:
    - "your-api-key-1"
    - "your-api-key-2"
```

## 使用方法

### 1. 网络服务模式

启动HTTP服务器，提供网络API：

```bash
# 基本启动
python run.py --mode server

# 自定义端口和主机
python run.py --mode server --host 0.0.0.0 --port 8080

# 开发模式（自动重载）
python run.py --mode server --reload
```

服务启动后，访问：
- API文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/v1/health

### 2. 本地调用模式

直接在命令行中调用模型：

```bash
# 使用默认模型和消息
python run.py --mode local

# 指定模型和消息
python run.py --mode local --model gpt-4 --message "你是谁？"
```

### 3. 模型管理

```bash
# 列出所有配置的模型
python run.py --mode list

# 测试所有模型可用性
python run.py --mode test
```

## 客户端调用

### 极简Python客户端

只需要几行代码，像调用OpenAI一样简单：

```python
from client import chat, list_models

# 获取可用模型 - 1行代码
models = list_models()

# 发送聊天请求 - 1行代码  
response = chat("你好", "gpt-3.5-turbo")
print(response)

# 带参数调用
response = chat(
    "用一句话总结AI发展", 
    "gpt-3.5-turbo", 
    max_tokens=50, 
    temperature=0.7
)

# 自定义网关地址
response = chat(
    "你好", 
    "gpt-3.5-turbo",
    base_url="http://localhost:8000",
    api_key="your-api-key"
)
```

### 运行示例

```bash
# 运行极简示例
python simple_demo.py

# 运行客户端测试
python client.py
```

## API接口

### 聊天完成接口

```http
POST /v1/chat/completions
Authorization: Bearer your-api-key
Content-Type: application/json

{
  "model": "gpt-3.5-turbo",
  "messages": [
    {
      "role": "user",
      "content": "你好"
    }
  ],
  "max_tokens": 1000,
  "temperature": 0.7
}
```

### 模型列表接口

```http
GET /v1/models
Authorization: Bearer your-api-key
```

### 模型测试接口

```http
POST /v1/models/{model_name}/test
Authorization: Bearer your-api-key
Content-Type: application/json

{
  "test_message": "你好"
}
```

### 健康检查接口

```http
GET /v1/health
```

## 模型类型说明

### OpenAI类型

适用于兼容OpenAI API格式的服务：

```yaml
- name: "gpt-3.5-turbo"
  type: "openai"
  base_url: "https://api.openai.com/v1"
  api_key: "your-api-key"
  max_tokens: 4096
  enabled: true
```

### Request类型

适用于需要token认证的自定义服务，支持两种认证方式：

**方式1：直接配置token（推荐）**
```yaml
- name: "custom-model"
  type: "request"
  base_url: "https://your-api.com"
  token: "your-fixed-token-here"  # 直接配置写死的token
  model_name: "actual-model-name"
  max_tokens: 4096
  enabled: true
```

**方式2：用户名密码认证（自动获取token）**
```yaml
- name: "custom-model"
  type: "request"
  base_url: "https://your-api.com"
  auth_url: "https://your-api.com/auth"
  username: "your-username"
  password: "your-password"
  model_name: "actual-model-name"
  max_tokens: 4096
  enabled: true
  token_cache_hours: 8
```

## 配置说明

### 模型配置参数

- `name`: 模型名称（用户调用时使用）
- `type`: 模型类型（openai 或 request）
- `base_url`: API基础URL
- `api_key`: API密钥（OpenAI类型）
- `model_name`: 实际模型名称（可选，默认使用name）
- `max_tokens`: 最大token数
- `enabled`: 是否启用
- `auth_url`: 认证URL（Request类型，用户名密码认证时需要）
- `username`: 用户名（Request类型，用户名密码认证时需要）
- `password`: 密码（Request类型，用户名密码认证时需要）
- `token`: 直接配置的token（Request类型，推荐使用）
- `token_cache_hours`: Token缓存时间（Request类型，用户名密码认证时有效）

### 服务器配置

```yaml
server:
  host: "0.0.0.0"
  port: 8000
  debug: false
```

### 认证配置

```yaml
auth:
  api_keys:
    - "api-key-1"
    - "api-key-2"
```

## 开发调试

### 查看日志

服务运行时会输出详细的日志信息，包括：
- 请求接收和处理
- 模型调用状态
- 错误信息
- Token缓存状态

### 错误处理

- API密钥无效: HTTP 401
- 模型不存在: HTTP 404
- 模型调用失败: HTTP 500
- 网络错误: HTTP 500

### Token缓存机制

Request类型的服务会自动缓存认证token：
- 缓存时间: 8小时（可配置）
- 自动刷新: token过期时自动重新获取
- 错误重试: 401错误时自动清除缓存并重试

## 注意事项

1. **API密钥安全**: 请妥善保管配置文件中的API密钥
2. **网络安全**: 生产环境建议使用HTTPS
3. **资源限制**: 注意各模型服务的调用限制
4. **日志管理**: 生产环境建议配置日志轮转
5. **监控告警**: 建议设置模型可用性监控

## 常见问题

### Q: 如何添加新的模型？
A: 在 `config/models.yaml` 中添加新的模型配置，重启服务即可。

### Q: 如何处理模型调用失败？
A: 检查模型配置、网络连接和API密钥，使用测试模式排查问题。

### Q: Token缓存在哪里？
A: Token缓存在内存中，服务重启后会清空。

### Q: 如何自定义API密钥？
A: 在配置文件的 `auth.api_keys` 中添加您的密钥。

## 许可证

MIT License 