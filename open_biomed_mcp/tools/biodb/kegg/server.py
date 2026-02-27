
from mcp.server.fastmcp import FastMCP

from tools.biodb.kegg.kegg_api import KeggAPI

mcp = FastMCP(
    "kegg_mcp",
    stateless_http=True,
)
kegg_api = KeggAPI()


@mcp.tool()
async def kegg_info(db: str):
    """此操作显示数据库发布信息及数据库统计信息。
    除了 kegg、genes 和 ligand 之外，此操作还显示可在 link 操作中使用的链接数据库列表。
    显示给定数据库的当前统计信息。

    Args:
        db: kegg 数据库（字符串）

    Query example: {"db": "genes"}

    Returns:
        文本消息
    """
    try:
        result = kegg_api.kegg_info(database=db)
    except Exception as e:
        return [{"error": f"An error occurred while querying kegg_info: {str(e)}"}]
    return result


@mcp.tool()
async def kegg_find(db: str, query: str, option: str = ''):
    """KEGG find - 数据搜索。在给定数据库中查找与查询关键字或其他查询数据匹配的条目。

    Args:
        db: KEGG 数据库（字符串）
        query: 要搜索的关键字或标识符（字符串）
        option: 附加搜索选项（字符串）

    Query example: {"db": "genes", "query": "p53", "option": ""}
    
    Returns:
        制表符分隔的文本
    """
    try:
        result = kegg_api.kegg_find(database=db, query=query, option=option)
    except Exception as e:
        return {"error": f"An error occurred while querying kegg_find: {str(e)}"}
    return result


@mcp.tool()
async def kegg_list(db: str, org: str = ''):
    """此操作可用于获取每个数据库中所有条目的列表。当已知生物体代码时，可以使用第二种形式获取特定生物体的通路列表。第三种形式是 brite 层次结构的类似选项。第四种形式可用于获取给定数据库条目标识符集的定义列表。可以给出的最大标识符数量为 10。

    Args:
        db: kegg 数据库（字符串）
        org: 可选参数，用于指定生物体前缀。仅当 db 为某些类型时有效（字符串）

    Query example: {"db": "pathway", "org": ""}

    Returns:
        制表符分隔的文本
    """
    try:
        result = kegg_api.kegg_list(database=db, org=org)
    except Exception as e:
        return {"error": f"An error occurred while querying kegg_list: {str(e)}"}
    return result


@mcp.tool()
async def kegg_get(dbentries: str, option: str):
    """此操作以平面文件格式或带选项的其他格式检索给定的数据库条目。平面文件格式适用于除 brite 之外的所有 KEGG 数据库。输入限制为最多 10 个条目。

    Args:
        dbentries: 指定要查询的 KEGG 条目标识符或列表。多个条目用 + 分隔（字符串）
        option: 控制返回数据的格式或内容（字符串）

    Query example: {"dbentries": "path:hsa00010", "option": "kgml"}

    Returns:
        平面文件数据库格式
    """
    try:
        result = kegg_api.kegg_get(dbentries=dbentries, option=option)
    except Exception as e:
        return {"error": f"An error occurred while querying kegg_get: {str(e)}"}
    return result


@mcp.tool()
async def kegg_conv(target_db: str, source_db_or_dbentries: str, option: str):
    """此操作可用于将外部数据库的条目标识符（登录号）转换为 KEGG 标识符，反之亦然。第一种形式允许数据库到数据库的映射，而第二种形式允许转换选定数量的条目。数据库名称 "genes" 只能在第二种形式中使用。

    Args:
        target_db: 目标数据库（字符串）
        source_db_or_dbentries: 源数据库或数据库条目（字符串）
        option: 选项（字符串）

    Query example: {"target_db": "ncbi-geneid", "source_db_or_dbentries": "hsa:10458", "option": ""}

    Returns:
        制表符分隔的文本
    """
    try:
        result = kegg_api.kegg_conv(
            target_db=target_db, source_db=source_db_or_dbentries, option=option
        )
    except Exception as e:
        return {"error": f"An error occurred while querying kegg_conv: {str(e)}"}
    return result


@mcp.tool()
async def kegg_link(target_db: str, source_db_or_dbentries: str, option: str):
    """KEGG link - 通过使用数据库交叉引用查找相关条目。

    Args:
        target_db: 指定要映射到的目标数据库名称（字符串）
        source_db_or_dbentries: 数据库名称或特定条目标识符（字符串）
        option: 控制返回结果的格式或范围（字符串）

    Query example: {"target_db": "pathway", "source_db_or_dbentries": "hsa:10458", "option": ""}

    Returns:
        制表符分隔的文本
    """
    try:
        result = kegg_api.kegg_link(
            target_db=target_db, source_db=source_db_or_dbentries, option=option
        )
    except Exception as e:
        return {"error": f"An error occurred while querying kegg_link: {str(e)}"}
    return result


@mcp.prompt()
def system_prompt():
    """客户端的系统提示。"""
    prompt = """您可以访问用于搜索 KEGG 的工具，KEGG 是一个数据库资源，用于从分子水平信息（特别是基因组测序和其他高通量实验技术生成的大规模分子数据集）理解生物系统（如细胞、生物体和生态系统）的高级功能和效用。
    使用 API 工具提取相关信息。
    如果用户未提供缺失的参数，请用合理的值填充。"""
    return prompt


if __name__ == "__main__":
    # Initialize and run the server
    # mcp.run(transport='sse')
    mcp.run(transport="stdio")
