"""
MCP to FastAPI Adapter
将MCP服务转换为FastAPI端点，使其可以同时作为MCP服务和REST API使用
"""

import inspect
import logging
from typing import Any, Callable, Dict, List, Optional, get_type_hints
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, create_model
from mcp.server.fastmcp import FastMCP

logger = logging.getLogger(__name__)


class MCPToolAdapter:
    """将MCP工具适配为FastAPI端点"""
    
    def __init__(self, mcp_server: FastMCP, prefix: str = ""):
        """
        初始化适配器
        
        Args:
            mcp_server: FastMCP服务器实例
            prefix: API路径前缀，例如 "/chembl"
        """
        self.mcp_server = mcp_server
        self.prefix = prefix.rstrip("/")
        self.router = APIRouter()
        
    def _create_request_model(self, func: Callable, tool_name: str) -> type[BaseModel]:
        """
        根据函数签名创建Pydantic请求模型
        
        Args:
            func: 工具函数
            tool_name: 工具名称
            
        Returns:
            Pydantic模型类
        """
        sig = inspect.signature(func)
        type_hints = get_type_hints(func)
        
        fields = {}
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
                
            # 获取类型注解
            param_type = type_hints.get(param_name, Any)
            
            # 获取默认值
            if param.default == inspect.Parameter.empty:
                # 必填参数
                fields[param_name] = (param_type, ...)
            else:
                # 可选参数
                fields[param_name] = (param_type, param.default)
        
        # 动态创建模型
        model_name = f"{tool_name.title().replace('_', '')}Request"
        return create_model(model_name, **fields)
    
    def _create_response_model(self, tool_name: str) -> type[BaseModel]:
        """
        创建统一的响应模型
        
        Args:
            tool_name: 工具名称
            
        Returns:
            Pydantic响应模型类
        """
        model_name = f"{tool_name.title().replace('_', '')}Response"
        return create_model(
            model_name,
            message=(str, "success"),
            error=(str, ""),
            data=(Any, ...)
        )
    
    def _create_endpoint_handler(self, tool_func: Callable, request_model: type[BaseModel]):
        """
        创建FastAPI端点处理函数
        
        Args:
            tool_func: MCP工具函数
            request_model: 请求模型
            
        Returns:
            异步处理函数
        """
        async def handler(request: request_model):
            try:
                # 将请求模型转换为字典
                params = request.model_dump()
                
                # 调用MCP工具函数
                if inspect.iscoroutinefunction(tool_func):
                    result = await tool_func(**params)
                else:
                    result = tool_func(**params)
                
                # 返回统一格式
                return {
                    "message": "success",
                    "error": "",
                    "data": result
                }
            except Exception as e:
                logger.error(f"Error calling tool {tool_func.__name__}: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))
        
        return handler
    
    def register_tools(self, tags: Optional[List[str]] = None) -> APIRouter:
        """
        将MCP服务器中的所有工具注册为FastAPI端点
        
        Args:
            tags: FastAPI标签列表
            
        Returns:
            配置好的APIRouter
        """
        if tags is None:
            tags = [self.mcp_server.name]
        
        # 获取MCP服务器中注册的所有工具
        tools = self.mcp_server._tool_manager._tools
        
        for tool_name, tool_info in tools.items():
            tool_func = tool_info.fn
            
            # 创建请求和响应模型
            request_model = self._create_request_model(tool_func, tool_name)
            
            # 创建端点处理函数
            handler = self._create_endpoint_handler(tool_func, request_model)
            
            # 构建端点路径
            endpoint_path = f"{self.prefix}/{tool_name}"
            
            # 获取工具描述
            description = tool_func.__doc__ or f"Call {tool_name} tool"
            
            # 注册到路由器
            self.router.post(
                endpoint_path,
                tags=tags,
                summary=tool_name,
                description=description,
                operation_id=tool_name,
                response_model=None  # 使用动态响应
            )(handler)
            
            # logger.info(f"Registered FastAPI endpoint: POST {endpoint_path}")
        
        return self.router


def create_mcp_fastapi_router(
    mcp_server: FastMCP,
    prefix: str = "",
    tags: Optional[List[str]] = None
) -> APIRouter:
    """
    便捷函数：创建MCP到FastAPI的路由器
    
    Args:
        mcp_server: FastMCP服务器实例
        prefix: API路径前缀
        tags: FastAPI标签列表
        
    Returns:
        配置好的APIRouter
        
    Example:
        >>> from tools.chembl.server import mcp as chembl_mcp
        >>> router = create_mcp_fastapi_router(
        ...     chembl_mcp,
        ...     prefix="/chembl",
        ...     tags=["ChEMBL"]
        ... )
        >>> app.include_router(router)
    """
    adapter = MCPToolAdapter(mcp_server, prefix)
    return adapter.register_tools(tags)
