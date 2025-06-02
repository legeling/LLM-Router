"""
模型管理API路由
提供模型列表查询和测试功能
"""
import time
from fastapi import APIRouter, Depends, HTTPException
from loguru import logger

from ..models import ModelsListResponse, ModelInfo, ModelTestRequest, HealthCheckResponse
from ..auth import verify_api_key
from ..config import config
from ..services.llm_service import LLMService

router = APIRouter(prefix="/v1", tags=["Models"])


@router.get("/models", response_model=ModelsListResponse)
async def list_models(api_key: str = Depends(verify_api_key)):
    """
    获取可用模型列表（OpenAI兼容）
    """
    logger.info("获取模型列表请求")
    
    try:
        models = config.get_all_models()
        model_list = []
        
        for model in models:
            model_info = ModelInfo(
                id=model.name,
                object="model",
                created=int(time.time()),
                owned_by="llm-gateway",
                type=model.type,
                max_tokens=model.max_tokens,
                enabled=model.enabled
            )
            model_list.append(model_info)
        
        return ModelsListResponse(data=model_list)
    
    except Exception as e:
        logger.error(f"获取模型列表失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取模型列表失败: {str(e)}")


@router.post("/models/{model_name}/test")
async def test_model(
    model_name: str,
    request: ModelTestRequest = None,
    api_key: str = Depends(verify_api_key)
):
    """
    测试指定模型的可用性
    """
    logger.info(f"测试模型请求: {model_name}")
    
    try:
        test_message = request.test_message if request else "你好"
        result = await LLMService.test_model(model_name, test_message)
        logger.info(f"模型测试完成: {model_name}, 状态: {result.get('status')}")
        return result
    
    except Exception as e:
        logger.error(f"测试模型失败: {model_name}, {e}")
        raise HTTPException(status_code=500, detail=f"测试模型失败: {str(e)}")


@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """
    健康检查接口
    """
    try:
        models = config.get_all_models()
        models_status = {}
        
        # 简单检查每个模型的配置状态
        for model in models:
            models_status[model.name] = model.enabled
        
        return HealthCheckResponse(
            status="healthy",
            timestamp=str(int(time.time())),
            models_count=len(models),
            models_status=models_status
        )
    
    except Exception as e:
        logger.error(f"健康检查失败: {e}")
        raise HTTPException(status_code=500, detail=f"健康检查失败: {str(e)}")


@router.get("/models/{model_name}")
async def get_model_info(
    model_name: str,
    api_key: str = Depends(verify_api_key)
):
    """
    获取指定模型的详细信息
    """
    logger.info(f"获取模型信息: {model_name}")
    
    try:
        model_config = config.get_model_by_name(model_name)
        
        return ModelInfo(
            id=model_config.name,
            object="model",
            created=int(time.time()),
            owned_by="llm-gateway",
            type=model_config.type,
            max_tokens=model_config.max_tokens,
            enabled=model_config.enabled
        )
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"获取模型信息失败: {model_name}, {e}")
        raise HTTPException(status_code=500, detail=f"获取模型信息失败: {str(e)}") 