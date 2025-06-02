"""
LLM网关主应用
FastAPI应用入口文件
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
import uvicorn
import sys

from .config import config
from .api import chat, models

# 配置日志
logger.remove()
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
)

# 创建FastAPI应用
app = FastAPI(
    title="LLM Gateway",
    description="大模型网关服务 - 统一不同大模型服务的API接口",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 全局异常处理
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """HTTP异常处理"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "message": exc.detail,
                "type": "http_error",
                "code": exc.status_code
            }
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """通用异常处理"""
    logger.error(f"未处理的异常: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "message": "内部服务器错误",
                "type": "internal_error",
                "code": 500
            }
        }
    )


# 启动事件
@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    logger.info("LLM网关服务启动中...")
    logger.info(f"配置文件: {config.config_path}")
    logger.info(f"可用模型数量: {len(config.get_all_models())}")
    logger.info("LLM网关服务启动完成")


# 关闭事件
@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    logger.info("LLM网关服务正在关闭...")


# 根路径
@app.get("/")
async def root():
    """根路径信息"""
    return {
        "service": "LLM Gateway",
        "version": "1.0.0",
        "description": "大模型网关服务",
        "docs": "/docs",
        "health": "/v1/health"
    }


# 注册路由
app.include_router(chat.router)
app.include_router(models.router)


def start_server(host: str = None, port: int = None, reload: bool = False):
    """启动服务器"""
    server_host = host or config.server.host
    server_port = port or config.server.port
    
    logger.info(f"启动服务器: http://{server_host}:{server_port}")
    
    uvicorn.run(
        "app.main:app",
        host=server_host,
        port=server_port,
        reload=reload,
        log_level="info"
    )


if __name__ == "__main__":
    start_server(reload=True) 