from mcp.server.fastmcp import FastMCP

from tools.biodb.uniprot.uniprot_api import UNIPROTAPI


mcp = FastMCP(
    "uniprot_mcp", 
    stateless_http=True
)
uniprot_api = UNIPROTAPI()


@mcp.tool()
async def get_general_info_by_protein_or_gene_name(query: str, sepcies: str = 'Homo sapiens'):
    """
    通过蛋白质或基因名称从 UniProt 数据库获取一般信息。
    
    Args:
        name: 蛋白质或基因名称。
        sepcies: 物种名称。
    
    Query example: {"query": "TP53"}
        
    Returns:
        包含蛋白质或基因一般信息的 JSON 字符串。
    """
    try:
        result = uniprot_api.get_general_info_by_protein_or_gene_name(query=query, species=sepcies)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result
    

@mcp.tool()
async def get_uniprotkb_entry_by_accession(accession: str):
    """
    通过蛋白质条目登录号搜索 UniProtKB，返回与该条目相关的所有数据。
    
    Args:
        accession: UniProtKB 登录号 ID（字符串，必需）
    
    Query example: {"accession": "P68871"}
    
    Returns:
        包含指定 UniProtKB 条目所有相关数据的 JSON 字符串，包括条目类型、主要和次要登录号 ID、UniProtKB ID、注释评分、生物体详情、蛋白质描述、基因名称、功能注释，以及序列和数据库交叉引用等附加注释。
    """

    try:
        result = uniprot_api.get_uniprotkb_entry_by_accession(accession=accession)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def stream_uniprotkb_entries(query: str):
    """
    在单次下载中流式传输与搜索词相关的所有 UniProtKB 条目。
    
    Args:
        query: UniProtKB 条目的搜索词，例如蛋白质名称或关键词（如 "hemoglobin"）（字符串，必需）
    
    Query example: {"query": "hemoglobin"}
    
    Returns:
        包含与搜索查询匹配的 UniProtKB 条目列表的 JSON 字符串。每个条目包括条目类型、主要和次要登录号 ID、UniProtKB ID、条目审计信息、注释评分、生物体详情、蛋白质描述（推荐名称、替代名称和包含的分子）、基因名称、功能注释，以及序列和特征等附加注释。
    """

    try:
        result = uniprot_api.stream_uniprotkb_entries(query=query)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def search_uniprotkb_entries(query: str):
    """
    使用查询搜索 UniProtKB 条目，返回分页列表。
    
    Args:
        query: UniProtKB 条目的搜索词，例如蛋白质名称或关键词（如 "hemoglobin"）（字符串，必需）
    
    Query example: {"query": "hemoglobin"}
    
    Returns:
        包含与搜索查询匹配的 UniProtKB 条目分页列表的 JSON 字符串。每个条目包括条目类型、主要登录号 ID、UniProtKB ID、生物体详情、蛋白质描述（推荐名称、替代名称和包含的分子）、基因名称、功能注释，以及组织特异性等附加特征。
    """

    try:
        result = uniprot_api.search_uniprotkb_entries(query=query)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_uniref_cluster_by_id(uniref_id: str):
    """
    通过 ID 搜索 UniRef 条目，返回与该条目相关的所有数据。
    
    Args:
        uniref_id: UniRef 簇 ID（字符串，必需）
    
    Query example: {"uniref_id": "UniRef90_P68871"}
    
    Returns:
        包含指定 UniRef 簇所有相关数据的 JSON 字符串，包括簇 ID、名称、成员数量、更新日期、条目类型、共同分类、代表性成员（包含序列和 UniProtKB 登录号），以及簇成员列表及其各自的生物体和序列详情。
    """

    try:
        result = uniprot_api.get_uniref_cluster_by_id(uniref_id=uniref_id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_uniref_cluster_members_by_id(uniref_id: str):
    """
    通过成员 ID 搜索 UniRef 条目，返回与该条目相关的所有数据。
    
    Args:
        uniref_id: UniRef 簇 ID（字符串，必需）
    
    Query example: {"uniref_id": "UniRef90_P68871"}
    
    Returns:
        包含指定 UniRef 簇中成员列表的 JSON 字符串。每个成员包括成员 ID 类型、成员 ID、生物体名称和分类 ID、序列长度、蛋白质名称、UniProtKB 登录号、相关的 UniRef50/100 和 UniParc ID，以及序列详情（值、长度、分子量、CRC64 校验和、MD5 哈希）。
    """

    try:
        result = uniprot_api.get_uniref_cluster_members_by_id(uniref_id=uniref_id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_uniref_light_cluster_by_id(uniref_id: str):
    """
    通过 ID 搜索轻量级 UniRef 条目，返回与该条目相关的所有数据。
    
    Args:
        uniref_id: UniRef 簇 ID（字符串，必需）
    
    Query example: {"uniref_id": "UniRef90_P68871"}
    
    Returns:
        包含指定 UniRef 簇轻量级数据的 JSON 字符串，包括簇 ID、名称、更新日期、条目类型、共同分类、成员和生物体数量、代表性成员详情（包含序列和 UniProtKB 登录号）、种子 ID、成员 ID 类型、成员 ID 列表，以及部分生物体信息。
    """

    try:
        result = uniprot_api.get_uniref_light_cluster_by_id(uniref_id=uniref_id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def stream_uniref_clusters(query: str):
    """
    在单次下载中流式传输与搜索词相关的所有 UniRef 簇。
    
    Args:
        query: UniRef 簇的搜索词，例如蛋白质名称或关键词（如 "hemoglobin"）（字符串，必需）
    
    Query example: {"query": "hemoglobin"}
    
    Returns:
        包含与搜索查询匹配的 UniRef 簇列表的 JSON 字符串。每个簇包括簇 ID、名称、更新日期、条目类型、共同分类、成员和生物体数量、代表性成员详情（包含序列和 UniProtKB 登录号）、种子 ID、成员 ID 类型、成员 ID，以及生物体详情。
    """

    try:
        result = uniprot_api.stream_uniref_clusters(query=query)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def search_uniref_clusters(query: str):
    """
    使用查询搜索 UniRef 簇，返回分页列表。
    
    Args:
        query: UniRef 簇的搜索词，例如蛋白质名称或关键词（如 "hemoglobin"）（字符串，必需）
    
    Query example: {"query": "hemoglobin"}
    
    Returns:
        包含与搜索查询匹配的 UniRef 簇分页列表的 JSON 字符串。每个簇包括簇 ID、名称、更新日期、条目类型、共同分类、成员和生物体数量、代表性成员详情（包含序列和 UniProtKB 登录号）、种子 ID、成员 ID 类型、成员 ID，以及生物体详情。
    """

    try:
        result = uniprot_api.search_uniref_clusters(query=query)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_uniparc_entry_by_upi(uniparc_id: str):
    """
    通过 ID (UPI) 搜索 UniParc 条目，返回与该条目相关的所有数据。
    
    Args:
        uniparc_id: UniParc UPI ID（字符串，必需）
    
    Query example: {"uniparc_id": "UPI00000015C9"}
    
    Returns:
        包含指定 UniParc 条目所有相关数据的 JSON 字符串，包括 UniParc ID、蛋白质序列（值、长度、分子量、CRC64 校验和、MD5 哈希），以及来自 Pfam、PROSITE 和 InterPro 等数据库的序列特征。
    """

    try:
        result = uniprot_api.get_uniparc_entry_by_upi(uniparc_id=uniparc_id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_uniparc_light_entry_by_upi(uniparc_id: str):
    """
    通过 ID (UPI) 搜索 UniParc 条目，返回与该条目相关的所有数据（轻量级版本）。
    
    Args:
        uniparc_id: UniParc UPI ID（字符串，必需）
    
    Query example: {"uniparc_id": "UPI00000015C9"}
    
    Returns:
        包含指定 UniParc 条目轻量级数据的 JSON 字符串，包括 UniParc ID、蛋白质序列（值、长度、分子量、CRC64 校验和、MD5 哈希）、交叉引用数量、共同分类单元、UniProtKB 登录号，以及来自 Pfam、PROSITE 和 InterPro 等数据库的序列特征。
    """

    try:
        result = uniprot_api.get_uniparc_light_entry_by_upi(uniparc_id=uniparc_id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_uniparc_cross_references_by_upi(uniparc_id: str):
    """
    通过 UPI 获取数据库交叉引用条目的分页列表。
    
    Args:
        uniparc_id: UniParc UPI ID（字符串，必需）
    
    Query example: {"uniparc_id": "UPI000035B535"}
    
    Returns:
        包含指定 UniParc UPI 的数据库交叉引用条目分页列表的 JSON 字符串，包括数据库类型、登录号 ID、活动状态，以及蛋白质名称和分类等相关属性。
    """

    try:
        result = uniprot_api.get_uniparc_cross_references_by_upi(uniparc_id=uniparc_id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def stream_uniparc_cross_references_by_upi(uniparc_id: str):
    """
    流式传输指定 UniParc UPI 的数据库交叉引用条目。
    
    Args:
        uniparc_id: UniParc UPI ID（字符串，必需）
    
    Query example: {"uniparc_id": "UPI000041C017"}
    
    Returns:
        包含流式传输的交叉引用条目的 JSON 字符串，每个条目将 UniParc ID 链接到源数据库登录号，包括数据库类型、登录号、版本、活动状态和分类信息等详情。
    """

    try:
        result = uniprot_api.stream_uniparc_cross_references_by_upi(uniparc_id=uniparc_id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def stream_uniparc_entries(uniparc_id: str):
    """
    在单次下载中流式传输与指定搜索词相关的所有 UniParc 条目。
    
    Args:
        uniparc_id: UniParc 条目的搜索词，通常是 UniParc UPI ID（字符串，必需）
    
    Query example: {"uniparc_id": "UPI0000086E9C"}
    
    Returns:
        包含与搜索词匹配的 UniParc 条目列表的 JSON 字符串。每个条目包括 UniParc ID、序列详情（值、长度、分子量、CRC64 校验和、MD5 哈希）、交叉引用数量、UniProtKB 登录号、共同分类单元，以及来自 Pfam、InterPro 和 PROSITE 等数据库的序列特征。
    """

    try:
        result = uniprot_api.stream_uniparc_entries(uniparc_id=uniparc_id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def search_uniparc_entries(entry: str):
    """
    使用查询搜索 UniParc 条目，返回分页列表。
    
    Args:
        entry: UniParc 条目的搜索词，通常采用 "字段:值" 格式（如 "protein:hemoglobin"）（字符串，必需）
    
    Query example: {"entry": "protein:hemoglobin"}
    
    Returns:
        包含与搜索查询匹配的 UniParc 条目分页列表的 JSON 字符串。每个条目包括 UniParc ID、序列详情（值、长度、分子量、CRC64 校验和、MD5 哈希）、交叉引用数量、UniProtKB 登录号、共同分类单元、来自 Pfam 和 PROSITE 等数据库的序列特征，以及交叉引用的创建/更新日期。
    """

    try:
        result = uniprot_api.search_uniparc_entries(entry=entry)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_gene_centric_by_accession(accession: str):
    """
    通过 UniProtKB 登录号检索 GeneCentric 条目。
    
    Args:
        accession: UniProtKB 登录号 ID（字符串）
    
    
    Query example: {"accession": "P12345"}
    
    Returns:
        包含以下内容的字典列表：
    Gene Name: 与蛋白质相关的标准化基因符号
    Protein Name: 蛋白质的描述性名称
    UniProtKB ID: UniProt 登录号（主要标识符）
    Proteome ID: 包含该蛋白质的蛋白质组条目标识符
    Organism: 物种名称
    Taxon ID: 生物体的 NCBI 分类标识符
    Entry Type: UniProt 条目状态
    Protein Existence: 蛋白质的证据级别
    Flag Type: 附加注释（'Precursor' 表示前体状态）
    Sequence:
    -Length: 氨基酸数量
    -Molecular Weight: 以道尔顿为单位的近似质量
    -CRC64: 序列的校验和
    -MD5: 序列的 MD5 哈希
    -Sequence Version: UniProt 中序列的版本号
    """

    try:
        result = uniprot_api.get_gene_centric_by_accession(accession=accession)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_gene_centric_by_proteome(upid: str):
    """
    通过蛋白质组 ID 搜索 GeneCentric 条目，返回与该条目相关的所有数据。
    
    Args:
        upid: UniProt 蛋白质组 ID（字符串）
    
    
    Query example: {"upid": "UP000005640"}
    
    Returns:
        包含以下内容的字典列表：
    Gene Name: 基因符号
    Protein Name: 蛋白质的全名或描述
    UniProtKB ID: 规范蛋白质的 UniProt 标识符
    Proteome ID: 蛋白质所属的蛋白质组标识符
    Organism: 物种名称 
    Taxon ID: NCBI 分类 ID 
    Entry Type: UniProt 条目的状态
    Protein Existence: 证据级别 
    Flag Type: 注释详情，如 "Precursor" 或 "Fragment"
    Sequence:
    -Length: 氨基酸数量
    -Molecular Weight: 以道尔顿为单位
    -CRC64: 校验和
    -MD5: MD5 哈希
    -Sequence Version: 序列的版本号
    """

    try:
        result = uniprot_api.get_gene_centric_by_proteome(upid=upid)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def stream_gene_centric(accession: str):
    """
    流式传输与查询匹配的 GeneCentric 条目（最多 1000 万条）。
    Args:
        accession (str): GeneCentric 条目的搜索词。
    Returns:
        包含所有匹配的 GeneCentric 条目的 JSON 字符串。
    
    Query example: {"accession": "gene:PAX6"}
    """

    try:
        result = uniprot_api.stream_gene_centric(accession=accession)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def search_gene_centric(accession: str):
    """
    使用分页搜索 GeneCentric 条目。
    Args:
        accession (str): GeneCentric 条目的搜索词。
    Returns:
        包含分页的 GeneCentric 条目的 JSON 字符串。
    
    Query example: {"accession": "gene:TP53"}
    """

    try:
        result = uniprot_api.search_gene_centric(accession=accession)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_proteome_by_id(upid: str):
    """
    通过 UniProt 蛋白质组 ID 检索蛋白质组。
    Args:
        upid (str): UniProt 蛋白质组 ID。
    Returns:
        包含蛋白质组数据的 JSON 字符串。
    
    Query example: {"upid": "UP000002311"}
    """

    try:
        result = uniprot_api.get_proteome_by_id(upid=upid)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def stream_proteomes(query: str):
    """
    流式传输与查询匹配的蛋白质组条目（最多 1000 万条）。
    Args:
        query (str): 蛋白质组的搜索词。
    Returns:
        包含所有匹配的蛋白质组的 JSON 字符串。
    """
    try:
        result = uniprot_api.stream_proteomes(query=query)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def search_proteomes(query: str, size: int = 50):
    """
    使用分页搜索蛋白质组条目。
    Args:
        query (str): 蛋白质组的搜索词。
        size (int, optional): 每页的条目数量。默认为 50。
    Returns:
        包含分页的蛋白质组条目的 JSON 字符串。
    """
    try:
        result = uniprot_api.search_proteomes(query=query, size=size)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.prompt()
def system_prompt():
    """UniProt MCP 服务器客户端的系统提示。"""
    prompt = """您可以访问用于搜索 UniProt 的工具：蛋白质知识库和相关资源。\n使用 API 工具提取相关信息。\n如果用户未提供缺失的参数，请用合理的值填充。"""
    return prompt

