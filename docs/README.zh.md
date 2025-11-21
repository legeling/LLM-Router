<div align="center">
  <h1>LLM-Router · 统一 LLM API 网关</h1>
  <p>一个生产就绪、高性能的网关服务，将多个 LLM 提供商统一在单个 OpenAI 兼容的 API 下。</p>
  <p>
    <a href="https://github.com/legeling/LLM-Router/stargazers"><img src="https://img.shields.io/github/stars/legeling/LLM-Router?style=flat-square" alt="GitHub Stars"/></a>
    <a href="https://github.com/legeling/LLM-Router/network/members"><img src="https://img.shields.io/github/forks/legeling/LLM-Router?style=flat-square" alt="GitHub Forks"/></a>
    <a href="https://github.com/legeling/LLM-Router/watchers"><img src="https://img.shields.io/github/watchers/legeling/LLM-Router?style=flat-square" alt="GitHub Watchers"/></a>
    <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python Version"/>
    <a href="https://github.com/legeling/LLM-Router/issues"><img src="https://img.shields.io/github/issues/legeling/LLM-Router?style=flat-square" alt="GitHub Issues"/></a>
    <img src="https://img.shields.io/github/license/legeling/LLM-Router?style=flat-square" alt="License"/>
    <img src="https://img.shields.io/badge/Status-Production%20Ready-brightgreen?style=flat-square" alt="Status"/>
  </p>
</div>

<p align="center">
  <a href="./README.en.md">English</a> ·
  <a href="./README.zh.md">简体中文</a>
</p>

---

## 🚀 核心特性

- **🔄 多提供商支持**: 统一接口支持 OpenAI、Anthropic、DeepSeek 和自定义提供商
- **⚡ 高性能**: 异步架构，支持连接池和请求缓存
- **🔒 企业级安全**: API 密钥认证、速率限制和请求验证
- **📊 OpenAI 兼容**: 可直接替换 OpenAI API 客户端
- **🌐 流式支持**: 通过服务器发送事件实现实时响应流
- **📈 可观测性**: 内置指标、健康检查和结构化日志
- **🐳 生产就绪**: Docker 部署，支持 Kubernetes 清单
- **🔧 动态配置**: 无需重启即可热重载模型配置

## 📦 快速开始

### 使用 Docker（推荐）

```bash
# 克隆仓库
git clone git@github.com:legeling/LLM-Router.git
cd LLM-Router

# 复制并编辑配置
cp .env.example .env
cp config/models.example.json config/models.json
# 编辑这两个文件，填入你的 API 密钥和设置

# 使用 Docker Compose 启动
docker-compose up -d

# 检查健康状态
curl http://localhost:8000/v1/health
```

### 手动安装

```bash
# 克隆并设置
git clone git@github.com:legeling/LLM-Router.git
cd LLM-Router

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 设置配置
cp .env.example .env
cp config/models.example.json config/models.json

# 运行服务器
python run.py
```

### 首次 API 调用

```bash
curl -X POST "http://localhost:8000/v1/chat/completions" \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openai-gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "你好，LLM-Router！"}],
    "stream": false
  }'
```

## 🏗️ 架构概览

```
LLM-Router/
├── app/                    # 核心应用
│   ├── main.py            # FastAPI 应用入口
│   ├── config.py          # 配置管理
│   ├── models.py          # Pydantic 数据模型
│   ├── auth.py            # 认证中间件
│   ├── api/               # API 路由
│   │   ├── chat.py        # 聊天完成端点
│   │   ├── models.py      # 模型管理
│   │   └── health.py      # 健康检查
│   └── services/          # LLM 提供商服务
│       └── llm_service.py # 服务实现
├── config/                # 配置文件
│   └── models.json        # 模型定义
├── docs/                  # 文档
├── tests/                 # 测试套件
└── monitoring/            # 可观测性配置
```

## 📚 API 文档

启动后访问：
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🔧 配置

### 环境变量

`.env` 中的关键环境变量：

```bash
# 服务器
HOST=0.0.0.0
PORT=8000
DEBUG=false

# 认证
API_KEY=your-secure-api-key-here

# 日志
LOG_LEVEL=INFO
LOG_FILE=logs/llm_router.log

# 缓存（可选）
REDIS_URL=redis://localhost:6379/0
CACHE_TTL=3600

# 速率限制
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
```

### 模型配置

在 `config/models.json` 中配置 LLM 提供商：

