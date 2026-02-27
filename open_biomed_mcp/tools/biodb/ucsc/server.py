from mcp.server.fastmcp import FastMCP

from tools.biodb.ucsc.ucsc_api import UCSCAPI


mcp = FastMCP(
    "ucsc_mcp",
    stateless_http=True,
)
ucsc_api = UCSCAPI()

@mcp.tool()
async def list_genomes():
    """从 UCSC 基因组浏览器获取所有支持的基因组组装。
    
    Args:
    
    Query example: {}
    
    Returns:
        包含 UCSC 基因组浏览器所有支持的基因组组装的字典，包含元数据（downloadTime、dataTime）和详细的基因组信息。
    """

    try:
        return ucsc_api.list_genomes()
    except Exception as e:
        return {"error": f"Failed to list genomes: {str(e)}"}

@mcp.tool()
async def list_tracks(genome: str):
    """列出特定基因组组装的所有轨道。
    
    Args:
        genome: 基因组组装名称（例如 'hg38'）（字符串）
    
    Query example: {"genome": "hg38"}
    
    Returns:
        包含指定基因组所有轨道的字典。
    """

    try:
        return ucsc_api.list_tracks(genome)
    except Exception as e:
        return {"error": f"Failed to list tracks: {str(e)}"}

@mcp.tool()
async def list_hub_tracks(hub_url: str, genome: str):
    """列出基因组的特定轨道中心中的所有轨道。
    
    Args:
        hub_url: 轨道中心的 URL（字符串）
        genome: 基因组组装名称（字符串）
    
    Query example: {
        "hub_url": "http://hgdownload.soe.ucsc.edu/hubs/GCA/009/914/755/GCA_009914755.4/hub.txt",
        "genome": "hg38"
    }
    
    Returns:
        包含中心中轨道的字典
    """

    try:
        return ucsc_api.list_hub_tracks(hub_url, genome)
    except Exception as e:
        return {"error": f"Failed to list hub tracks: {str(e)}"}

@mcp.tool()
async def list_chromosomes(genome: str):
    """列出基因组组装的所有染色体。
    
    Args:
        genome: 基因组组装名称（字符串）
    
    Query example: {"genome": "hg38"}
    
    Returns:
        包含染色体信息的字典，包括将染色体名称映射到其长度（以碱基对为单位）的 'chromosomes' 键，以及下载时间和染色体计数等元数据。
    """

    try:
        return ucsc_api.list_chroms(genome)
    except Exception as e:
        return {"error": f"Failed to list chromosomes: {str(e)}"}

@mcp.tool()
async def list_public_hubs():
    """获取所有公共 UCSC 轨道中心的列表。
    
    Args:
        None
    
    Query example: {}
    
    Returns:
        包含 'publicHubs' 键下的公共 UCSC 轨道中心列表的字典，其中每个中心由 hubUrl、shortLabel、longLabel、registrationTime、dbCount、dbList 和 descriptionUrl 等字段描述，以及下载时间等元数据。
    """

    try:
        return ucsc_api.list_hubs()
    except Exception as e:
        return {"error": f"Failed to list public hubs: {str(e)}"}

@mcp.tool()
async def get_chromosome_sequence(genome: str, chrom: str):
    """获取整个染色体的序列。
    
    Args:
        genome: 基因组组装名称（字符串）
        chrom: 染色体名称（例如 'chr1'）（字符串）
    
    Query example: {"genome": "hg38", "chrom": "chr1"}
    
    Returns:
        [基于测试结果的返回描述]
    """

    try:
        return ucsc_api.get_chrom_sequence(genome, chrom)
    except Exception as e:
        return {"error": f"Failed to get chromosome sequence: {str(e)}"}

@mcp.tool()
async def get_sequence(
    genome: str,
    chrom: str,
    start: int = None,
    end: int = None,
    revcomp: bool = False,
    hub_url: str = None
):
    """获取基因组区域的 DNA 序列。
    
    Args:
        genome: 基因组组装名称（字符串）
        chrom: 染色体名称（字符串）
        start: 起始位置（可选）（整数或 null）
        end: 结束位置（可选）（整数或 null）
        revcomp: 返回反向互补序列（默认：False）（布尔值）
        hub_url: 轨道中心 URL（可选）（字符串或 null）
    
    Query example: {"genome": "hg38", "chrom": "chr1", "start": 1000, "end": 2000, "revcomp": false, "hub_url": null}
    
    Returns:
        包含 'dna' 键下指定基因组区域的 DNA 序列的字典，以及基因组、染色体、起始、结束和下载时间等元数据。序列可能包含 'N' 表示未知或掩蔽的碱基。
    """

    try:
        return ucsc_api.get_sequence(genome, chrom, start, end, revcomp, hub_url)
    except Exception as e:
        return {"error": f"Failed to get sequence: {str(e)}"}

@mcp.tool()
async def get_track_data(
    genome: str,
    track: str,
    chrom: str = None,
    start: int = None,
    end: int = None,
    max_items: int = None
):
    """获取基因组区域的特定轨道数据。
    
    Args:
        genome: 基因组组装名称（字符串）
        track: 轨道名称（字符串）
        chrom: 染色体名称（字符串或 null）
        start: 起始位置（整数或 null）
        end: 结束位置（整数或 null）
        max_items: 返回的最大项目数（整数或 null）
    
    Query example: {"genome": "hg38", "track": "knownGene", "chrom": "chr1", "start": 100000, "end": 200000, "max_items": 100}
    
    Returns:
        包含轨道元数据和指定基因组区域内基因对象列表的字典。每个基因对象包括详细信息，如染色体坐标、基因名称、链、外显子结构和各种注释。
    """

    try:
        return ucsc_api.get_track_data(genome, track, chrom, start, end, max_items)
    except Exception as e:
        return {"error": f"Failed to get track data: {str(e)}"}

@mcp.tool()
async def get_cytoband(genome: str, chrom: str = None):
    """获取指定基因组和染色体的细胞带（染色体带）信息。
    
    Args:
        genome: 基因组组装名称（字符串，必需）
        chrom: 染色体名称（字符串或 null，可选，默认=null）
    
    Query example: {"genome": "hg38", "chrom": "chr1"}
    
    Returns:
        包含细胞带信息的字典，包括指定基因组和染色体（如果提供）的细胞带记录列表。每条记录通常包括染色体名称、起始和结束位置、带名称和 Giemsa 染色水平等字段。
    """

    try:
        return ucsc_api.get_cytoband(genome, chrom)
    except Exception as e:
        return {"error": f"Failed to get cytoband data: {str(e)}"}

@mcp.prompt()
def system_prompt():
    """客户端的系统提示。"""
    return """你可以访问用于查询 UCSC 基因组浏览器 API 的工具。
    使用这些工具检索基因组数据，包括序列、轨道和注释。
    在需要时提供基因组组装名称（例如 hg38）。"""
