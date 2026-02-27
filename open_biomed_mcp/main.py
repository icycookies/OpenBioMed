import logging
from pathlib import Path
from dotenv import load_dotenv
from mcp_to_fastapi import create_mcp_fastapi_router

env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(env_path)

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi_mcp import FastApiMCP


# 导入MCP工具注册中心
from registry import setup_mcp_tools, registry

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 禁用第三方库的 INFO 日志
logging.getLogger('numexpr').setLevel(logging.WARNING)
logging.getLogger('fastapi_mcp').setLevel(logging.WARNING)
logging.getLogger('fastapi_mcp.server').setLevel(logging.WARNING)

# ============================================================================
# 创建FastAPI应用
# ============================================================================
app = FastAPI(
    title="Pharmolix Tools with MCP Integration",
    description="本项目为OpenBioMed集成外部MCP工具服务",
    version="0.2.0",
)

# ============================================================================
# 注册MCP工具为FastAPI端点
# ============================================================================
setup_mcp_tools()

# 将所有MCP工具注册到应用
# 所有工具端点将在 /tools 前缀下
registry.register_to_app(app, base_prefix="/tools")

# 添加工具摘要端点
@app.get("/tools/summary", tags=["工具管理"])
def get_tools_summary():
    """获取所有已注册MCP工具的摘要信息"""
    return registry.get_tools_summary()

# ============================================================================
# MCP服务化（将现有FastAPI转为MCP SSE端点）
# ============================================================================
mcp = FastApiMCP(
    app,
    name="Pharmolix API MCP",
    description="MCP server for Pharmolix existing API",
)
mcp.mount()

# ============================================================================
# 按模块拆分的 MCP 端点
# ============================================================================
for config in registry.tool_configs:
    try:
        # 为每个模块创建一个独立的子 FastAPI 应用，只包含该模块的路由
        sub_app = FastAPI(title=config.get("description", ""))
        
        # 把该模块的工具端点注册到子应用
        sub_router = create_mcp_fastapi_router(
            mcp_server=config["mcp_server"],
            prefix=config["prefix"],
            tags=config["tags"]
        )
        sub_app.include_router(sub_router)
        
        # 基于子应用创建 FastApiMCP 并挂载到主应用
        module_mcp = FastApiMCP(
            sub_app,
            name=config.get("description", config["prefix"]),
        )
        # 挂载路径示例: /chembl/mcp, /biocomputing_literature/mcp
        module_mcp.mount(app, mount_path=f"{config['prefix']}/mcp")
        
        logger.info(f"Mounted MCP endpoint at {config['prefix']}/mcp")
    except Exception as e:
        logger.warning(f"Failed to mount MCP for {config['prefix']}: {e}")


# ============================================================================
# 健康检查端点
# ============================================================================
@app.get("/healthz")
def ping():
    return {
        "status": "healthy",
        "service": "Pharmolix Tools",
        "mcp_tools_count": len(registry.mcp_servers)
    }

# ============================================================================
# 异常处理
# ============================================================================
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f"{exc}".replace("\n", " ").replace("   ", " ")
    logging.error(f"{request}: {exc_str}")
    content = {"status_code": 422, "message": exc_str}
    return JSONResponse(
        content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )

# ============================================================================
# 启动信息
# ============================================================================
@app.on_event("startup")
async def startup_event():
    logger.info("=" * 60)
    logger.info("Pharmolix Tools API Started")
    logger.info(f"Registered {len(registry.mcp_servers)} MCP tool servers")
    logger.info("=" * 60)
    
    # 打印所有注册的工具
    summary = registry.get_tools_summary()
    for server in summary["servers"]:
        logger.info(f"  - {server['name']}: {server['tool_count']} tools at {server['prefix']}")
