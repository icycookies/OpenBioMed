"""
MCP SSE Client for fastapi-mcp servers
Supports the SSE protocol of fastapi-mcp
"""

import httpx
from typing import Dict, List, Any, Tuple


class FastAPIMCPClient:
    """fastapi-mcp SSE client"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.tools_cache = None
        
        # Extract the server prefix and base URL from the URL
        # e.g.: http://localhost:8086/ncbi/mcp -> server_prefix=ncbi, api_base=http://localhost:8086
        # or:   http://localhost:8086/ncbi     -> server_prefix=ncbi, api_base=http://localhost:8086
        parts = self.base_url.split('/')
        if len(parts) >= 4:
            # Find the server prefix (ncbi, pubchem, etc.)
            self.server_prefix = parts[-2] if parts[-1] == 'mcp' else parts[-1]
            # Build the API base URL
            self.api_base = '/'.join(parts[:3])  # http://localhost:8086
        else:
            raise ValueError(f"Invalid base_url format: {base_url}")
        
    async def start(self):
        """Start the client"""
        pass
        
    async def stop(self):
        """Stop the client"""
        pass
        
    async def list_tools(self) -> List[Dict[str, Any]]:
        """List all tools"""
        if self.tools_cache is not None:
            return self.tools_cache
            
        async with httpx.AsyncClient(timeout=30.0) as client:
            # First get the list of tool names from summary
            response = await client.get(f"{self.api_base}/tools/summary")
            response.raise_for_status()
            result = response.json()
            
            # Find the corresponding server
            tools = []
            
            for server in result.get("servers", []):
                if server["prefix"] == f"/{self.server_prefix}":
                    tool_names = server["tools"]
                    
                    # For each tool, try to get its OpenAPI schema
                    # FastAPI auto-generates /openapi.json
                    try:
                        openapi_response = await client.get(f"{self.api_base}/openapi.json")
                        if openapi_response.status_code == 200:
                            openapi_spec = openapi_response.json()
                            paths = openapi_spec.get("paths", {})
                            components = openapi_spec.get("components", {})
                            schemas = components.get("schemas", {})
                            
                            # Build schema for each tool
                            for tool_name in tool_names:
                                tool_path = f"/tools/{self.server_prefix}/{tool_name}"
                                if tool_path in paths:
                                    path_info = paths[tool_path]
                                    post_info = path_info.get("post", {})
                                    
                                    # Extract description and parameters
                                    # Prefer description (full docstring) over summary
                                    description = post_info.get("description", "") or post_info.get("summary", "") or f"{self.server_prefix} tool: {tool_name}"
                                    
                                    # Extract input schema
                                    request_body = post_info.get("requestBody", {})
                                    content = request_body.get("content", {})
                                    json_content = content.get("application/json", {})
                                    input_schema = json_content.get("schema", {"type": "object", "properties": {}})
                                    
                                    # Resolve $ref references
                                    if "$ref" in input_schema:
                                        ref_path = input_schema["$ref"]
                                        # Format: #/components/schemas/SchemaName
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
                                    # If no OpenAPI definition found, use defaults
                                    tools.append({
                                        "name": tool_name,
                                        "description": f"{self.server_prefix} tool: {tool_name}",
                                        "inputSchema": {"type": "object", "properties": {}}
                                    })
                    except Exception as e:
                        # If fetching the OpenAPI spec fails, use defaults
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
        """Call a tool"""
        async with httpx.AsyncClient(timeout=60.0) as client:
            # Build URL: http://localhost:8086/tools/ncbi/tool_name
            url = f"{self.api_base}/tools/{self.server_prefix}/{tool_name}"
            
            response = await client.post(url, json=arguments)
            response.raise_for_status()
            result = response.json()
            
            # Extract result
            if "data" in result:
                return result["data"], result.get("message", "success")
            else:
                return result, "success"


def create_mcp_client(config: Dict[str, Any]):
    """Create the appropriate MCP client based on configuration"""
    if "url" in config:
        return FastAPIMCPClient(config["url"])
    else:
        raise ValueError("Unsupported MCP client configuration")
