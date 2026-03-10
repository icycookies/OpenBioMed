"""
MCP SSE Client for fastapi-mcp servers
支持 fastapi-mcp 的 SSE 协议
"""

import httpx
from typing import Dict, List, Any, Tuple


class FastAPIMCPClient:
    """fastapi-mcp SSE 客户端"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.tools_cache = None
        
        # 从 URL 中提取服务器前缀和基础 URL
        # 例如: http://localhost:8086/ncbi/mcp -> server_prefix=ncbi, api_base=http://localhost:8086
        # 或: http://localhost:8086/ncbi -> server_prefix=ncbi, api_base=http://localhost:8086
        parts = self.base_url.split('/')
        if len(parts) >= 4:
            # 找到服务器前缀（ncbi, pubchem 等）
            self.server_prefix = parts[-2] if parts[-1] == 'mcp' else parts[-1]
            # 构造 API 基础 URL
            self.api_base = '/'.join(parts[:3])  # http://localhost:8086
        else:
            raise ValueError(f"Invalid base_url format: {base_url}")
        
    async def start(self):
        """启动客户端"""
        pass
        
    async def stop(self):
        """停止客户端"""
        pass
        
    async def list_tools(self) -> List[Dict[str, Any]]:
        """列出所有工具"""
        if self.tools_cache is not None:
            return self.tools_cache
            
        async with httpx.AsyncClient(timeout=30.0) as client:
            # 首先从 summary 获取工具名称列表
            response = await client.get(f"{self.api_base}/tools/summary")
            response.raise_for_status()
            result = response.json()
            
            # 找到对应的服务器
            tools = []
            
            for server in result.get("servers", []):
                if server["prefix"] == f"/{self.server_prefix}":
                    tool_names = server["tools"]
                    
                    # 对于每个工具，尝试获取其 OpenAPI schema
                    # FastAPI 会自动生成 /openapi.json
                    try:
                        openapi_response = await client.get(f"{self.api_base}/openapi.json")
                        if openapi_response.status_code == 200:
                            openapi_spec = openapi_response.json()
                            paths = openapi_spec.get("paths", {})
                            components = openapi_spec.get("components", {})
                            schemas = components.get("schemas", {})
                            
                            # 为每个工具构建 schema
                            for tool_name in tool_names:
                                tool_path = f"/tools/{self.server_prefix}/{tool_name}"
                                if tool_path in paths:
                                    path_info = paths[tool_path]
                                    post_info = path_info.get("post", {})
                                    
                                    # 提取描述和参数
                                    # 优先使用 description（包含完整 docstring），其次是 summary
                                    description = post_info.get("description", "") or post_info.get("summary", "") or f"{self.server_prefix} tool: {tool_name}"
                                    
                                    # 提取输入 schema
                                    request_body = post_info.get("requestBody", {})
                                    content = request_body.get("content", {})
                                    json_content = content.get("application/json", {})
                                    input_schema = json_content.get("schema", {"type": "object", "properties": {}})
                                    
                                    # 解析 $ref 引用
                                    if "$ref" in input_schema:
                                        ref_path = input_schema["$ref"]
                                        # 格式: #/components/schemas/SchemaName
                                        if ref_path.startswith("#/components/schemas/"):
                                            schema_name = ref_path.split("/")[-1]
                                            if schema_name in schemas:
                                                input_schema = schemas[schema_name]
                                    
                                    tools.append({
                                        "name": tool_name,
                                        "description": description,
                                        "inputSchema": input_schema
                                    })
                                else:
                                    # 如果没有找到 OpenAPI 定义，使用默认值
                                    tools.append({
                                        "name": tool_name,
                                        "description": f"{self.server_prefix} tool: {tool_name}",
                                        "inputSchema": {"type": "object", "properties": {}}
                                    })
                    except Exception as e:
                        # 如果获取 OpenAPI spec 失败，使用默认值
                        for tool_name in tool_names:
                            tools.append({
                                "name": tool_name,
                                "description": f"{self.server_prefix} tool: {tool_name}",
                                "inputSchema": {"type": "object", "properties": {}}
                            })
                    break
            
            self.tools_cache = tools
            return tools
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Tuple[Any, str]:
        """调用工具"""
        async with httpx.AsyncClient(timeout=60.0) as client:
            # 构造 URL: http://localhost:8086/tools/ncbi/tool_name
            url = f"{self.api_base}/tools/{self.server_prefix}/{tool_name}"
            
            response = await client.post(url, json=arguments)
            response.raise_for_status()
            result = response.json()
            
            # 提取结果
            if "data" in result:
                return result["data"], result.get("message", "success")
            else:
                return result, "success"


def create_mcp_client(config: Dict[str, Any]):
    """根据配置创建合适的 MCP 客户端"""
    if "url" in config:
        return FastAPIMCPClient(config["url"])
    else:
        raise ValueError("Unsupported MCP client configuration")
