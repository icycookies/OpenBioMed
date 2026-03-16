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


# Import MCP tool registry
from registry import setup_mcp_tools, registry

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Disable INFO logs from third-party libraries
logging.getLogger('numexpr').setLevel(logging.WARNING)
logging.getLogger('fastapi_mcp').setLevel(logging.WARNING)
logging.getLogger('fastapi_mcp.server').setLevel(logging.WARNING)

# ============================================================================
# Create FastAPI application
# ============================================================================
app = FastAPI(
    title="Pharmolix Tools with MCP Integration",
    description="This project integrates external MCP tool services for OpenBioMed",
    version="0.2.0",
)

# ============================================================================
# Register MCP tools as FastAPI endpoints
# ============================================================================
setup_mcp_tools()

# Register all MCP tools to the app
# All tool endpoints will be under the /tools prefix
registry.register_to_app(app, base_prefix="/tools")

# Add tools summary endpoint
@app.get("/tools/summary", tags=["Tool Management"])
def get_tools_summary():
    """Get summary information of all registered MCP tools"""
    return registry.get_tools_summary()

# ============================================================================
# MCP serving (convert existing FastAPI to MCP SSE endpoints)
# ============================================================================
mcp = FastApiMCP(
    app,
    name="Pharmolix API MCP",
    description="MCP server for Pharmolix existing API",
)
mcp.mount()

# ============================================================================
# Per-module MCP endpoints
# ============================================================================
for config in registry.tool_configs:
    try:
        # Create an independent sub FastAPI app for each module, containing only that module's routes
        sub_app = FastAPI(title=config.get("description", ""))
        
        # Register the module's tool endpoints to the sub-app
        sub_router = create_mcp_fastapi_router(
            mcp_server=config["mcp_server"],
            prefix=config["prefix"],
            tags=config["tags"]
        )
        sub_app.include_router(sub_router)
        
        # Create FastApiMCP from the sub-app and mount to the main app
        module_mcp = FastApiMCP(
            sub_app,
            name=config.get("description", config["prefix"]),
        )
        # Mount path example: /chembl/mcp, /biocomputing_literature/mcp
        module_mcp.mount(app, mount_path=f"{config['prefix']}/mcp")
        
        logger.info(f"Mounted MCP endpoint at {config['prefix']}/mcp")
    except Exception as e:
        logger.warning(f"Failed to mount MCP for {config['prefix']}: {e}")


# ============================================================================
# Health check endpoint
# ============================================================================
@app.get("/healthz")
def ping():
    return {
        "status": "healthy",
        "service": "Pharmolix Tools",
        "mcp_tools_count": len(registry.mcp_servers)
    }

# ============================================================================
# Exception handling
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
# Startup information
# ============================================================================
@app.on_event("startup")
async def startup_event():
    logger.info("=" * 60)
    logger.info("Pharmolix Tools API Started")
    logger.info(f"Registered {len(registry.mcp_servers)} MCP tool servers")
    logger.info("=" * 60)
    
    # Print all registered tools
    summary = registry.get_tools_summary()
    for server in summary["servers"]:
        logger.info(f"  - {server['name']}: {server['tool_count']} tools at {server['prefix']}")