```json
{
  "models": [
    {
      "id": "openai-gpt-4",
      "name": "OpenAI GPT-4",
      "provider": "openai",
      "type": "openai_compatible",
      "config": {
        "base_url": "https://api.openai.com/v1",
        "api_key": "sk-your-openai-api-key",
        "model": "gpt-4"
      },
      "enabled": true
    }
  ]
}
```

## 🚀 部署

### Docker 生产环境

```bash
# 构建生产镜像
docker build -t llm-router:latest .

# 使用环境文件运行
docker run -d \
  --name llm-router \
  -p 8000:8000 \
  --env-file .env \
  -v $(pwd)/config:/app/config:ro \
  llm-router:latest
```

### Kubernetes

```bash
# 应用清单
kubectl apply -f k8s/

# 检查部署
kubectl get pods -l app=llm-router
```

### 云服务提供商

- **AWS**: 部署到 ECS 或 EKS
- **GCP**: 部署到 Cloud Run 或 GKE
- **Azure**: 部署到 Container Instances 或 AKS

## 📊 支持的提供商

| 提供商 | 状态 | 模型 | 流式支持 |
|---|---|---|---|
| OpenAI | ✅ | GPT-3.5, GPT-4 | ✅ |
| DeepSeek | ✅ | DeepSeek-Chat | ✅ |
| Anthropic | 🚧 | Claude 3 | ✅ |
| 自定义 API | ✅ | 任何 OpenAI 兼容 | ✅ |
| 本地模型 | ✅ | Ollama, LM Studio | ✅ |

## 🧪 测试

```bash
# 运行所有测试
pytest

# 运行覆盖率测试
pytest --cov=app --cov-report=html

# 运行特定测试
pytest tests/test_chat.py

# 负载测试
locust -f tests/load_test.py
```

## 📈 监控与指标

### 健康检查

- **存活检查**: `/v1/health`
- **就绪检查**: `/v1/health/ready`
- **指标**: `/metrics` (Prometheus)

### 可观测性栈

```bash
# 启用监控栈
docker-compose --profile monitoring up -d

# 访问仪表板
# Grafana: http://localhost:3000 (admin/admin)
# Prometheus: http://localhost:9090
```

## 🔄 开发

### 设置开发环境

```bash
# 克隆仓库
git clone git@github.com:legeling/LLM-Router.git
cd LLM-Router

# 设置开发环境
python -m venv venv
source venv/bin/activate

# 安装开发依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 开发模式运行
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 代码质量

```bash
# 格式化代码
black .
isort .

# 代码检查
flake8 .
mypy app/

# 安全扫描
bandit -r app/
safety check
```

## 📋 路线图

查看 [OPTIMIZATION_PLAN.md](../OPTIMIZATION_PLAN.md) 了解全面路线图：

- [ ] **阶段 1**: 代码翻译为英文、类型提示、错误处理
- [ ] **阶段 2**: 架构重构、安全增强  
- [ ] **阶段 3**: 生产就绪、监控、文档
- [ ] **阶段 4**: 高级功能、性能优化

## 📝 更新日志

| 日期 | 版本 | 亮点 |
|---|---|---|
| 2025/11/21 | - | 添加生产就绪基础设施、CI/CD、Docker 部署 |
| 待定 | 1.0.0 | 初始稳定版本（计划中）|

## 🤝 贡献

我们欢迎贡献！请查看 [CONTRIBUTING.md](../CONTRIBUTING.md) 了解指南。

### 快速贡献步骤

1. Fork 仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](../LICENSE) 文件。

## ⭐ Star 历史

[![Star History Chart](https://api.star-history.com/svg?repos=legeling/LLM-Router&type=Date)](https://star-history.com/#legeling/LLM-Router&Date)

## 💬 支持

- **Issues**: [GitHub Issues](https://github.com/legeling/LLM-Router/issues)
- **Discussions**: [GitHub Discussions](https://github.com/legeling/LLM-Router/discussions)
- **文档**: [Wiki](https://github.com/legeling/LLM-Router/wiki)

## 🙏 致谢

- [FastAPI](https://fastapi.tiangolo.com/) - 现代、快速的 Web 框架
- [OpenAI](https://openai.com/) - API 兼容性标准
- 所有让这个项目变得更好的贡献者和用户

---

<div align="center">
  <p><strong>如果这个项目对你的工作有帮助，请考虑给个 ⭐！</strong></p>
  <p>由社区用 ❤️ 构建</p>
</div>
