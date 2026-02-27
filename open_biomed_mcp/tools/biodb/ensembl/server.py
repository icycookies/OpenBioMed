from mcp.server.fastmcp import FastMCP

from tools.biodb.ensembl.ensembl_api import EnsemblClient


mcp = FastMCP(
    "ensembl_mcp",
    stateless_http=True,
)

ensembl_api = EnsemblClient()


DEFAULT_MAX_LENGTH = 10240


@mcp.tool()
async def get_lookup_symbol(symbol: str, species: str = "homo_sapiens", max_length: int = DEFAULT_MAX_LENGTH):
    """通过外部基因符号查找 Ensembl 基因信息。
    
    此函数允许您使用标准基因符号（例如人类基因的 HGNC 符号）查找 Ensembl 基因记录。
    
    Args:
        species: 蛇形命名格式的物种名称（例如，'homo_sapiens' 表示人类，'mus_musculus' 表示小鼠）
        symbol: 官方基因符号（例如，'BRCA2'、'TP53'、'APOE'）
        max_length: 响应的最大长度（以近似令牌数计，默认：8192）
    
    Query example: {"species": "homo_sapiens", "symbol": "BRCA2"}
    
    Returns:
        包含全面基因信息的字典，包括 Ensembl ID、基因组位置、
        生物类型（例如 protein_coding、lncRNA）、描述以及外部数据库的交叉引用。
    """

    result = ensembl_api.get_lookup_symbol(species=species, symbol=symbol, max_length=max_length)
    if "error" in result:
        return {"error": f"An error occurred while looking up gene: {result['error']}"}
    return result

@mcp.tool()
async def get_homology_symbol(symbol: str, species: str = "homo_sapiens", max_length: int = DEFAULT_MAX_LENGTH):
    """查找通过符号标识的基因的进化同源物（直系同源物和旁系同源物）。
    
    检索不同物种的同源基因，包含比对统计信息和分类学信息。
    对比较基因组学和进化研究至关重要。
    
    Args:
        species: 蛇形命名格式的物种名称（例如，'homo_sapiens' 表示人类）
        symbol: 官方基因符号（例如，'BRCA2'、'TP53'、'FOXP2'）
        max_length: 响应的最大长度（以近似令牌数计，默认：8192）
    
    Query example: {"species": "homo_sapiens", "symbol": "FOXP2"}
    
    Returns:
        包含同源性信息的字典，包括：
        - 直系同源物（不同物种中源自共同祖先基因的基因）
        - 旁系同源物（基因组内复制产生的基因）
        - 比对统计信息（一致性、覆盖率）
        - 每个同源物的分类学信息
    """

    result = ensembl_api.get_homology_symbol(species=species, symbol=symbol, max_length=max_length)
    if "error" in result:
        return {"error": f"An error occurred while getting homology: {result['error']}"}
    return result

@mcp.tool()
async def get_sequence_region(region: str, species: str = "homo_sapiens", max_length: int = DEFAULT_MAX_LENGTH):
    """检索特定染色体区域的基因组 DNA 序列。
    
    从特定基因组位置提取原始核苷酸序列，可用于引物设计、变异分析或序列特征识别。
    
    Args:
        species: 蛇形命名格式的物种名称（例如，'homo_sapiens' 表示人类）
        region: 基因组区域，格式为 'chromosome:start..end'（例如，'X:1000000..1000100'、
                '7:55152337..55207337'、'MT:1..16569'）。坐标为基于 1 的闭区间。
        max_length: 响应的最大长度（以近似令牌数计，默认：8192）
    
    Query example: {"species": "homo_sapiens", "region": "X:1000000..1000100"}
    
    Returns:
        包含 DNA 序列（核苷酸字符串 A、C、G、T）的字典，
        以及关于区域、序列长度和坐标系统的元数据。
    """

    result = ensembl_api.get_sequence_region(species=species, region=region, max_length=max_length)
    if "error" in result:
        return {"error": f"An error occurred while getting sequence: {result['error']}"}
    return result

@mcp.tool()
async def get_vep_hgvs(hgvs_notation: str, species: str = "homo_sapiens", max_length: int = DEFAULT_MAX_LENGTH):
    """使用变异效应预测器（VEP）和 HGVS 表示法预测变异的功能效应。
    
    分析遗传变异对基因、转录本和蛋白质序列的分子后果。
    VEP 提供全面的注释，包括蛋白质变化、调控效应、保守性评分和致病性预测。

    Args:
        species: 蛇形命名格式的物种名称（例如，'homo_sapiens' 表示人类）
        hgvs_notation: HGVS（人类基因组变异协会）表示法格式的变异
                      （例如，'ENST00000269305.4:c.2309C>T'、'NM_000059.3:c.274G>A'、
                       'NC_000017.10:g.7676154G>T'）
        max_length: 响应的最大长度（以近似令牌数计，默认：8192）

    Returns:
        包含详细变异效应预测的字典，包括：
        - 受影响的基因和转录本
        - 对蛋白质序列的影响（错义、无义等）
        - SIFT 和 PolyPhen 致病性评分
        - 保守性评分
        - 群体数据库中的等位基因频率
        - 调控特征注释
        - 临床意义注释
    """
    result = ensembl_api.get_vep_hgvs(species=species, hgvs_notation=hgvs_notation, max_length=max_length)
    if "error" in result:
        return {"error": f"An error occurred while getting variant effect: {result['error']}"}
    return result

@mcp.tool()
async def get_genetree_id(id: str, max_length: int = DEFAULT_MAX_LENGTH, species: str = "homo_sapiens"):
    """通过 Ensembl 稳定标识符检索系统发育基因树。
    
    基因树表示基因跨物种的进化历史，显示直系同源和旁系同源关系。
    这些树是使用蛋白质序列比对和系统发育算法构建的。
    
    Args:
        id: Ensembl 基因树稳定标识符（例如，'ENSGT00390000003602'）
        max_length: 响应的最大长度（以近似令牌数计，默认：8192）
    
    Query example: {"id": "ENSGT00390000003602"}
    
    Returns:
        包含嵌套结构基因树信息的字典，包括：
        - 分类学和序列关系
        - 表示进化距离的分支长度
        - 表示树置信度的自举值
        - 用于构建树的序列比对
        - 来自不同物种的成员基因
    """

    result = ensembl_api.get_genetree_id(id=id, max_length=max_length)
    if "error" in result:
        return {"error": f"An error occurred while getting gene tree: {result['error']}"}
    return result

@mcp.tool()
async def get_info_assembly(species: str, max_length: int = DEFAULT_MAX_LENGTH):
    """检索物种的基因组组装信息。
    
    提供 Ensembl 中使用的参考基因组组装的详细信息，包括组装版本、登录号和整体结构。
    对于理解坐标系统和基因组组织至关重要。
    
    Args:
        species: 蛇形命名格式的物种名称（例如，'homo_sapiens' 表示人类、
                 'mus_musculus' 表示小鼠、'danio_rerio' 表示斑马鱼）
        max_length: 响应的最大长度（以近似令牌数计，默认：8192）
    
    Query example: {"species": "homo_sapiens"}
    
    Returns:
        包含全面组装信息的字典，包括：
        - 组装名称和版本（例如，人类的 'GRCh38'）
        - 组装登录号（例如，'GCA_000001405.15'）
        - 顶层序列（染色体、支架、重叠群）
        - 坐标系统信息
        - 组装日期和来源
        - 组装统计信息（序列计数、长度）
    """

    result = ensembl_api.get_info_assembly(species=species, max_length=max_length)
    if "error" in result:
        return {"error": f"An error occurred while getting assembly info: {result['error']}"}
    return result

