"""
配置管理模块
负责加载和管理模型配置文件
"""
import yaml
import os
from typing import Dict, List, Any
from pydantic import BaseModel
from loguru import logger


class ModelConfig(BaseModel):
    """模型配置模型"""
    name: str
    type: str
    base_url: str
    api_key: str = ""
    model_name: str = ""
    max_tokens: int = 4096
    enabled: bool = True
    # Request服务特有配置 - 支持直接配置token
    auth_url: str = ""
    username: str = ""
    password: str = ""
    token: str = ""  # 直接配置的token
    token_cache_hours: int = 8


class ServerConfig(BaseModel):
    """服务器配置模型"""
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False


class AuthConfig(BaseModel):
    """认证配置模型"""
    api_keys: List[str] = []


class Config:
    """配置管理类"""
    
    def __init__(self, config_path: str = "config/models.yaml"):
        self.config_path = config_path
        self.models: Dict[str, List[ModelConfig]] = {}
        self.server: ServerConfig = ServerConfig()
        self.auth: AuthConfig = AuthConfig()
        self.load_config()
    
    def load_config(self):
        """加载配置文件"""
        try:
            if not os.path.exists(self.config_path):
                logger.error(f"配置文件不存在: {self.config_path}")
                return
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
            
            # 加载模型配置
            if 'models' in config_data:
                for category, models in config_data['models'].items():
                    self.models[category] = [
                        ModelConfig(**model) for model in models
                    ]
            
            # 加载服务器配置
            if 'server' in config_data:
                self.server = ServerConfig(**config_data['server'])
            
            # 加载认证配置
            if 'auth' in config_data:
                self.auth = AuthConfig(**config_data['auth'])
            
            logger.info(f"配置文件加载成功: {self.config_path}")
            
        except Exception as e:
            logger.error(f"加载配置文件失败: {e}")
            raise
    
    def get_all_models(self) -> List[ModelConfig]:
        """获取所有启用的模型"""
        all_models = []
        for models in self.models.values():
            all_models.extend([model for model in models if model.enabled])
        return all_models
    
    def get_model_by_name(self, name: str) -> ModelConfig:
        """根据名称获取模型配置"""
        for models in self.models.values():
            for model in models:
                if model.name == name and model.enabled:
                    return model
        raise ValueError(f"模型 {name} 未找到或未启用")
    
    def is_valid_api_key(self, api_key: str) -> bool:
        """验证API密钥"""
        return api_key in self.auth.api_keys


# 全局配置实例
config = Config() 