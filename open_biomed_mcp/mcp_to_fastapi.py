"""
MCP to FastAPI Adapter
Converts MCP services to FastAPI endpoints, enabling them to serve as both MCP services and REST APIs
"""

import inspect
import logging
from typing import Any, Callable, Dict, List, Optional, get_type_hints
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, create_model
from mcp.server.fastmcp import FastMCP

logger = logging.getLogger(__name__)


class MCPToolAdapter:
    """Adapts MCP tools as FastAPI endpoints"""
    
    def __init__(self, mcp_server: FastMCP, prefix: str = ""):
        """
        Initialize the adapter
        
        Args:
            mcp_server: FastMCP server instance
            prefix: API path prefix, e.g. "/chembl"
        """
        self.mcp_server = mcp_server
        self.prefix = prefix.rstrip("/")
        self.router = APIRouter()
        
    def _create_request_model(self, func: Callable, tool_name: str) -> type[BaseModel]:
        """
        Create a Pydantic request model from a function signature
        
        Args:
            func: Tool function
            tool_name: Tool name
            
        Returns:
            Pydantic model class
        """
        sig = inspect.signature(func)
        type_hints = get_type_hints(func)
        
        fields = {}
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
                
            # Get type annotation
            param_type = type_hints.get(param_name, Any)
            
            # Get default value
            if param.default == inspect.Parameter.empty:
                # Required parameter
                fields[param_name] = (param_type, ...)
            else:
                # Optional parameter
                fields[param_name] = (param_type, param.default)
        
        # Dynamically create model
        model_name = f"{tool_name.title().replace('_', '')}Request"
        return create_model(model_name, **fields)
    
    def _create_response_model(self, tool_name: str) -> type[BaseModel]:
        """
        Create a unified response model
        
        Args:
            tool_name: Tool name
            
        Returns:
            Pydantic response model class
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
        Create a FastAPI endpoint handler function
        
        Args:
            tool_func: MCP tool function
            request_model: Request model
            
        Returns:
            Async handler function
        """
        async def handler(request: request_model):
            try:
                # Convert request model to dict
                params = request.model_dump()
                
                # Call the MCP tool function
                if inspect.iscoroutinefunction(tool_func):
                    result = await tool_func(**params)
                else:
                    result = tool_func(**params)
                
                # Return unified format
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
        Register all tools from the MCP server as FastAPI endpoints
        
        Args:
            tags: FastAPI tag list
            
        Returns:
            Configured APIRouter
        """
        if tags is None:
            tags = [self.mcp_server.name]
        
        # Get all tools registered in the MCP server
        tools = self.mcp_server._tool_manager._tools
        
        for tool_name, tool_info in tools.items():
            tool_func = tool_info.fn
            
            # Create request and response models
            request_model = self._create_request_model(tool_func, tool_name)
            
            # Create endpoint handler
            handler = self._create_endpoint_handler(tool_func, request_model)
            
            # Build endpoint path
            endpoint_path = f"{self.prefix}/{tool_name}"
            
            # Get tool description
            description = tool_func.__doc__ or f"Call {tool_name} tool"
            
            # Register to router
            self.router.post(
                endpoint_path,
                tags=tags,
                summary=tool_name,
                description=description,
                operation_id=tool_name,
                response_model=None  # Use dynamic response
            )(handler)
            
            # logger.info(f"Registered FastAPI endpoint: POST {endpoint_path}")
        
        return self.router


def create_mcp_fastapi_router(
    mcp_server: FastMCP,
    prefix: str = "",
    tags: Optional[List[str]] = None
) -> APIRouter:
    """
    Convenience function: create a router from MCP to FastAPI
    
    Args:
        mcp_server: FastMCP server instance
        prefix: API path prefix
        tags: FastAPI tag list
        
    Returns:
        Configured APIRouter
        
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
