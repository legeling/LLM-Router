"""
LLM服务模块
统一处理不同类型的大模型服务调用
"""
import uuid
import time
from typing import Dict, Any, List
import httpx
from loguru import logger
from fastapi import HTTPException

from ..config import ModelConfig, config
from ..models import ChatCompletionRequest, ChatCompletionResponse, ChatMessage
from ..auth import TokenManager


class LLMService:
    """大模型服务统一调用类"""
    
    @staticmethod
    async def chat_completion(request: ChatCompletionRequest) -> Dict[str, Any]:
        """统一的聊天完成接口"""
        try:
            # 获取模型配置
            model_config = config.get_model_by_name(request.model)
            
            # 根据模型类型选择调用方式
            if model_config.type == "openai":
                return await LLMService._call_openai_api(model_config, request)
            elif model_config.type == "request":
                return await LLMService._call_request_api(model_config, request)
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"不支持的模型类型: {model_config.type}"
                )
        
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            logger.error(f"调用模型失败: {request.model}, {e}")
            raise HTTPException(status_code=500, detail=f"模型调用失败: {str(e)}")
    
    @staticmethod
    async def _call_openai_api(model_config: ModelConfig, request: ChatCompletionRequest) -> Dict[str, Any]:
        """调用OpenAI标准格式API"""
        url = f"{model_config.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {model_config.api_key}",
            "Content-Type": "application/json"
        }
        
        # 构建请求数据
        data = {
            "model": model_config.model_name or model_config.name,
            "messages": [msg.dict() for msg in request.messages],
            "max_tokens": request.max_tokens or model_config.max_tokens,
            "temperature": request.temperature,
            "top_p": request.top_p,
            "stream": request.stream
        }
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(url, headers=headers, json=data)
                
                if response.status_code == 200:
                    return response.json()
                else:
                    error_msg = f"API调用失败: {response.status_code}, {response.text}"
                    logger.error(error_msg)
                    raise HTTPException(status_code=response.status_code, detail=error_msg)
        
        except httpx.RequestError as e:
            error_msg = f"网络请求失败: {model_config.name}, {e}"
            logger.error(error_msg)
            raise HTTPException(status_code=500, detail=error_msg)
    
    @staticmethod
    async def _call_request_api(model_config: ModelConfig, request: ChatCompletionRequest) -> Dict[str, Any]:
        """调用Request服务API（需要token认证）"""
        # 获取token
        token = await TokenManager.get_token(model_config)
        
        url = f"{model_config.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # 构建请求数据
        data = {
            "model": model_config.model_name or model_config.name,
            "messages": [msg.dict() for msg in request.messages],
            "max_tokens": request.max_tokens or model_config.max_tokens,
            "temperature": request.temperature,
            "top_p": request.top_p,
            "stream": request.stream
        }
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(url, headers=headers, json=data)
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 401:
                    # Token可能过期，清除缓存并重试
                    logger.warning(f"Token可能过期，清除缓存: {model_config.name}")
                    TokenManager.clear_token(model_config.name, model_config.username)
                    
                    # 重新获取token并重试
                    token = await TokenManager.get_token(model_config)
                    headers["Authorization"] = f"Bearer {token}"
                    
                    response = await client.post(url, headers=headers, json=data)
                    if response.status_code == 200:
                        return response.json()
                    else:
                        error_msg = f"重试后仍失败: {response.status_code}, {response.text}"
                        logger.error(error_msg)
                        raise HTTPException(status_code=response.status_code, detail=error_msg)
                else:
                    error_msg = f"API调用失败: {response.status_code}, {response.text}"
                    logger.error(error_msg)
                    raise HTTPException(status_code=response.status_code, detail=error_msg)
        
        except httpx.RequestError as e:
            error_msg = f"网络请求失败: {model_config.name}, {e}"
            logger.error(error_msg)
            raise HTTPException(status_code=500, detail=error_msg)
    
    @staticmethod
    async def test_model(model_name: str, test_message: str = "你好") -> Dict[str, Any]:
        """测试模型可用性"""
        try:
            # 构建测试请求
            test_request = ChatCompletionRequest(
                model=model_name,
                messages=[ChatMessage(role="user", content=test_message)],
                max_tokens=50
            )
            
            start_time = time.time()
            response = await LLMService.chat_completion(test_request)
            end_time = time.time()
            
            return {
                "model": model_name,
                "status": "available",
                "response_time": round(end_time - start_time, 2),
                "test_message": test_message,
                "response": response
            }
        
        except Exception as e:
            return {
                "model": model_name,
                "status": "unavailable",
                "error": str(e),
                "test_message": test_message
            } 