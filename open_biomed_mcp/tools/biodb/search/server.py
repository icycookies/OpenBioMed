
from asyncio import to_thread
import os
from dotenv import load_dotenv

from mcp.server.fastmcp import FastMCP

from tools.biodb.search.tavily_search import TavilySearchEngine
from tools.biodb.search.jina_search import JinaSearchEngine

# 加载环境变量
load_dotenv()

# 从环境变量获取配置
conf = {
    "tavily_api_key": os.getenv("tavily_api_key", ""),
    "jina_api_key": os.getenv("jina_api_key", "")
}


mcp = FastMCP(
    "search_mcp",
    stateless_http=True,
)


tavily_api = TavilySearchEngine(conf["tavily_api_key"])
jina_api = JinaSearchEngine(conf["jina_api_key"])


@mcp.tool()
async def tavily_search(query: str):
    """使用给定的查询运行搜索引擎，检索并过滤结果。
    """
    if not conf["tavily_api_key"]:
        return "Tavily API key is not set in the configuration."
    
    try:
        results = await to_thread(tavily_api.run, query)
    except Exception as e:
        results = f"Tool tavily_search execution failed for query: {query}, error: {e}"
    return results


@mcp.tool()
async def jina_search(query: str):
    """使用给定的查询运行 Jina DeepSearch 引擎，检索并过滤结果。
    """
    if not conf["jina_api_key"]:
        return "Jina API key is not set in the configuration."
    
    try:
        results = await to_thread(jina_api.run, query)
    except Exception as e:
        results = f"Tool jina_search execution failed for query: {query}, error: {e}"
    return results