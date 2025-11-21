<div align="center">
  <h1>LLM-Router · Unified LLM API Gateway</h1>
  <p>A production-ready, high-performance gateway that unifies multiple LLM providers under a single OpenAI-compatible API.</p>
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

## 🚀 Key Features

- **🔄 Multi-Provider Support**: Unified interface for OpenAI, Anthropic, DeepSeek, and custom providers
- **⚡ High Performance**: Async architecture with connection pooling and request caching
- **🔒 Enterprise Security**: API key authentication, rate limiting, and request validation
- **📊 OpenAI Compatible**: Drop-in replacement for OpenAI API clients
- **🌐 Streaming Support**: Real-time response streaming via Server-Sent Events
- **📈 Observability**: Built-in metrics, health checks, and structured logging
- **🐳 Production Ready**: Docker deployment with Kubernetes manifests
- **🔧 Dynamic Configuration**: Hot-reload model configurations without restart

## 📦 Quick Start

### Using Docker (Recommended)

```bash
# Clone the repository
git clone git@github.com:legeling/LLM-Router.git
cd LLM-Router

# Copy and edit configuration
cp .env.example .env
cp config/models.example.json config/models.json
# Edit both files with your API keys and settings

# Start with Docker Compose
docker-compose up -d

# Check health
curl http://localhost:8000/v1/health
```

### Manual Installation

```bash
# Clone and setup
git clone git@github.com:legeling/LLM-Router.git
cd LLM-Router

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup configuration
cp .env.example .env
cp config/models.example.json config/models.json

# Run the server
python run.py
```

### First API Call

```bash
curl -X POST "http://localhost:8000/v1/chat/completions" \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openai-gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "Hello, LLM-Router!"}],
    "stream": false
  }'
```

## 🏗️ Architecture Overview

```
LLM-Router/
├── app/                    # Core application
│   ├── main.py            # FastAPI application entry
│   ├── config.py          # Configuration management
│   ├── models.py          # Pydantic data models
│   ├── auth.py            # Authentication middleware
│   ├── api/               # API routes
│   │   ├── chat.py        # Chat completion endpoints
│   │   ├── models.py      # Model management
│   │   └── health.py      # Health checks
│   └── services/          # LLM provider services
│       └── llm_service.py # Service implementations
├── config/                # Configuration files
│   └── models.json        # Model definitions
├── docs/                  # Documentation
├── tests/                 # Test suite
└── monitoring/            # Observability configs
```

## 📚 API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🔧 Configuration

### Environment Variables

Key environment variables in `.env`:

```bash
# Server
HOST=0.0.0.0
PORT=8000
DEBUG=false

# Authentication
API_KEY=your-secure-api-key-here

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/llm_router.log

# Cache (Optional)
REDIS_URL=redis://localhost:6379/0
CACHE_TTL=3600

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
```

### Model Configuration

Configure LLM providers in `config/models.json`:

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

## 🚀 Deployment

### Docker Production

```bash
# Build production image
docker build -t llm-router:latest .

# Run with environment file
docker run -d \
  --name llm-router \
  -p 8000:8000 \
  --env-file .env \
  -v $(pwd)/config:/app/config:ro \
  llm-router:latest
```

### Kubernetes

```bash
# Apply manifests
kubectl apply -f k8s/

# Check deployment
kubectl get pods -l app=llm-router
```

### Cloud Providers

- **AWS**: Deploy to ECS or EKS
- **GCP**: Deploy to Cloud Run or GKE
- **Azure**: Deploy to Container Instances or AKS

## 📊 Supported Providers

| Provider | Status | Models | Streaming |
|---|---|---|---|
| OpenAI | ✅ | GPT-3.5, GPT-4 | ✅ |
| DeepSeek | ✅ | DeepSeek-Chat | ✅ |
| Anthropic | 🚧 | Claude 3 | ✅ |
| Custom API | ✅ | Any OpenAI-compatible | ✅ |
| Local Models | ✅ | Ollama, LM Studio | ✅ |

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test
pytest tests/test_chat.py

# Load testing
locust -f tests/load_test.py
```

## 📈 Monitoring & Metrics

### Health Checks

- **Liveness**: `/v1/health`
- **Readiness**: `/v1/health/ready`
- **Metrics**: `/metrics` (Prometheus)

### Observability Stack

```bash
# Enable monitoring stack
docker-compose --profile monitoring up -d

# Access dashboards
# Grafana: http://localhost:3000 (admin/admin)
# Prometheus: http://localhost:9090
```

## 🔄 Development

### Setup Development Environment

```bash
# Clone repository
git clone git@github.com:legeling/LLM-Router.git
cd LLM-Router

# Setup development environment
python -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run in development mode
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Code Quality

```bash
# Format code
black .
isort .

# Lint
flake8 .
mypy app/

# Security scan
bandit -r app/
safety check
```

## 📋 Roadmap

See [OPTIMIZATION_PLAN.md](../OPTIMIZATION_PLAN.md) for comprehensive roadmap:

- [ ] **Phase 1**: Code translation to English, type hints, error handling
- [ ] **Phase 2**: Architecture refactoring, security enhancements  
- [ ] **Phase 3**: Production readiness, monitoring, documentation
- [ ] **Phase 4**: Advanced features, performance optimization

## 📝 Changelog

| Date | Version | Highlights |
|---|---|---|
| 2025/11/21 | - | Added production-ready infrastructure, CI/CD, Docker deployment |
| TBD | 1.0.0 | Initial stable release (planned) |

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

### Quick Contribution Steps

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see [LICENSE](../LICENSE) file for details.

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=legeling/LLM-Router&type=Date)](https://star-history.com/#legeling/LLM-Router&Date)

## 💬 Support

- **Issues**: [GitHub Issues](https://github.com/legeling/LLM-Router/issues)
- **Discussions**: [GitHub Discussions](https://github.com/legeling/LLM-Router/discussions)
- **Documentation**: [Wiki](https://github.com/legeling/LLM-Router/wiki)

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework
- [OpenAI](https://openai.com/) - API compatibility standards
- All contributors and users who make this project better

---

<div align="center">
  <p><strong>If this project helps your work, consider giving it a ⭐!</strong></p>
  <p>Built with ❤️ by the community</p>
</div>
