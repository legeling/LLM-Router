# 快速开始指南

## 1. 安装依赖

```bash
pip install -r requirements.txt
```

## 2. 配置模型服务

编辑 `config/models.yaml` 文件，添加您的模型配置：

```yaml
# 示例：OpenAI服务配置
models:
  openai:
    - name: "gpt-3.5-turbo"
      type: "openai"
      base_url: "https://api.openai.com/v1"
      api_key: "sk-your-openai-api-key-here"
      max_tokens: 4096
      enabled: true

auth:
  api_keys:
    - "llm-gateway-key-001"
```

## 3. 启动网关服务

```bash
python run.py --mode server
```

## 4. 极简客户端调用

只需要几行代码就能调用各种大模型：

```python
from client import chat, list_models

# 获取可用模型
models = list_models()
print("可用模型:", models)

# 发送聊天请求  
response = chat("你好", "gpt-3.5-turbo")
print("回复:", response)

# 带参数调用
response = chat("用一句话总结AI", "gpt-3.5-turbo", max_tokens=50)
print("简短回复:", response)
```

## 5. 运行示例

```bash
# 运行极简示例
python simple_demo.py

# 测试项目配置
python test_basic.py

# 列出可用模型
python run.py --mode list
```

## 6. API调用示例

```bash
curl -X POST "http://localhost:8000/v1/chat/completions" \
  -H "Authorization: Bearer llm-gateway-key-001" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [
      {
        "role": "user",
        "content": "你好"
      }
    ],
    "max_tokens": 1000
  }'
```

## 常见配置示例

### OpenAI兼容服务
```yaml
- name: "qwen-turbo"
  type: "openai"
  base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"
  api_key: "sk-your-key"
  model_name: "qwen-turbo"
  enabled: true
```

### 需要认证的自定义服务
```yaml
- name: "custom-claude"
  type: "request"
  base_url: "https://api.custom.com"
  auth_url: "https://api.custom.com/auth"
  username: "your-username"
  password: "your-password"
  model_name: "claude-3-sonnet"
  enabled: true
```

## 故障排除

1. **配置文件错误**: 检查YAML格式是否正确
2. **模块导入失败**: 确保依赖已正确安装
3. **API调用失败**: 检查API密钥和网络连接
4. **端口被占用**: 使用 `--port` 参数指定其他端口 