"""
MCP Tool Wrappers for OpenBioMed
Adapts MCP tools to OpenBioMed's tool interface
"""

import asyncio
from typing import Any, Dict, List, Tuple
from open_biomed.tools.base_tool import Tool
from open_biomed.tools.mcp_client_sse import create_mcp_client


class MCPToolWrapper(Tool):
    """Wrapper that adapts an MCP tool to OpenBioMed's tool interface"""
    
    def __init__(self, server_name: str, tool_name: str, tool_schema: Dict[str, Any]):
        """
        Initialize MCP tool wrapper
        
        Args:
            server_name: Name of the MCP server
            tool_name: Name of the tool on the server
            tool_schema: Tool schema from MCP server (includes description, inputSchema)
        """
        super().__init__()
        self.server_name = server_name
        self.tool_name = tool_name
        self.tool_schema = tool_schema
        
    def print_usage(self) -> str:
        """Generate usage documentation from MCP tool schema"""
        description = self.tool_schema.get("description", "No description available")
        input_schema = self.tool_schema.get("inputSchema", {})
        
        # Extract input parameters
        properties = input_schema.get("properties", {})
        required = input_schema.get("required", [])
        
        usage_lines = [
            f"{self.tool_name} (MCP Tool)",
            f"Description: {description}",
            "",
            "Inputs:",
        ]
        
        if properties:
            for param_name, param_info in properties.items():
                param_type = param_info.get("type", "any")
                param_desc = param_info.get("description", "")
                is_required = " (required)" if param_name in required else " (optional)"
                usage_lines.append(f"  - {param_name}: {param_type}{is_required} - {param_desc}")
        else:
            usage_lines.append("  No parameters required")
        
        usage_lines.extend([
            "",
            "Outputs: Result from MCP tool execution",
            "",
            "Example usage:",
            f"<execute>",
            f"from open_biomed.tools.tool_registry import TOOLS",
            f"tool = TOOLS['{self.tool_name}']",
            f"result, message = tool.run({', '.join([f'{p}=...' for p in list(properties.keys())[:2]])})",
            f"print(result)",
            f"</execute>",
        ])
        
        return "\n".join(usage_lines)
    
    def run(self, **kwargs) -> Tuple[List[Any], List[str]]:
        """
        Execute the MCP tool
        
        Args:
            **kwargs: Arguments to pass to the MCP tool
            
        Returns:
            Tuple of (results_list, messages_list)
        """
        # Run async call in sync context
        import threading
        
        # 检查是否在主线程
        is_main_thread = threading.current_thread() is threading.main_thread()
        
        try:
            # 尝试获取当前事件循环
            try:
                loop = asyncio.get_running_loop()
                # 如果已经在运行的循环中，使用 nest_asyncio
                import nest_asyncio
                nest_asyncio.apply()
                result, message = loop.run_until_complete(self._async_run(kwargs))
            except RuntimeError:
                # 没有运行中的循环，创建新的
                result, message = asyncio.run(self._async_run(kwargs))
        except Exception as e:
            # 如果上述方法都失败，尝试在新线程中运行
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, self._async_run(kwargs))
                result, message = future.result(timeout=60)
        
        # Return in OpenBioMed format: (list of results, list of messages)
        return [result], [message]
    
    async def _async_run(self, arguments: Dict[str, Any]) -> Tuple[Any, str]:
        """Async implementation of tool execution"""
        # 使用新的客户端
        from open_biomed.tools.mcp_client_sse import create_mcp_client
        
        # 重新创建客户端（简化版本，实际应该缓存）
        import json
        import os
        
        config_path = ".kiro/settings/mcp.json"
        if not os.path.exists(config_path):
            config_path = os.path.expanduser("~/.kiro/settings/mcp.json")
        
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        server_config = config["mcpServers"][self.server_name]
        client = create_mcp_client(server_config)
        
        return await client.call_tool(self.tool_name, arguments)


def load_mcp_tools_from_config(config_path: str = None) -> Dict[str, MCPToolWrapper]:
    """
    Load MCP tools from configuration file
    
    Args:
        config_path: Path to MCP configuration file (JSON format)
                    If None, looks for .kiro/settings/mcp.json
    
    Returns:
        Dictionary mapping tool names to MCPToolWrapper instances
    """
    import json
    import os
    
    if config_path is None:
        # Try workspace config first, then user config
        workspace_config = ".kiro/settings/mcp.json"
        user_config = os.path.expanduser("~/.kiro/settings/mcp.json")
        
        if os.path.exists(workspace_config):
            config_path = workspace_config
        elif os.path.exists(user_config):
            config_path = user_config
        else:
            print("Warning: No MCP configuration file found")
            return {}
    
    # Load configuration
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    mcp_servers = config.get("mcpServers", {})
    
    # 使用新的客户端加载工具
    all_tools = {}
    
    async def load_all_tools():
        for server_name, server_config in mcp_servers.items():
            if server_config.get("disabled", False):
                continue
            
            try:
                client = create_mcp_client(server_config)
                await client.start()
                tools = await client.list_tools()
                all_tools[server_name] = tools
                print(f"✓ Loaded {len(tools)} tools from {server_name}")
            except Exception as e:
                print(f"Warning: Failed to load tools from {server_name}: {e}")
                all_tools[server_name] = []
        
        return all_tools
    
    # 运行加载
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import nest_asyncio
            nest_asyncio.apply()
            all_tools = loop.run_until_complete(load_all_tools())
        else:
            all_tools = loop.run_until_complete(load_all_tools())
    except RuntimeError:
        # No event loop, create new one
        all_tools = asyncio.run(load_all_tools())
    except Exception as e:
        print(f"Error loading MCP tools: {e}")
        import traceback
        traceback.print_exc()
        return {}
    
    # Create tool wrappers
    tool_wrappers = {}
    for server_name, tools in all_tools.items():
        for tool_schema in tools:
            tool_name = tool_schema["name"]

            wrapper_name = tool_name
            
            tool_wrappers[wrapper_name] = MCPToolWrapper(
                server_name=server_name,
                tool_name=tool_name,
                tool_schema=tool_schema
            )
    
    return tool_wrappers



class MCPToolRegistry:
    """Registry for dynamically loaded MCP tools"""
    
    def __init__(self):
        self._tools = None
        self._loaded = False
    
    def load(self, config_path: str = None):
        """Load MCP tools from configuration"""
        if not self._loaded:
            self._tools = load_mcp_tools_from_config(config_path)
            self._loaded = True
    
    def get_tools(self) -> Dict[str, MCPToolWrapper]:
        """Get all loaded MCP tools"""
        if not self._loaded:
            self.load()
        return self._tools or {}
    
    def available_tools(self) -> List[str]:
        """Get list of available MCP tool names"""
        return list(self.get_tools().keys())


# Global MCP tool registry
_mcp_tool_registry = MCPToolRegistry()


def get_mcp_tool_registry() -> MCPToolRegistry:
    """Get the global MCP tool registry"""
    return _mcp_tool_registry
