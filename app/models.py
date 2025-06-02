"""
数据模型定义
定义API请求和响应的数据结构
"""
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """聊天消息模型"""
    role: str = Field(..., description="消息角色: user, assistant, system")
    content: str = Field(..., description="消息内容")


class ChatCompletionRequest(BaseModel):
    """聊天完成请求模型"""
    model: str = Field(..., description="模型名称")
    messages: List[ChatMessage] = Field(..., description="消息列表")
    max_tokens: Optional[int] = Field(None, description="最大token数")
    temperature: Optional[float] = Field(0.7, description="温度参数")
    top_p: Optional[float] = Field(1.0, description="top_p参数")
    stream: Optional[bool] = Field(False, description="是否流式输出")


class ChatCompletionResponse(BaseModel):
    """聊天完成响应模型"""
    id: str = Field(..., description="响应ID")
    object: str = Field("chat.completion", description="对象类型")
    created: int = Field(..., description="创建时间戳")
    model: str = Field(..., description="使用的模型")
    choices: List[Dict[str, Any]] = Field(..., description="选择列表")
    usage: Dict[str, int] = Field(..., description="使用统计")


class ModelInfo(BaseModel):
    """模型信息模型"""
    id: str = Field(..., description="模型ID")
    object: str = Field("model", description="对象类型")
    created: int = Field(..., description="创建时间")
    owned_by: str = Field(..., description="拥有者")
    type: str = Field(..., description="模型类型")
    max_tokens: int = Field(..., description="最大token数")
    enabled: bool = Field(..., description="是否启用")


class ModelsListResponse(BaseModel):
    """模型列表响应"""
    object: str = Field("list", description="对象类型")
    data: List[ModelInfo] = Field(..., description="模型列表")


class HealthCheckResponse(BaseModel):
    """健康检查响应"""
    status: str = Field(..., description="服务状态")
    timestamp: str = Field(..., description="检查时间")
    models_count: int = Field(..., description="可用模型数量")
    models_status: Dict[str, bool] = Field(..., description="各模型状态")


class ErrorResponse(BaseModel):
    """错误响应模型"""
    error: Dict[str, Any] = Field(..., description="错误信息")


class TokenResponse(BaseModel):
    """Token响应模型"""
    access_token: str = Field(..., description="访问令牌")
    token_type: str = Field("Bearer", description="令牌类型")
    expires_in: int = Field(..., description="过期时间(秒)")


class ModelTestRequest(BaseModel):
    """模型测试请求"""
    model: str = Field(..., description="要测试的模型名称")
    test_message: str = Field("你好", description="测试消息") 