from typing import Optional
from asyncio import to_thread
from mcp.server.fastmcp import FastMCP

from tools.biodb.clinicaltrials.clinicaltrials_api import ClinicalTrialsAPI


mcp = FastMCP(
    name="clinicaltrials_mcp",
    stateless_http=True,
)
clinicaltrials_api = ClinicalTrialsAPI()


@mcp.tool()
async def get_studies(
    query: Optional[dict] = None,
    filter: Optional[dict] = None,
    post_filter: Optional[dict] = None,
    fields: Optional[list] = None,
    sort: Optional[list] = None,
    page_size: int = 50,
    page_token: Optional[str] = None,
    format: str = "json",
    markup_format: str = "markdown",
    count_total: bool = False
):
    """
    在 ClinicalTrials.gov 上使用结构化查询参数搜索临床试验。
    支持使用 query、filter 和 post_filter 参数的复杂查询。
    返回分页结果，可选包含总计数。
    
    Args:
        query: query.* 字段的参数（例如 {"cond": "cancer"}）
        filter: filter.* 字段的参数（例如 {"status": "RECRUITING"}）
        post_filter: postFilter.* 字段的参数
        fields: 要返回的字段列表（例如 ["NCTId", "BriefTitle"]）
        sort: 排序字段（例如 ["@relevance", "EnrollmentCount:desc"]）
        page_size: 每页结果数量（最大 1000）
        page_token: 下一页的令牌
        format: 响应格式（"json" 或 "csv"）
        markup_format: 文本格式（"markdown" 或 "legacy"）
        count_total: 是否包含总计数
        
    Returns:
        包含以下内容的字典：
        - studies: 匹配的研究列表
        - next_page_token: 下一页的令牌（如果可用）
        - total_count: 研究总数（如果 count_total=True）
    
    Query example:  
        {'query': {'cond': 'cancer'}, 'filter': {'status': 'RECRUITING'}}
        {'query': {'cond': 'lung cancer'}, 'fields': ['NCTId', 'BriefTitle']}
        
    """
    result = await to_thread(clinicaltrials_api.get_studies,
        query=query,
        filter=filter,
        post_filter=post_filter,
        fields=fields,
        sort=sort,
        page_size=page_size,
        page_token=page_token,
        format=format,
        markup_format=markup_format,
        count_total=count_total
    )
    return {
        "studies": result.get("studies", []),
        "next_page_token": result.get("nextPageToken"),
        "total_count": result.get("totalCount")
    }

@mcp.tool()
async def get_study(
    nct_id: str,
    format: str = "json",
    markup_format: str = "markdown",
    fields: Optional[list] = None
):
    """
    获取单个临床试验的详细信息。
    
    Args:
        nct_id: NCT ID（例如 "NCT000001"）
        format: 响应格式（"json"、"csv" 等）
        markup_format: 文本格式（"markdown" 或 "legacy"）
        fields: 要包含的字段列表
        
    Returns:
        包含研究详细信息的字典
    
    Query example: {"nct_id": "NCT000001"}
    """
    return await to_thread(clinicaltrials_api.get_study,
        nct_id=nct_id,
        format=format,
        markup_format=markup_format,
        fields=fields
    )

@mcp.tool()
async def get_metadata(
    include_indexed_only: bool = False,
    include_historic_only: bool = False
):
    """
    获取有关可用研究字段的元数据。
    
    Args:
        include_indexed_only: 包含仅索引字段
        include_historic_only: 包含仅历史字段
        
    Returns:
        字段元数据字典
    """
    return await to_thread(clinicaltrials_api.get_metadata,
        include_indexed_only=include_indexed_only,
        include_historic_only=include_historic_only
    )

@mcp.tool()
async def get_search_areas():
    """
    获取可用的搜索文档和区域。
    
    Returns:
        搜索区域字典
    """
    return await to_thread(clinicaltrials_api.get_search_areas)

@mcp.tool()
async def get_enums():
    """
    获取枚举类型和值。
    
    Returns:
        枚举类型和值的字典
    """
    return await to_thread(clinicaltrials_api.get_enums)

@mcp.tool()
async def get_study_size_stats():
    """
    获取有关研究记录大小的统计信息。
    
    Returns:
        大小统计信息字典
    """
    return await to_thread(clinicaltrials_api.get_study_size_stats)

@mcp.tool()
async def get_field_value_stats(fields: list[str], types: Optional[list[str]] = None):
    """
    获取字段的值统计信息。
    
    Args:
        fields: 字段名称列表
        types: 按数据类型过滤（ENUM、STRING 等）
        
    Returns:
        字段值统计信息字典
    """
    return await to_thread(clinicaltrials_api.get_field_value_stats,
        fields=fields,
        types=types
    )

@mcp.tool()
async def get_field_size_stats(fields: Optional[list[str]] = None):
    """
    获取列表/数组字段的大小统计信息。
    
    Args:
        fields: 要过滤的字段名称列表
        
    Returns:
        字段大小统计信息字典
    """
    return await to_thread(clinicaltrials_api.get_field_size_stats,
        fields=fields
    )

@mcp.prompt()
def system_prompt():
    return """您是 ClinicalTrials.gov MCP 服务器。
    您可以使用 ClinicalTrials.gov API 回答有关临床试验的问题。
    始终在最终答案中包含工具调用的结果。"""

