"""
认证模块
处理API密钥验证和token缓存管理
"""
import time
from typing import Optional, Dict
from datetime import datetime, timedelta
from cachetools import TTLCache
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import httpx
from loguru import logger

from .config import config


# Token缓存，TTL为8小时
token_cache: TTLCache = TTLCache(maxsize=100, ttl=8*3600)

# Bearer token安全方案
security = HTTPBearer()


async def verify_api_key(credentials: HTTPAuthorizationCredentials = Security(security)) -> str:
    """验证API密钥"""
    api_key = credentials.credentials
    
    if not config.is_valid_api_key(api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的API密钥",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return api_key


class TokenManager:
    """Token管理器，用于Request服务的认证"""
    
    @staticmethod
    async def get_token(service_config) -> str:
        """获取或刷新token"""
        # 如果直接配置了token，优先使用
        if service_config.token:
            logger.info(f"使用配置的token: {service_config.name}")
            return service_config.token
        
        # 如果没有配置token，使用用户名密码认证
        cache_key = f"{service_config.name}_{service_config.username}"
        
        # 检查缓存中是否有有效token
        if cache_key in token_cache:
            logger.info(f"使用缓存token: {service_config.name}")
            return token_cache[cache_key]
        
        # 获取新token
        try:
            async with httpx.AsyncClient() as client:
                auth_data = {
                    "username": service_config.username,
                    "password": service_config.password
                }
                
                response = await client.post(
                    service_config.auth_url,
                    json=auth_data,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    token_data = response.json()
                    access_token = token_data.get("access_token")
                    
                    if access_token:
                        # 存储到缓存
                        token_cache[cache_key] = access_token
                        logger.info(f"获取新token成功: {service_config.name}")
                        return access_token
                    else:
                        raise HTTPException(
                            status_code=500,
                            detail=f"Token响应格式错误: {service_config.name}"
                        )
                else:
                    raise HTTPException(
                        status_code=500,
                        detail=f"获取token失败: {service_config.name}, 状态码: {response.status_code}"
                    )
        
        except httpx.RequestError as e:
            logger.error(f"获取token网络错误: {service_config.name}, {e}")
            raise HTTPException(
                status_code=500,
                detail=f"获取token网络错误: {service_config.name}"
            )
        except Exception as e:
            logger.error(f"获取token未知错误: {service_config.name}, {e}")
            raise HTTPException(
                status_code=500,
                detail=f"获取token未知错误: {service_config.name}"
            )
    
    @staticmethod
    def clear_token(service_name: str, username: str):
        """清除指定服务的token缓存"""
        cache_key = f"{service_name}_{username}"
        if cache_key in token_cache:
            del token_cache[cache_key]
            logger.info(f"清除token缓存: {service_name}")
    
    @staticmethod
    def get_cache_info() -> Dict:
        """获取缓存信息"""
        return {
            "cache_size": len(token_cache),
            "max_size": token_cache.maxsize,
            "ttl": token_cache.ttl,
            "cached_services": list(token_cache.keys())
        } 