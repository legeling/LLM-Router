#!/usr/bin/env python3
"""
LLM网关运行脚本
支持本地运行和网络服务两种模式
"""
import argparse
import asyncio
from app.main import start_server
from app.config import config
from app.services.llm_service import LLMService
from app.models import ChatCompletionRequest, ChatMessage
from loguru import logger


async def local_chat(model: str, message: str):
    """本地聊天模式"""
    try:
        logger.info(f"本地模式 - 使用模型: {model}")
        logger.info(f"用户消息: {message}")
        
        # 构建请求
        request = ChatCompletionRequest(
            model=model,
            messages=[ChatMessage(role="user", content=message)]
        )
        
        # 调用模型
        response = await LLMService.chat_completion(request)
        
        # 提取回复内容
        if "choices" in response and len(response["choices"]) > 0:
            assistant_message = response["choices"][0]["message"]["content"]
            logger.info(f"助手回复: {assistant_message}")
            print(f"\n助手回复: {assistant_message}\n")
        else:
            print("未收到有效回复")
            
    except Exception as e:
        logger.error(f"本地聊天失败: {e}")
        print(f"错误: {e}")


async def test_all_models():
    """测试所有可用模型"""
    logger.info("开始测试所有模型...")
    models = config.get_all_models()
    
    for model in models:
        logger.info(f"测试模型: {model.name}")
        result = await LLMService.test_model(model.name, "你好")
        
        if result["status"] == "available":
            print(f"✅ {model.name}: 可用 (响应时间: {result.get('response_time', 'N/A')}s)")
        else:
            print(f"❌ {model.name}: 不可用 - {result.get('error', 'Unknown error')}")


def list_models():
    """列出所有配置的模型"""
    models = config.get_all_models()
    print("\n配置的模型列表:")
    print("-" * 50)
    
    for model in models:
        status = "✅ 启用" if model.enabled else "❌ 禁用"
        print(f"名称: {model.name}")
        print(f"类型: {model.type}")
        print(f"状态: {status}")
        print(f"最大Token: {model.max_tokens}")
        print(f"Base URL: {model.base_url}")
        print("-" * 50)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="LLM网关服务")
    parser.add_argument("--mode", choices=["server", "local", "test", "list"], default="server",
                       help="运行模式: server(网络服务), local(本地调用), test(测试模型), list(列出模型)")
    parser.add_argument("--host", default=None, help="服务器主机地址")
    parser.add_argument("--port", type=int, default=None, help="服务器端口")
    parser.add_argument("--reload", action="store_true", help="开发模式，自动重载")
    parser.add_argument("--model", default="gpt-3.5-turbo", help="本地模式使用的模型")
    parser.add_argument("--message", default="你好", help="本地模式的消息内容")
    
    args = parser.parse_args()
    
    if args.mode == "server":
        logger.info("启动网络服务模式")
        start_server(host=args.host, port=args.port, reload=args.reload)
    
    elif args.mode == "local":
        logger.info("启动本地调用模式")
        asyncio.run(local_chat(args.model, args.message))
    
    elif args.mode == "test":
        logger.info("启动模型测试模式")
        asyncio.run(test_all_models())
    
    elif args.mode == "list":
        list_models()


if __name__ == "__main__":
    main() 