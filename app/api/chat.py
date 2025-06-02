"""
聊天API路由
提供标准的OpenAI兼容的聊天接口
"""
from fastapi import APIRouter, Depends, HTTPException
from loguru import logger

from ..models import ChatCompletionRequest, ChatCompletionResponse
from ..auth import verify_api_key
from ..services.llm_service import LLMService

router = APIRouter(prefix="/v1", tags=["Chat"])


@router.post("/chat/completions", response_model=dict)
async def chat_completions(
    request: ChatCompletionRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    聊天完成接口（OpenAI兼容）
    
    支持的参数：
    - model: 模型名称
    - messages: 消息列表
    - max_tokens: 最大token数
    - temperature: 温度参数
    - top_p: top_p参数
    - stream: 是否流式输出
    """
    logger.info(f"收到聊天请求: model={request.model}, messages_count={len(request.messages)}")
    
    try:
        response = await LLMService.chat_completion(request)
        logger.info(f"聊天请求成功: model={request.model}")
        return response
    
    except Exception as e:
        logger.error(f"聊天请求失败: model={request.model}, error={e}")
        raise 