@mcp.tool()
async def get_xrefs_symbol(symbol: str, species: str = "homo_sapiens"):
    """获取基因符号的交叉引用。
    
    Args:
        species: 物种名称（例如 'homo_sapiens' 表示人类）
        symbol: 基因符号（例如 'BRCA2'）
    
    Query example: {"species": "homo_sapiens", "symbol": "BRCA2"}
    
    Returns:
        包含其他数据库交叉引用的字典列表。
    """

    try:
        result = ensembl_api.get_xrefs_symbol(species=species, symbol=symbol)
    except Exception as e:
        return {"error": f"An error occurred while getting cross references: {str(e)}"}
    return result

# Archive endpoints
@mcp.tool()
async def get_archive_id(id: str):
    """获取 Ensembl 稳定标识符的最新版本。
    
    Args:
        id: Ensembl 稳定标识符（例如，'ENSG00000139618'）
    
    Query example: {"id": "ENSG00000139618"}
    
    Returns:
        包含给定标识符最新版本信息的字典。
    """

    try:
        result = ensembl_api.get_archive_id(id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def post_archive_id(ids: list[str]):
    """获取多个 Ensembl 稳定标识符的最新版本。
    
    Args:
        ids: Ensembl 稳定标识符列表。
    
    Query example: {"ids": ["ENSG00000139618", "ENSG00000168269"]}
    
    Returns:
        一个字典，其中键是输入 ID，值是包含每个 ID 最新版本信息的字典。
    """

    try:
        result = ensembl_api.post_archive_id(ids=ids)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

# Comparative Genomics endpoints
@mcp.tool()
async def get_cafe_genetree_id(id: str):
    """通过 ID 检索 CAFE（基因家族进化计算分析）基因树。
    
    CAFE 分析基因家族大小在系统发育树上的进化，识别整个进化过程中基因家族的扩张和收缩。
    这有助于理解适应、功能多样化和物种特异性特征。
    
    Args:
        id: Ensembl 基因树稳定标识符（例如，'ENSGT00390000003602'）
    
    Query example: {"id": "ENSGT00390000003602"}
    
    Returns:
        包含 CAFE 基因树数据的字典，包括：
        - 进化时间上的基因家族大小变化
        - 扩张/收缩的统计显著性
        - 基因家族大小变化的 P 值
        - 带有基因计数信息的物种树拓扑
    """

    try:
        result = ensembl_api.get_cafe_genetree_id(id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_cafe_genetree_member_symbol(symbol: str, species: str = "homo_sapiens"):
    """检索通过符号标识的基因的 CAFE 基因树。
    
    获取包含指定基因的基因家族的基因家族进化分析（扩张/收缩）。
    无需知道特定基因树 ID 即可识别进化模式。
    
    Args:
        species: 蛇形命名格式的物种名称（例如，'homo_sapiens' 表示人类）
        symbol: 官方基因符号（例如，'BRCA2'、'TP53'、'OR4F5'）
    
    Query example: {"species": "homo_sapiens", "symbol": "OR4F5"}
    
    Returns:
        包含 CAFE 基因树数据的字典，包括：
        - 进化时间上的基因家族大小变化
        - 扩张/收缩的统计显著性
        - 基因家族大小变化的 P 值
        - 带有基因计数信息的物种树拓扑
    """

    try:
        result = ensembl_api.get_cafe_genetree_member_symbol(species=species, symbol=symbol)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_cafe_genetree_member_id(id: str, species: str = "homo_sapiens"):
    """检索包含通过 Ensembl ID 标识的基因的基因树。
    
    查找显示感兴趣基因进化关系的系统发育树，使用其 Ensembl 稳定标识符进行标识。
    当您拥有特定基因 ID 时，对于理解基因进化很有用。
    
    Args:
        species: 蛇形命名格式的物种名称（例如，'homo_sapiens' 表示人类）
        id: Ensembl 基因、转录本或翻译稳定标识符
            （例如，'ENSG00000139618' 表示人类 BRCA2 基因）
    
    Query example: {"species": "homo_sapiens", "id": "ENSG00000139618"}
    
    Returns:
        包含嵌套结构基因树信息的字典，包括：
        - 分类学和序列关系
        - 表示进化距离的分支长度
        - 表示树置信度的自举值
        - 用于构建树的序列比对
        - 来自不同物种的成员基因
    """

    try:
        result = ensembl_api.get_cafe_genetree_member_id(species=species, id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_genetree_member_symbol(symbol: str, species: str = "homo_sapiens"):
    """通过符号获取基因树。
    
    Args:
        species: 物种名称（例如 'homo_sapiens' 表示人类）
        symbol: 基因符号
    
    Query example: {"species": "homo_sapiens", "symbol": "BRCA2"}
    
    Returns:
        包含基因树信息的字典。
    """

    try:
        result = ensembl_api.get_genetree_member_symbol(species=species, symbol=symbol)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_alignment_region(region: str, species: str = "homo_sapiens"):
    """检索特定区域的物种间基因组比对。
    
    获取跨物种基因组区域的多序列比对，显示进化保守性和分歧。
    对于识别保守的功能元件（如增强子）或检测选择压力至关重要。
    
    Args:
        species: 蛇形命名格式的参考物种名称（例如，'homo_sapiens'）
        region: 基因组区域，格式为 'chromosome:start..end'（例如，'X:1000000..1000100'）
                坐标为基于 1 的闭区间。
    
    Query example: {"species": "homo_sapiens", "region": "X:1000000..1000100"}
    
    Returns:
        包含指定区域多个物种比对序列的字典，
        包括比对块、评分以及基因组之间的坐标映射。
    """

    try:
        result = ensembl_api.get_alignment_region(species=species, region=region)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_homology_id(id: str, species: str = "homo_sapiens"):
    """查找通过 Ensembl ID 标识的基因的进化同源物（直系同源物和旁系同源物）。
    
    检索不同物种的同源基因，包含比对统计信息和分类学信息。
    对比较基因组学和进化研究至关重要。
    
    Args:
        species: 蛇形命名格式的物种名称（例如，'homo_sapiens' 表示人类）
        id: Ensembl 基因 ID（例如，'ENSG00000139618' 表示人类 BRCA2 基因）
    
    Query example: {"species": "homo_sapiens", "id": "ENSG00000139618"}
    
    Returns:
        包含同源性信息的字典，包括：
        - 直系同源物（不同物种中源自共同祖先基因的基因）
        - 旁系同源物（基因组内复制产生的基因）
        - 比对统计信息（一致性、覆盖率）
        - 每个同源物的分类学信息
    """

    try:
        result = ensembl_api.get_homology_id(species=species, id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

# Cross References endpoints
@mcp.tool()
async def get_xrefs_id(id: str):
    """通过 ID 获取交叉引用。
    
    Args:
        id: Ensembl 稳定标识符
    
    Query example: {"id": "ENSG00000139618"}
    
    Returns:
        包含其他数据库交叉引用的字典列表。
    """

    try:
        result = ensembl_api.get_xrefs_id(id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_xrefs_name(name: str, species: str = "homo_sapiens"):
    """通过名称获取交叉引用。
    
    Args:
        species: 物种名称（例如 'homo_sapiens' 表示人类）
        name: 外部名称
    
    Query example: {"species": "homo_sapiens", "name": "BRCA2"}
    
    Returns:
        包含其他数据库交叉引用的字典列表。
    """

    try:
        result = ensembl_api.get_xrefs_name(species=species, name=name)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

# Information endpoints
@mcp.tool()
async def get_info_analysis(species: str = "homo_sapiens"):
    """列出用于物种基因组的分析和数据处理流程。
    
    提供有关用于生成物种 Ensembl 数据的计算方法和分析的信息，
    包括基因注释方法、比较基因组学分析和变异数据处理。
    
    Args:
        species: 蛇形命名格式的物种名称（例如，'homo_sapiens' 表示人类）
    
    Query example: {"species": "homo_sapiens"}
    
    Returns:
        包含物种分析信息的字典，包括：
        - 基因注释方法和来源
        - 使用的比对算法
        - 变异调用程序
        - 调控特征检测方法
        - 比较基因组学流程详细信息
    """

    try:
        result = ensembl_api.get_info_analysis(species=species)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_assembly_region_info(region_name: str, species: str = "homo_sapiens"):
    """检索特定基因组区域或染色体的详细信息。
    
    获取基因组组装中特定序列的组装元数据，例如染色体长度、支架组成或重叠群信息。
    
    Args:
        species: 蛇形命名格式的物种名称（例如，'homo_sapiens' 表示人类）
        region_name: 顶层序列的名称（例如，'1' 表示 1 号染色体、
                     'X' 表示 X 染色体、'KZ622775.1' 表示支架）
    
    Query example: {"species": "homo_sapiens", "region_name": "X"}
    
    Returns:
        包含指定区域详细信息的字典，包括：
        - 序列长度
        - 坐标系统
        - 组装异常（如果有）
        - 序列组成
        - 相关元数据和属性
    """

    try:
        result = ensembl_api.get_assembly_region_info(species=species, region_name=region_name)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_info_biotypes(species: str = "homo_sapiens"):
    """检索物种的基因和转录本生物类型目录。
    
    生物类型根据基因和转录本的生物学性质对其进行分类，
    例如蛋白质编码、假基因或各种非编码 RNA 类别。
    此信息对于过滤和解释基因组数据至关重要。
    
    Args:
        species: 蛇形命名格式的物种名称（例如，'homo_sapiens' 表示人类）
    
    Query example: {"species": "homo_sapiens"}
    
    Returns:
        字典列表，其中每个字典描述物种的可用生物类型。
    """

    try:
        result = ensembl_api.get_info_biotypes(species=species)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_info_compara_methods():
    """获取 Ensembl Compara 中使用的比较分析方法。
    
    Args:
    
    Query example: {}
    
    Returns:
        包含不同类别比较方法和每个类别中特定方法的字典。
    """

    try:
        result = ensembl_api.get_info_compara_methods()
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_info_external_dbs(species: str):
    """获取物种的外部数据库。
    
    Args:
        species: 物种名称（例如 'homo_sapiens' 表示人类）
    
    Query example: {"species": "homo_sapiens"}
    
    Returns:
        字典列表，其中每个字典包含为物种链接的外部数据库的信息。
    """

    try:
        result = ensembl_api.get_info_external_dbs(species=species)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

# Mapping endpoints
@mcp.tool()
async def get_map_cdna(id: str, region: str):
    """将 cDNA 坐标映射到基因组坐标。
    
    Args:
        id: 转录本 ID
        region: cDNA 坐标
    
    Query example: {"id": "ENST00000380152", "region": "100..300"}
    
    Returns:
        包含坐标映射结果列表的字典，其中每个结果提供输入 cDNA 区域片段的基因组坐标（染色体、起始、结束、链）。
    """

    try:
        result = ensembl_api.get_map_cdna(id=id, region=region)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_map_cds(id: str, region: str):
    """将 CDS 坐标映射到基因组坐标。
    
    Args:
        id: 转录本 ID
        region: CDS 坐标
    
    Query example: {"id": "ENST00000139618", "region": "1..200"}
    
    Returns:
        包含坐标映射结果列表的字典，其中每个结果提供输入 CDS 区域片段的基因组坐标（染色体、起始、结束、链）。
    """

    try:
        result = ensembl_api.get_map_cds(id=id, region=region)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_map_translation(id: str, region: str):
    """将蛋白质坐标映射到基因组坐标。
    
    Args:
        id: 翻译 ID
        region: 蛋白质坐标
    
    Query example: {"id": "ENSP00000265436", "region": "1..50"}
    
    Returns:
        包含坐标映射结果列表的字典，其中每个结果提供输入蛋白质区域片段的基因组坐标（染色体、起始、结束、链）。
    """

    try:
        result = ensembl_api.get_map_translation(id=id, region=region)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

# Ontologies and Taxonomy endpoints
@mcp.tool()
async def get_ontology_ancestors(id: str):
    """获取本体祖先。注意：此工具对输入 ID 的格式敏感，对于某些看起来有效的 ID 可能返回 400 错误请求错误。建议使用直接从其他 Ensembl 工具获得的 ID。
    
    Args:
        id: 本体术语标识符（GO 术语 ID，如 'GO:0005667'）。
    
    Query example: {"id": "GO:0005667"}
    
    Returns:
        字典列表，其中每个字典包含祖先本体术语的信息。
    """

    try:
        result = ensembl_api.get_ontology_ancestors(id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_ontology_descendants(id: str):
    """获取本体后代。注意：此工具对输入 ID 的格式敏感，对于某些看起来有效的 ID 可能返回 400 错误请求错误。建议使用直接从其他 Ensembl 工具获得的 ID。
    
    Args:
        id: 本体术语 ID（例如，GO 术语 ID，如 'GO:0005667'）。
    
    Query example: {"id": "GO:0005667"}
    
    Returns:
        字典列表，其中每个字典包含后代本体术语的信息。
    """

    try:
        result = ensembl_api.get_ontology_descendants(id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_ontology_id(id: str):
    """通过 ID 获取本体。注意：此工具对输入 ID 的格式敏感，对于某些看起来有效的 ID 可能返回 400 错误请求错误。建议使用直接从其他 Ensembl 工具获得的 ID。
    
    Args:
        id: 本体术语标识符（GO 术语 ID，如 'GO:0005667'）。
    
    Query example: {"id": "GO:0005667"}
    
    Returns:
        包含指定术语本体信息的字典，包括其在层次结构中的子项和父项。
    """

    try:
        result = ensembl_api.get_ontology_id(id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_ontology_name(name: str):
    """通过名称获取本体。
    
    Args:
        name: 本体名称。支持 SQL 通配符。
    
    Query example: {"name": "transcription factor complex"}
    
    Returns:
        包含匹配术语本体信息的字典。
    """

    try:
        result = ensembl_api.get_ontology_name(name=name)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

# Overlap endpoints
@mcp.tool()
async def get_overlap_id(id: str):
    """获取与标识符定义的区域重叠的特征。注意：此工具当前无法正常工作，对于有效的 Ensembl ID 返回 400 错误请求错误。
    
    Args:
        id: Ensembl 稳定标识符
    
    Query example: {"id": "ENST00000380152"}
    
    Returns:
        包含重叠特征的字典。失败时返回错误消息。
    """

    try:
        result = ensembl_api.get_overlap_id(id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_overlap_region(features:str, region: str, species: str = "homo_sapiens"):
    """获取与基因组区域重叠的特征。注意：此工具对于有效查询可能失败并返回 400 错误请求错误。
    
    Args:
        features: 要检索的特征类型。如果用逗号分隔，则接受多个值（例如 'feature=gene;feature=transcript;'）。枚举(band, gene, transcript, cds, exon, repeat, simple, misc, variation, somatic_variation, structural_variation, somatic_structural_variation, constrained, regulatory, motif, mane)
        species: 物种名称（例如 'homo_sapiens' 表示人类）
        region: 基因组区域（例如 'X:1..1000:1','X:1..1000:-1','X:1..1000'）
    
    Query example: {"species": "homo_sapiens", "region": "X:1000000..1000100", "features": "gene"}
    
    Returns:
        包含重叠特征的字典。失败时返回错误消息。
    """

    try:
        result = ensembl_api.get_overlap_region(features=features,species=species, region=region)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_overlap_translation(id: str):
    """获取与翻译重叠的特征。
    
    Args:
        id: 翻译稳定标识符
    
    Query example: {"id": "ENSP00000265436"}
    
    Returns:
        字典列表，其中每个字典包含与指定翻译 ID 基因组区域重叠的特征信息。
    """

    try:
        result = ensembl_api.get_overlap_translation(id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

# Phenotype endpoints
@mcp.tool()
async def get_phenotype_region(region: str, species: str = "homo_sapiens", max_length: int = DEFAULT_MAX_LENGTH):
    """检索基因组区域中变异的表型关联。
    
    查找与位于特定基因组区域内的遗传变异相关的疾病、性状和表型。
    对于探索 GWAS 位点或候选区域中的疾病关联很有用。
    
    Args:
        species: 蛇形命名格式的物种名称（例如，'homo_sapiens' 表示人类）
        region: 基因组区域，格式为 'chromosome:start..end'
                （例如，'9:22125500..22136000'、'17:7669000..7676000'）
    
    Query example: {"species": "homo_sapiens", "region": "9:22125500..22136000"}
    
    Returns:
        包含区域中变异表型注释的字典列表，包括：
        - 相关疾病和性状
        - 特定变异位置和等位基因
        - 关联来源（例如 ClinVar、GWAS Catalog）
    """

    result = ensembl_api.get_phenotype_region(species=species, region=region, max_length=max_length)
    if "error" in result:
        return {"error": f"An error occurred while fetching phenotype data: {result['error']}"}
    return result

@mcp.tool()
async def get_phenotype_gene(gene: str, species: str = "homo_sapiens", max_length: int = DEFAULT_MAX_LENGTH):
    """检索特定基因的表型关联。
    
    查找与感兴趣基因相关的疾病、性状和表型。
    这些关联来自各种来源，包括文献整理、GWAS 研究和临床数据库。
    
    Args:
        species: 蛇形命名格式的物种名称（例如，'homo_sapiens' 表示人类）
        gene: 基因稳定 ID 或名称（例如，'ENSG00000139618'、'BRCA2'）
        max_length: 响应的最大长度（以近似令牌数计，默认：8192）
    
    Query example: {"species": "homo_sapiens", "gene": "BRCA2"}
    
    Returns:
        包含基因表型注释的字典列表，包括：
        - 相关疾病和性状
        - 关联来源（例如 ClinVar、GWAS Catalog）
        - 研究参考文献和引用
        - 遗传关联的变异详细信息
        - 可用时的临床意义
    """

    result = ensembl_api.get_phenotype_gene(species=species, gene=gene, max_length=max_length)
    if "error" in result:
        return {"error": f"An error occurred while fetching phenotype data: {result['error']}"}
    return result

@mcp.tool()
async def get_phenotype_accession(accession: str, species: str = "homo_sapiens", max_length: int = DEFAULT_MAX_LENGTH):
    """检索与特定表型本体术语相关的基因组特征。
    
    查找与通过本体登录号标识的特定疾病或性状相关的基因和变异（例如，来自人类表型本体或实验因子本体）。
    
    Args:
        species: 蛇形命名格式的物种名称（例如，'homo_sapiens' 表示人类）
        accession: 表型本体登录号（例如，'HP:0001250' 表示癫痫发作）
        max_length: 响应的最大长度（以近似令牌数计，默认：8192）
    
    Query example: {"species": "homo_sapiens", "accession": "HP:0001250"}
    
    Returns:
        包含基因表型注释的字典列表，包括：
        - 相关疾病和性状
        - 关联来源（例如 ClinVar、GWAS Catalog）
        - 研究参考文献和引用
        - 遗传关联的变异详细信息
    """

    result = ensembl_api.get_phenotype_accession(species=species, accession=accession, max_length=max_length)
    if "error" in result:
        return {"error": f"An error occurred while fetching phenotype data: {result['error']}"}
    return result

# Sequence endpoints
@mcp.tool()
async def get_sequence_id(id: str):
    """检索与 Ensembl 标识符关联的序列。
    
    获取基因或转录本的核苷酸序列，或蛋白质的氨基酸序列。
    对于分析基因结构、转录本变体或蛋白质结构域很有用。
    
    Args:
        id: Ensembl 稳定标识符（例如，'ENSG00000139618' 表示 BRCA2 基因 DNA、
            'ENST00000380152' 表示转录本序列，或 'ENSP00000369497' 表示蛋白质序列）
    
    Query example: {"id": "ENST00000380152"}
    
    Returns:
        包含序列（核苷酸或氨基酸）和实体元数据的字典，包括长度、序列类型和坐标信息。
    """

    try:
        result = ensembl_api.get_sequence_id(id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

# VEP endpoints
@mcp.tool()
async def get_vep_id(id: str, species: str = "homo_sapiens"):
    """使用变异效应预测器（VEP）和变异标识符预测变异的功能效应。
    
    使用已知变异 ID（例如 dbSNP rs 标识符）检索全面的变异注释。
    提供分子后果、群体频率和致病性预测。
    
    Args:
        species: 蛇形命名格式的物种名称（例如，'homo_sapiens' 表示人类）
        id: 变异标识符（例如，'rs6025' 表示因子 V Leiden，'rs429358' 表示 APOE 变异）
    
    Query example: {"species": "homo_sapiens", "id": "rs6025"}
    
    Returns:
        包含详细变异效应预测的字典，包括：
        - 受影响的基因和转录本
        - 对蛋白质序列的影响（错义、无义等）
        - SIFT 和 PolyPhen 致病性评分
        - 保守性评分
        - 群体数据库中的等位基因频率
        - 调控特征注释
        - 临床意义注释
    """

    try:
        result = ensembl_api.get_vep_id(species=species, id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_vep_region(region: str, allele: str, species: str = "homo_sapiens"):
    """使用变异效应预测器（VEP）和基因组坐标预测变异的功能效应。
    
    分析由染色体位置和替代等位基因指定的变异。
    对于新变异或没有已建立标识符的变异特别有用。

    Args:
        species: 蛇形命名格式的物种名称（例如，'homo_sapiens' 表示人类）
        region: 基因组区域，格式为 'chromosome:position' 或 'chromosome:start-end'
                （例如，'9:22125503'、'1:230710048-230710048'）
        allele: 替换参考序列的变异等位基因序列（替代等位基因）

    Returns:
        包含详细变异效应预测的字典，包括：
        - 受影响的基因和转录本
        - 对蛋白质序列的影响（错义、无义等）
        - SIFT 和 PolyPhen 致病性评分
        - 保守性评分
        - 群体数据库中的等位基因频率
        - 调控特征注释
        - 临床意义注释
    """
    try:
        result = ensembl_api.get_vep_region(species=species, region=region, allele=allele)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

# Variation endpoints
@mcp.tool()
async def get_variation(id: str, species: str = "homo_sapiens"):
    """通过标识符检索遗传变异的详细信息。
    
    提供有关已知遗传变异的全面数据，包括其基因组位置、等位基因、群体频率、表型关联以及外部数据库的链接。
    
    Args:
        species: 蛇形命名格式的物种名称（例如，'homo_sapiens' 表示人类）
        id: 变异标识符（例如，'rs6025' 表示因子 V Leiden，'rs429358' 表示 APOE 变异）
    
    Query example: {"species": "homo_sapiens", "id": "rs6025"}
    
    Returns:
        包含详细变异信息的字典，包括：
        - 基因组位置和等位基因
        - 不同群体的群体频率
        - 临床意义和表型关联
        - 转录本的后果预测
        - 引用和参考文献
        - 外部数据库链接（dbSNP、ClinVar 等）
    """

    try:
        result = ensembl_api.get_variation(species=species, id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_variant_recoder(id: str, species: str = "homo_sapiens"):
    """在不同变异命名系统和表示之间进行转换。
    
    在不同格式之间转换变异标识符（例如 rsID、HGVS 表示法、基因组坐标）。
    对于整合来自不同来源或分析工具的变异数据很有用。
    
    Args:
        species: 蛇形命名格式的物种名称（例如，'homo_sapiens' 表示人类）
        id: 任何支持格式的变异标识符（例如，'rs6025'、
            'ENST00000367640.3:c.1601G>A'、'1:g.169519049G>T'）
    
    Query example: {"species": "homo_sapiens", "id": "rs6025"}
    
    Returns:
        包含以各种命名系统表示的变异的字典：
        - dbSNP rsID
        - HGVS 表示法（基因组、转录本、蛋白质）
        - VCF 格式的基因组坐标
        - SPDI 表示法（序列位置删除插入）
    """

    try:
        result = ensembl_api.get_variant_recoder(species=species, id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

# Additional Information endpoints
@mcp.tool()
async def get_info_data():
    """获取数据发布信息。
    
    Query example: {}

    Returns:
        包含数据发布信息的字典。
    """
    try:
        result = ensembl_api.get_info_data()
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_info_eg_version():
    """获取 Ensembl Genomes 版本。
    
    Args:
    
    Query example: {}
    
    Returns:
        包含版本信息的字典。
    """

    try:
        result = ensembl_api.get_info_eg_version()
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_info_divisions():
    """获取 Ensembl 分区。
    
    Args:
    
    Query example: {}
    
    Returns:
        包含主要 Ensembl 分区名称的列表。
    """

    try:
        result = ensembl_api.get_info_divisions()
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_info_genomes(genome_name: str):
    """查找有关给定基因组的信息。
    
    Args:
        genome_name: 基因组名称（例如，'homo_sapiens'）
    
    Query example: {"genome_name": "homo_sapiens"}
    
    Returns:
        包含详细基因组信息的字典。
    """

    try:
        result = ensembl_api.get_info_genomes(genome_name=genome_name)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_info_genomes_accession(accession: str):
    """查找包含指定 INSDC 登录号的基因组信息。注意：底层数据稀疏，许多有效的登录号可能导致返回 null。
    
    Args:
        accession: INSDC 登录号（例如，'GCA_000001635.9'）。
    
    Query example: {"accession": "GCA_000001635.9"}
    
    Returns:
        包含指定登录号基因组信息的字典。如果未找到信息则返回 null。
    """

    try:
        result = ensembl_api.get_info_genomes_accession(accession=accession)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_info_genomes_assembly(assembly_id: str):
    """查找具有指定组装的基因组信息。注意：此工具对于有效的组装 ID 可能失败并返回 400 错误请求错误。
    
    Args:
        assembly_id: 组装标识符
    
    Query example: {"assembly_id": "71511"}
    
    Returns:
        包含基因组信息的字典。失败时返回错误消息。
    """

    try:
        result = ensembl_api.get_info_genomes_assembly(assembly_id=assembly_id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_info_genomes_division(division_name: str):
    """查找给定分区中所有基因组的信息。
    
    Args:
        division_name: 分区名称（例如，'EnsemblVertebrates'）
    
    Query example: {"division_name": "EnsemblVertebrates"}
    
    Returns:
        字典列表，其中每个字典包含指定分区中基因组的信息。
    """

    try:
        result = ensembl_api.get_info_genomes_division(division_name=division_name)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_info_genomes_taxonomy(taxon_name: str):
    """查找分类学给定节点下所有基因组的信息。
    
    Args:
        taxon_name: 分类单元名称（例如，'Primates'）
    
    Query example: {"taxon_name": "Primates"}
    
    Returns:
        JSON 字符串列表，其中每个字符串是包含指定分类单元内物种基因组信息的字典。
    """

    try:
        result = ensembl_api.get_info_genomes_taxonomy(taxon_name=taxon_name)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_info_ping():
    """检查服务是否存活。
    
    Args:
    
    Query example: {}
    
    Returns:
        包含 ping 状态的字典（1 表示存活）。
    """

    try:
        result = ensembl_api.get_info_ping()
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_info_rest():
    """显示 Ensembl REST API 的当前版本。
    
    Args:
    
    Query example: {}
    
    Returns:
        包含 REST API 版本信息的字典。
    """

    try:
        result = ensembl_api.get_info_rest()
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_info_software():
    """显示 REST 服务器使用的 Ensembl API 的当前版本。
    
    Args:
    
    Query example: {}
    
    Returns:
        包含软件版本信息的字典。
    """

    try:
        result = ensembl_api.get_info_software()
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_info_species():
    """列出 Ensembl 数据库中所有可用的物种。
    
    提供 Ensembl 中所有可用生物的全面目录，包括其学名、俗名和组装信息。
    对于发现和探索可用的基因组数据很有用。
    
    Args:
    
    Query example: {}
    
    Returns:
        字典列表，其中每个字典包含可用物种的信息。
    """

    try:
        result = ensembl_api.get_info_species()
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_info_variation(species: str):
    """列出 Ensembl 中用于物种的所有变异数据源。
    
    提供有关为物种向 Ensembl 贡献变异数据（SNP、插入缺失、结构变异）的数据库、研究和项目的信息。
    
    Args:
        species: 蛇形命名格式的物种名称（例如，'homo_sapiens' 表示人类）
    
    Query example: {"species": "homo_sapiens"}
    
    Returns:
        字典列表，其中每个字典包含物种变异数据源的信息。
    """

    try:
        result = ensembl_api.get_info_variation(species=species)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_info_variation_consequence_types():
    """列出 Ensembl 使用的所有变异后果类型。
    
    Args:
    
    Query example: {}
    
    Returns:
        JSON 字符串列表，其中每个字符串是包含变异后果类型信息的字典。
    """

    try:
        result = ensembl_api.get_info_variation_consequence_types()
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_info_variation_populations(species: str, population_name: str = None):
    """列出物种的所有变异群体，或列出特定群体中的所有个体。
    
    Args:
        species: 物种名称（例如，'homo_sapiens' 表示人类）。
        population_name: 可选的群体名称以获取个体。如果未提供，则返回物种的所有群体。
    
    Query example for all populations: {"species": "homo_sapiens"}
    Query example for individuals in a population: {"species": "homo_sapiens", "population_name": "1000GENOMES:phase_3:ACB"}
    
    Returns:
        包含群体信息的字典列表，或特定群体的个体信息字典。
    """

    try:
        result = ensembl_api.get_info_variation_populations(species=species, population_name=population_name)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

# Linkage Disequilibrium endpoints
@mcp.tool()
async def get_ld(species: str, id: str, population_name: str):
    """计算并返回给定变异与窗口中所有其他变异之间的 LD 值。
    
    Args:
        species: 物种名称（例如 'homo_sapiens' 表示人类）
        id: 变异标识符
        population_name: 群体名称
    
    Query example: {"species": "homo_sapiens", "id": "rs6025", "population_name": "1000GENOMES:phase_3:EUR"}
    
    Returns:
        JSON 字符串列表，其中每个字符串是包含查询变异与另一个附近变异之间 LD 值（d_prime、r2）的字典。
    """

    try:
        result = ensembl_api.get_ld(species=species, id=id, population_name=population_name)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_ld_pairwise(species: str, id1: str, id2: str):
    """计算并返回给定变异之间的 LD 值。
    
    Args:
        species: 物种名称（例如 'homo_sapiens' 表示人类）
        id1: 第一个变异标识符
        id2: 第二个变异标识符
    
    Query example: {"species": "homo_sapiens", "id1": "rs6025", "id2": "rs2213868"}
    
    Returns:
        JSON 字符串列表，其中每个字符串是包含特定群体中变异对 LD 值的字典。
    """

    try:
        result = ensembl_api.get_ld_pairwise(species=species, id1=id1, id2=id2)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_ld_region(species: str, region: str, population_name: str):
    """计算并返回定义区域中所有变异对之间的 LD 值。
    
    Args:
        species: 物种名称（例如 'homo_sapiens' 表示人类）
        region: 基因组区域
        population_name: 群体名称
    
    Query example: {"species": "homo_sapiens", "region": "1:169549800-169549900", "population_name": "1000GENOMES:phase_3:EUR"}
    
    Returns:
        JSON 字符串列表，其中每个字符串是包含指定区域和群体内变异对 LD 值的字典。
        如果在区域中未找到具有 LD 数据的变异对，则可能返回空列表。
    """

    try:
        result = ensembl_api.get_ld_region(species=species, region=region, population_name=population_name)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

# Lookup endpoints
@mcp.tool()
async def get_lookup_id(id: str):
    """查找任何 Ensembl 稳定标识符的详细信息。
    
    使用其稳定标识符检索有关任何 Ensembl 实体（基因、转录本、蛋白质等）的全面信息。
    
    Args:
        id: Ensembl 稳定标识符（例如，'ENSG00000139618' 表示人类 BRCA2 基因、
            'ENST00000380152' 表示转录本，或 'ENSP00000369497' 表示蛋白质）
    
    Query example: {"id": "ENSG00000139618"}
    
    Returns:
        包含实体详细信息的字典，包括其类型、位置、与其他实体的关系以及交叉引用。
    """

    try:
        result = ensembl_api.get_lookup_id(id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def post_lookup_id(ids: list[str]):
    """在单个请求中查找多个 Ensembl 稳定标识符的详细信息。
    
    批量检索多个 Ensembl 实体（基因、转录本、蛋白质等）的信息。
    
    Args:
        ids: Ensembl 稳定标识符列表（例如，['ENSG00000139618', 'ENSG00000141510']
            表示人类 BRCA2 和 TP53 基因）
    
    Returns:
        将每个输入 ID 映射到其对应实体信息的字典。
        未找到的标识符将从结果中排除。
    
    Query example: {"ids": ["ENSG00000157764", "ENSG00000248378"]}
    """

    try:
        result = ensembl_api.post_lookup_id(ids=ids)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def post_lookup_symbol(symbols: list[str], species: str = "homo_sapiens"):
    """在单个请求中查找多个基因符号。
    
    批量检索多个外部基因符号的 Ensembl 基因信息。
    
    Args:
        species: 蛇形命名格式的物种名称（例如，'homo_sapiens' 表示人类）
        symbols: 官方基因符号列表（例如，['BRCA2', 'TP53', 'APOE']）
    
    Returns:
        将每个输入符号映射到其对应基因信息的字典。
        未找到的符号将从结果中排除。
    
    Query example: {"species": "homo_sapiens", "symbols": ["BRCA2"]}
    """

    try:
        result = ensembl_api.post_lookup_symbol(species=species, symbols=symbols)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

# Mapping endpoints
@mcp.tool()
async def get_map(asm_one: str, region: str, asm_two: str, species: str = "homo_sapiens"):
    """在组装之间映射坐标。

    Args:
        species: 物种名称（例如 'homo_sapiens' 表示人类）
        asm_one: 源组装
        region: 源组装中的基因组区域
        asm_two: 目标组装

    Returns:
        包含映射坐标的字典。
    """
    try:
        result = ensembl_api.get_map(species=species, asm_one=asm_one, region=region, asm_two=asm_two)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

# Ontology endpoints
@mcp.tool()
async def get_ontology_ancestors_chart(id: str):
    """从 is_a 和 part_of 关系重建术语的整个祖先。
    
    Args:
        id: 本体术语 ID
    
    Returns:
        包含祖先图表信息的字典。
    
    Query example: {"id": "GO:0005667"}
    """

    try:
        result = ensembl_api.get_ontology_ancestors_chart(id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

# Taxonomy endpoints
@mcp.tool()
async def get_taxonomy_classification(id: str):
    """返回分类单元节点的分类学分类。
    
    Args:
        id: 分类学 ID
    
    Returns:
        包含分类学分类的字典。
    
    Query example: {"id": "9606"}
    """

    try:
        result = ensembl_api.get_taxonomy_classification(id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_taxonomy_id(id: str):
    """通过标识符或名称搜索分类学术语。
    
    Args:
        id: 分类学 ID 或名称
    
    Returns:
        包含分类学信息的字典。
    
    Query example: {"id": "9606"}
    """

    try:
        result = ensembl_api.get_taxonomy_id(id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_taxonomy_name(name: str):
    """通过非科学名称搜索分类学 id。
    
    Args:
        name: 非科学名称
    
    Returns:
        包含分类学信息的字典。
    
    Query example: {"name": "Homo sapiens"}
    """

    try:
        result = ensembl_api.get_taxonomy_name(name=name)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

# Regulation endpoints
@mcp.tool()
async def get_species_binding_matrix(binding_matrix_stable_id: str, species: str = "homo_sapiens"):
    """返回指定的结合矩阵。
    
    Args:
        species: 物种名称（例如 'homo_sapiens' 表示人类）
        binding_matrix_stable_id: 结合矩阵稳定 ID
    
    Returns:
        包含结合矩阵信息的字典。
    
    Query example: {"species": "homo_sapiens", "binding_matrix_stable_id": "ENSPFM0001"}
    """

    try:
        result = ensembl_api.get_species_binding_matrix(species=species, binding_matrix_stable_id=binding_matrix_stable_id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

# Sequence endpoints
@mcp.tool()
async def post_sequence_id(ids: list[str]):
    """通过稳定标识符列表请求多种类型的序列。
    
    在单个请求中高效获取多个基因、转录本或蛋白质的序列。
    
    Args:
        ids: Ensembl 稳定标识符列表（例如，['ENSG00000139618', 'ENSG00000141510']）
    
    Returns:
        将每个标识符映射到其对应序列和元数据的字典。
    
    Query example: {"ids": ["ENSG00000157764", "ENSG00000248378"]}
    """

    try:
        result = ensembl_api.post_sequence_id(ids=ids)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def post_sequence_region(regions: list[dict], species: str = "homo_sapiens"):
    """通过多个区域获取序列。

    Args:
        species: 物种名称（例如 'homo_sapiens' 表示人类）
        regions: 基因组区域列表

    Returns:
        包含序列的字典。
    """
    try:
        result = ensembl_api.post_sequence_region(species=species, regions=regions)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

# Transcript Haplotypes endpoints
@mcp.tool()
async def get_transcript_haplotypes(id: str, species: str = "homo_sapiens"):
    """基于分阶段基因型数据计算观察到的转录本单倍型序列。
    
    Args:
        species: 物种名称（例如 'homo_sapiens' 表示人类）
        id: 转录本 ID
    
    Returns:
        包含转录本单倍型信息的字典。
    
    Query example: {"species": "homo_sapiens", "id": "ENST00000288602"}
    """

    try:
        result = ensembl_api.get_transcript_haplotypes(species=species, id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

# VEP endpoints
@mcp.tool()
async def post_vep_hgvs(hgvs_notations: list[str], species: str = "homo_sapiens"):
    """使用 VEP 和 HGVS 表示法批量预测多个变异的功能效应。
    
    在单个请求中使用变异效应预测器高效分析多个变异。
    非常适合分析来自测序数据或遗传研究的变异集。
    
    Args:
        species: 蛇形命名格式的物种名称（例如，'homo_sapiens' 表示人类）
        hgvs_notations: HGVS 表示法格式的变异列表
                        （例如，['ENST00000269305.4:c.2309C>T', 'NM_000059.3:c.274G>A']）
    
    Returns:
        字典列表，每个字典包含一个输入变异的详细变异效应预测。
    
    Query example: {"species": "human", "hgvs_notations": ["ENST00000366667:c.803C>T", "9:g.22125504G>C"]}
    """

    try:
        result = ensembl_api.post_vep_hgvs(species=species, hgvs_notations=hgvs_notations)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def post_vep_id(ids: list[str], species: str = "homo_sapiens"):
    """使用 VEP 和变异标识符批量预测多个变异的功能效应。
    
    在单个请求中使用变异效应预测器高效分析多个已知变异。
    非常适合分析常见变异集或 SNP 面板数据。
    
    Args:
        species: 蛇形命名格式的物种名称（例如，'homo_sapiens' 表示人类）
        ids: 变异标识符列表（例如，['rs6025', 'rs429358']）
    
    Returns:
        字典列表，每个字典包含一个输入变异的详细变异效应预测。
    
    Query example: {"species": "human", "ids": ["rs56116432", "COSM476", "__VAR(sv_id)__"]}
    """

    try:
        result = ensembl_api.post_vep_id(species=species, ids=ids)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def post_vep_region(variants: list[dict], species: str = "homo_sapiens"):
    """通过多个区域获取变异效应预测。

    Args:
        species: 物种名称（例如 'homo_sapiens' 表示人类）
        variants: 变异定义列表

    Returns:
        包含变异效应预测的字典。
    """
    try:
        result = ensembl_api.post_vep_region(species=species, variants=variants)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

# Variation endpoints
@mcp.tool()
async def post_variant_recoder(ids: list[str], species: str = "homo_sapiens"):
    """将变异标识符、HGVS 表示法或基因组 SPDI 表示法列表转换为所有可能的变异 ID、HGVS 和基因组 SPDI。
    
    Args:
        species: 物种名称（例如 'homo_sapiens' 表示人类）
        ids: 变异标识符列表
    
    Returns:
        包含变异标识符转换的字典。
    
    Query example: {"species": "human", "ids": ["rs56116432", "rs1042779"]}
    """

    try:
        result = ensembl_api.post_variant_recoder(species=species, ids=ids)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_variation_pmcid(pmcid: str, species: str = "homo_sapiens"):
    """使用 PubMed Central 参考编号（PMCID）通过出版物获取变异。
    
    Args:
        species: 物种名称（例如 'homo_sapiens' 表示人类）
        pmcid: PubMed Central 参考编号
    
    Returns:
        包含变异信息的字典。
    
    Query example: {"species": "human", "pmcid": "PMC5002951"}
    """

    try:
        result = ensembl_api.get_variation_pmcid(species=species, pmcid=pmcid)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_variation_pmid(pmid: str, species: str = "homo_sapiens"):
    """使用 PubMed 参考编号（PMID）通过出版物获取变异。
    
    Args:
        species: 物种名称（例如 'homo_sapiens' 表示人类）
        pmid: PubMed 参考编号
    
    Returns:
        包含变异信息的字典。
    
    Query example: {"species": "human", "pmid": "26318936"}
    """

    try:
        result = ensembl_api.get_variation_pmid(species=species, pmid=pmid)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def post_variation(ids: list[str], species: str = "homo_sapiens"):
    """使用变异标识符列表（例如 rsID）返回变异特征，包括可选的基因型、表型和群体数据。
    
    Args:
        species: 物种名称（例如 'homo_sapiens' 表示人类）
        ids: 变异标识符列表
    
    Returns:
        包含变异信息的字典。
    
    Query example: {"species": "human", "ids": ["rs56116432", "COSM476", "__VAR(sv_id)__"]}
    """

    try:
        result = ensembl_api.post_variation(species=species, ids=ids)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

# GA4GH endpoints
@mcp.tool()
async def get_ga4gh_beacon():
    """获取 Beacon 信息。
    
    Returns:
        包含 Beacon 信息的字典。
    
    Args:None
    
    Query example:{}
    """

    try:
        result = ensembl_api.get_ga4gh_beacon()
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_ga4gh_beacon_query(params: dict):
    """查询 Beacon。

    Args:
        params: 查询参数

    Returns:
        包含 Beacon 响应的字典。
    """
    try:
        result = ensembl_api.get_ga4gh_beacon_query(params=params)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def post_ga4gh_beacon_query(data: dict):
    """使用 POST 查询 Beacon。

    Args:
        data: 查询数据

    Returns:
        包含 Beacon 响应的字典。
    """
    try:
        result = ensembl_api.post_ga4gh_beacon_query(data=data)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_ga4gh_features(id: str):
    """通过 ID 获取 GA4GH 特征。

    Args:
        id: 特征标识符

    Returns:
        包含特征信息的字典。
    """
    try:
        result = ensembl_api.get_ga4gh_features(id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def post_ga4gh_features_search(data: dict):
    """以 GA4GH 格式获取序列注释特征列表。
    
    Args:
        data: 搜索参数
    
    Returns:
        包含特征信息的字典。
    
    Query example: {"data": {"parentId": "ENST00000408937.7", "pageSize": 2, "featureSetId": "", "featureTypes": ["cds"], "start": 197859, "end": 220023, "referenceName": "X"}}
    """

    try:
        result = ensembl_api.post_ga4gh_features_search(data=data)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def post_ga4gh_callsets_search(data: dict):
    """搜索 GA4GH callsets。
    
    Args:
        data: 搜索参数
    
    Returns:
        包含 callset 信息的字典。
    
    Query example: {"data": {"variantSetId": 1, "pageSize": 3, "name": "HG00099"}}
    """

    try:
        result = ensembl_api.post_ga4gh_callsets_search(data=data)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_ga4gh_callsets(id: str):
    """根据标识符获取特定 CallSet 的 GA4GH 记录。
    
    Args:
        id: Callset 标识符
    
    Returns:
        包含 callset 信息的字典。
    
    Query example: {"id": "1:NA19777"}
    """

    try:
        result = ensembl_api.get_ga4gh_callsets(id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def post_ga4gh_datasets_search(data: dict):
    """以 GA4GH 格式获取数据集列表。
    
    Args:
        data: 搜索参数
    
    Returns:
        包含数据集信息的字典。
    
    Query example: {"data": {}}
    """

    try:
        result = ensembl_api.post_ga4gh_datasets_search(data=data)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_ga4gh_datasets(id: str):
    """根据标识符获取特定数据集的 GA4GH 记录。
    
    Args:
        id: 数据集标识符
    
    Returns:
        包含数据集信息的字典。
    
    Query example: {"id": "6e340c4d1e333c7a676b1710d2e3953c"}
    """

    try:
        result = ensembl_api.get_ga4gh_datasets(id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def post_ga4gh_featuresets_search(data: dict):
    """搜索 GA4GH 特征集。
    
    Args:
        data: 搜索参数
    
    Returns:
        包含特征集信息的字典。
    
    Query example: {"data": {"datasetId": "Ensembl", "pageToken": "", "pageSize": 2}}
    """

    try:
        result = ensembl_api.post_ga4gh_featuresets_search(data=data)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_ga4gh_featuresets(id: str):
    """根据标识符返回特定 featureSet 的 GA4GH 记录。
    
    Args:
        id: 特征集标识符
    
    Returns:
        包含特征集信息的字典。
    
    Query example: {"id": "Ensembl.114.GRCh38"}
    """

    try:
        result = ensembl_api.get_ga4gh_featuresets(id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_ga4gh_variants(id: str):
    """通过 ID 获取 GA4GH 变异。
    
    Args:
        id: 变异标识符
    
    Returns:
        包含变异信息的字典。
    
    Query example: {"id": "1:rs1333049"}
    """

    try:
        result = ensembl_api.get_ga4gh_variants(id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def post_ga4gh_variantannotations_search(data: dict):
    """以 GA4GH 格式返回参考序列上区域的变异注释信息。
    
    Args:
        data: 搜索参数
    
    Returns:
        包含变异注释信息的字典。
    
    Query example: {"data": {"pageSize": 2, "variantAnnotationSetId": "Ensembl", "referenceId": "9489ae7581e14efcad134f02afafe26c", "start": 25221400, "end": 25221500}}
    """

    try:
        result = ensembl_api.post_ga4gh_variantannotations_search(data=data)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def post_ga4gh_variants_search(data: dict):
    """以 GA4GH 格式返回参考序列上区域的变异调用信息。
    
    Args:
        data: 搜索参数
    
    Returns:
        包含变异信息的字典。
    
    Query example: {"data": {"variantSetId": 1, "callSetIds": ["1:NA19777", "1:HG01242", "1:HG01142"], "referenceName": 22, "start": 17190024, "end": 17671934, "pageToken": "", "pageSize": 3}}
    """

    try:
        result = ensembl_api.post_ga4gh_variants_search(data=data)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def post_ga4gh_variantsets_search(data: dict):
    """搜索 GA4GH 变异集。
    
    Args:
        data: 搜索参数
    
    Returns:
        包含变异集信息的字典。
    
    Query example: {"data": {"datasetId": "6e340c4d1e333c7a676b1710d2e3953c", "pageToken": "", "pageSize": 2}}
    """

    try:
        result = ensembl_api.post_ga4gh_variantsets_search(data=data)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_ga4gh_variantsets(id: str):
    """根据标识符返回特定 VariantSet 的 GA4GH 记录。
    
    Args:
        id: 变异集标识符
    
    Returns:
        包含变异集信息的字典。
    
    Query example: {"id": "1"}
    """

    try:
        result = ensembl_api.get_ga4gh_variantsets(id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def post_ga4gh_references_search(data: dict):
    """以 GA4GH 格式返回参考序列列表。
    
    Args:
        data: 搜索参数
    
    Returns:
        包含参考信息的字典。
    
    Args:
        data: 数据（对象）
    
    Query example: {"data": {"referenceSetId": "GRCh38", "pageSize": 10}}
    """

    try:
        result = ensembl_api.post_ga4gh_references_search(data=data)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_ga4gh_references(id: str):
    """通过 id 以 GA4GH 格式返回特定参考的数据。
    
    Args:
        id: 参考标识符
    
    Returns:
        包含参考信息的字典。
        
    Query example: {"id": "9489ae7581e14efcad134f02afafe26c"}
    """

    try:
        result = ensembl_api.get_ga4gh_references(id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def post_ga4gh_referencesets_search(data: dict):
    """搜索 GA4GH 参考集。
    
    Args:
        data: 搜索参数
    
    Returns:
        包含以下字段的字典：
        referenceSets:包含所有可用参考基因组集合（数组）
        nextPageToken:分页标记
    
    Args:
        data: 数据（对象）
    
    Query example: {"data": {}}
    """

    try:
        result = ensembl_api.post_ga4gh_referencesets_search(data=data)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_ga4gh_referencesets(id: str):
    """通过 ID 以 GA4GH 格式搜索特定参考集的数据。
    
    Args:
        id: 参考集标识符
    
    Returns:
        包含以下字段的字典：
        id:基因组的唯一标识符（短名称）
        name:人类可读的名称，通常与 id 相同
        assemblyId:官方基因组组装 ID
        ncbiTaxonId:NCBI 物种 ID
        description:基因组描述的全名
    
    Args:
        id: Id（字符串）
    
    Query example: {"id": "GRCh38", "sourceURI": null, "assemblyId": "GRCh38", "isDerived": "true", "ncbiTaxonId": "9606", "sourceAccessions": ["GCA_000001405.18"], "description": "Homo sapiens GRCh38", "name": "GRCh38", "md5checksum": "4c30331c23188932dba64cb1845d18f5"}
    """

    try:
        result = ensembl_api.get_ga4gh_referencesets(id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def post_ga4gh_variantannotationsets_search(data: dict):
    """以 GA4GH 格式返回注释集列表。
    
    Args:
        data: 搜索参数
    
    Returns:
        包含变异注释集信息的字典。
    
    Args:
        data: 数据（对象）
    
    Query example: {"data": {"variantSetId": "Ensembl"}}
    """

    try:
        result = ensembl_api.post_ga4gh_variantannotationsets_search(data=data)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_ga4gh_variantannotationsets(id: str):
    """通过 ID 以 GA4GH 格式返回特定注释集的元数据。
    
      Args:
          id: 变异注释集标识符
    
      Returns:
          包含变异注释集信息的字典。
    
      Query example: {"id": "Ensembl"}
    """

    try:
        result = ensembl_api.get_ga4gh_variantannotationsets(id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_genetree_member_id(id: str, species: str = "homo_sapiens"):
    """检索包含通过 Ensembl ID 标识的基因的基因树。查找显示感兴趣基因进化关系的系统发育树，
    使用其 Ensembl 稳定标识符进行标识。当您拥有特定基因 ID 时，对于理解基因进化很有用。
    
    Args:
        species: 蛇形命名格式的物种名称（例如，'homo_sapiens' 表示人类）
        id: Ensembl 基因、转录本或翻译稳定标识符
            （例如，'ENSG00000139618' 表示人类 BRCA2 基因）
    
    Returns:
        包含嵌套结构基因树信息的字典，包括：
        - 分类学和序列关系
        - 表示进化距离的分支长度
        - 表示树置信度的自举值
        - 用于构建树的序列比对
        - 来自不同物种的成员基因
    
    Query example: {"species": "human", "id": "ENSG00000167664"}
    """

    try:
        result = ensembl_api.get_genetree_member_id(species=species, id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_info_biotypes_groups(group: str, object_type: str):
    """提供 :group 参数时，列出该组内生物类型的属性。可以提供对象类型（基因或转录本）进行过滤。
    
    Args:
        group: 生物类型组
        object_type: 对象类型（基因或转录本）
    
    Returns:
        包含以下字段的字典：
        object_type:表示此生物类型的对象类型
        biotype_group:生物体类型的高级分组，指示基因的功能类别（例如编码、非编码、假基因等）
        name:Ensembl 内部名称
        so_term:基因/转录本生物功能描述的序列本体（SO）标准术语。
        so_acc:对应于序列本体中 so_term 的唯一标识符（登录号）
        
    
    Query example: {"group": "coding", "object_type": "gene"}
    """

    try:
        result = ensembl_api.get_info_biotypes_groups(group=group, object_type=object_type)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_info_biotypes_name(name: str, object_type: str):
    """列出具有给定名称的生物类型的属性。可以提供对象类型（基因或转录本）进行过滤。
    
    Args:
        name: 生物类型名称
        object_type: 对象类型（基因或转录本）
    
    Returns:
        包含以下字段的字典：
        object_type:表示此生物类型的对象类型
        biotype_group:生物体类型的高级分组，指示基因的功能类别（例如编码、非编码、假基因等）
        so_term:基因/转录本生物功能描述的序列本体（SO）标准术语。
        so_acc:对应于序列本体中 so_term 的唯一标识符（登录号）
        name:生物类型的缩写，与 Ensembl 内使用的命名法一致
        
    Query example: {"name": "protein_coding", "object_type": "gene"}
    """

    try:
        result = ensembl_api.get_info_biotypes_name(name=name, object_type=object_type)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_info_compara_species_sets(method: str):
    """列出使用指定比较方法分析的所有物种集合。
    
    Args:
        method: 比较分析方法
    
    Returns:
        包含物种集信息的字典。
    
    Query example: {"method": "EPO"}
    """

    try:
        result = ensembl_api.get_info_compara_species_sets(method=method)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_info_comparas():
    """获取所有可用的比较基因组学数据库及其数据发布。
    
    Args:None
    
    Query example:{}
    
    Returns:
        包含以下字段的字典：
            release: Ensembl Compara 数据库的版本或发布号
            name:数据库中物种组或比较基因组学分析的子组名称
    """

    try:
        result = ensembl_api.get_info_comparas()
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.prompt()
def system_prompt():
    """客户端的系统提示。"""
    prompt = """您可以访问用于查询 Ensembl REST API 的工具。
    使用这些工具获取有关基因、序列、变异等的信息。
    该 API 提供对多个物种基因组数据的访问。
    对于物种名称，使用格式 'homo_sapiens' 表示人类，'mus_musculus' 表示小鼠等。
    对于区域，使用格式 'chromosome:start..end'（例如 'X:1000000..1000100'）。
    对于变异，使用正确的 HGVS 表示法（例如 'ENST00000003084:c.1431_1433delTTC'）。
    """
    return prompt