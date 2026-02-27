from mcp.server.fastmcp import FastMCP

from tools.biodb.STRING.string_api import StringAPI


mcp = FastMCP(
    "string_mcp",
    stateless_http=True,
)
string_api = StringAPI()


@mcp.tool()
async def mapping_identifiers(genes: list[str], species: int):
    """将常见的蛋白质名称、同义词和 UniProt 标识符映射到 STRING 标识符。
    
    Args:
        genes: 基因名称列表，必需（数组）
        species: NCBI/STRING 分类单元编号（整数）
    
    Query example: {"genes": ["TP53", "BRCA1"], "species": 9606}
    
    Returns:
        包含基因 STRING 标识符的字典列表
    """

    try:
        result = string_api.mapping_identifiers(identifiers=genes, species=species)
    except Exception as e:
        return [{"error": f"An error occurred while mapping identifiers: {str(e)}"}]
    return result


@mcp.tool()
async def get_string_network_interaction(
    identifiers: list[str],
    species: int,
    required_score: int,
    add_nodes: int,
    network_type: str,
    show_query_node_labels: int,
):
    """检索一个或多个蛋白质的 STRING 相互作用网络，以各种文本格式呈现。
    它将告诉你该蛋白质集的综合得分以及所有通道特定得分。
    你还可以通过设置 "add_nodes" 来扩展网络邻域，这将按置信度顺序向你的网络添加新的相互作用伙伴。
    
    Args:
        identifiers: 多个项目列表的必需参数（数组）
        species: NCBI/STRING 分类单元编号（例如人类为 9606，或小鼠为 STRG0A10090）（整数）
        required_score: 过滤低质量相互作用，介于 0 和 1000 之间的数字（整数）
        add_nodes: 除初始查询基因外添加的关联基因数量（整数）
        network_type: 网络类型：functional（默认）、physical（字符串）
        show_query_node_labels: 是否在结果中标记查询基因（1 表示是，0 表示否）（整数）
    
    Query example: {"identifiers": ["TP53", "BRCA1"], "species": 9606, "required_score": 700, "add_nodes": 5, "network_type": "physical", "show_query_node_labels": 1}
    
    Returns:
        包含以下字段的字典：
        stringId_A:     STRING 标识符（蛋白质 A）
        stringId_B:     STRING 标识符（蛋白质 B）
        preferredName_A: 常见蛋白质名称（蛋白质 A）
        preferredName_B: 常见蛋白质名称（蛋白质 B）
        ncbiTaxonId: NCBI 分类单元标识符
        score:  综合得分
        nscore: 基因邻域得分
        fscore: 基因融合得分
        pscore: 系统发育谱得分
        ascore: 共表达得分
        escore: 实验得分
        dscore: 数据库得分
        tscore: 文本挖掘得分
    """

    try:
        result = string_api.get_string_network_interaction(
            identifiers=identifiers,
            species=species,
            required_score=required_score,
            add_nodes=add_nodes,
            network_type=network_type,
            show_query_node_labels=show_query_node_labels,
        )
    except Exception as e:
        return [
            {
                "error": f"An error occurred while getting STRING network interaction: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_all_interaction_partners_of_the_protein_set(
    identifiers: list[str],
    species: int,
    limit: int,
    required_score: int,
    network_type: str,
):
    """此方法提供你提供的蛋白质集与所有其他 STRING 蛋白质之间的相互作用。
    由于 STRING 网络通常有很多低得分的相互作用，你可能希望使用 "limit" 参数限制每个蛋白质检索的相互作用伙伴数量。
    
    Args:
        identifiers: 多个项目列表的必需参数
        species: NCBI/STRING 分类单元（例如人类为 9606，或 STRG0AXXXXX）
        limit: 限制每个蛋白质检索的相互作用伙伴数量（最可信的相互作用优先）
        required_score: 包含相互作用的显著性阈值，介于 0 和 1000 之间的数字（默认取决于网络）
        network_type: 网络类型：functional（默认）、physical
        
    Returns:
        包含以下字段的字典：
        stringId_A:     STRING 标识符（蛋白质 A）
        stringId_B:     STRING 标识符（蛋白质 B）
        preferredName_A: 常见蛋白质名称（蛋白质 A）
        preferredName_B: 常见蛋白质名称（蛋白质 B）
        ncbiTaxonId: NCBI 分类单元标识符
        score:  综合得分
        nscore: 基因邻域得分
        fscore: 基因融合得分
        pscore: 系统发育谱得分
        ascore: 共表达得分
        escore: 实验得分
        dscore: 数据库得分
        tscore: 文本挖掘得分
    
    Query example: {"identifiers": ["TP53", "BRCA1"], "species": 9606, "limit": 20, "required_score": 700, "network_type": "physical"}
    """

    try:
        result = string_api.get_all_interaction_partners_of_the_protein_set(
            identifiers=identifiers,
            species=species,
            required_score=required_score,
            limit=limit,
            network_type=network_type,
        )
    except Exception as e:
        return [
            {
                "error": f"An error occurred while getting all interaction partners of the protein set: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_similarity_scores_of_the_protein_set(identifiers: list[str], species: int):
    """STRING 内部使用 Smith-Waterman 比特分数作为蛋白质同源性的代理。
    使用此 API，你可以检索所选物种中蛋白质之间的这些分数。
    它们是对称的，意味着 A->B 等于 B->A。
    我们不存储或报告同源性的比特分数截止值为 50。
    
    Args:
        identifiers: 多个项目列表的必需参数
        species: NCBI/STRING 分类单元（例如人类为 9606，或 STRG0AXXXXX）
        
    Returns:
        包含以下字段的字典：
        ncbiTaxonId_A:  NCBI 分类单元标识符（蛋白质 A）
        stringId_A:     STRING 标识符（蛋白质 A）
        ncbiTaxonId_B:  NCBI 分类单元标识符（蛋白质 B）
        stringId_B:     STRING 标识符（蛋白质 B）
        bitscore: Smith-Waterman 比对比特分数
    
    Query example: {"identifiers": ["Syp", "Dlg4", "Grin2b"], "species": 10090}
    """

    try:
        result = string_api.get_similarity_scores_of_the_protein_set(
            identifiers=identifiers, species=species
        )
    except Exception as e:
        return [
            {
                "error": f"An error occurred while getting similarity scores of the protein set: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_best_similarity_hits_between_species(identifiers: list[str], species: int, species_b: list[int]):
    """检索从你的输入蛋白质到每个 STRING 物种中最佳（最）相似蛋白质的相似性。
    
    Args:
        identifiers: 多个项目列表的必需参数
        species: 指定输入标识符的物种（例如人类为 9606，或 STRG0AXXXXX）
        species_b: 要比较的目标物种的 NCBI 分类单元标识符列表，用 "%0d" 分隔（例如人类、果蝇和酵母为 "9606%0d7227%0d4932"）
        
    Returns:
        包含以下字段的字典：
        ncbiTaxonId_A:  NCBI 分类单元标识符（蛋白质 A）
        stringId_A:     STRING 标识符（蛋白质 A）要比较的目标物种的分类学 ID
        ncbiTaxonId_B:  NCBI 分类单元标识符（蛋白质 B）
        stringId_B:     STRING 标识符（蛋白质 B）
        bitscore:       Smith-Waterman 比对比特分数
    
    Query example: {"identifiers": ["TP53", "BRCA1"], "species": 9606, "species_b": [10090, 10116]}
    """

    try:
        result = string_api.get_best_similarity_hits_between_species(
            identifiers=identifiers, species=species, species_b=species_b
        )
    except Exception as e:
        return [
            {
                "error": f"An error occurred while getting best similarity hits of the protein set between species: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_functional_enrichment(identifiers: list[str], species: int, background_string_identifiers: str):
    """STRING 将多个数据库映射到其蛋白质上，包括：Gene Ontology、KEGG 通路、UniProt 关键词、PubMed 出版物、Pfam 结构域、InterPro 结构域和 SMART 结构域。
    STRING 富集 API 方法允许你检索任何输入蛋白质集的功能富集。
    它将告诉你哪些输入蛋白质具有富集的术语以及该术语的描述。
    API 提供原始 p 值以及错误发现率（B-H 校正的 p 值）。
    Args:
        identifiers: 多个项目列表的必需参数
        background_string_identifiers: 使用此参数，你可以指定实验的背景蛋白质组。只识别 STRING 标识符（每个必须用 "%0d" 分隔），例如 '7227.FBpp0077451%0d7227.FBpp0074373'。你可以使用映射标识符方法映射 STRING 标识符。
        species: NCBI/STRING 分类单元（例如人类为 9606，或 STRG0AXXXXX）
    Returns:
        category: 术语类别（例如 GO 过程、KEGG 通路）
        term: 富集术语（GO 术语、结构域或通路）
        number_of_genes: 输入列表中分配了该术语的基因数量
        number_of_genes_in_background: 背景蛋白质组中分配了该术语的基因总数
        ncbiTaxonId: NCBI 分类单元标识符
        inputGenes: 来自你输入的基因名称
        preferredNames: 常见蛋白质名称（与输入基因顺序相同）
        p_value: 原始 p 值
        fdr: 错误发现率
        description: 富集术语的描述
    """
    try:
        result = string_api.get_functional_enrichment(
            identifiers=identifiers,
            species=species,
            background_string_identifiers=background_string_identifiers,
        )
    except Exception as e:
        return [
            {
                "error": f"An error occurred while getting functional enrichment for proteins: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_functional_annotation(identifiers: list[str], species: int, allow_pubmed: int, only_pubmed: int):
    """STRING 将多个数据库映射到其蛋白质上，包括：Gene Ontology、KEGG 通路、UniProt 关键词、PubMed 出版物、Pfam 结构域、InterPro 结构域和 SMART 结构域。
    
    Args:
        identifiers: 多个项目列表的必需参数
        species: NCBI/STRING 分类单元（例如人类为 9606，或 STRG0AXXXXX，参见：STRING 生物体）
        allow_pubmed: 1 表示除其他类别外还打印 PubMed 注释，默认为 0
        only_pubmed: 1 表示仅打印 PubMed 注释，默认为 0
    
    Returns:
        包含以下字段的字典：
        category: 术语类别（例如 GO 过程、KEGG 通路）
        term: 富集术语（GO 术语、结构域或通路）
        number_of_genes: 输入列表中分配了该术语的基因数量
        ratio_in_set: 输入列表中分配了该术语的蛋白质比例
        ncbiTaxonId: NCBI 分类单元标识符
        inputGenes: 来自你输入的基因名称
        preferredNames: 常见蛋白质名称（与输入基因顺序相同）
        description: 富集术语的描述
    
    Query example: {"identifiers": ["TP53", "BRCA1"], "species": 9606, "allow_pubmed": 1, "only_pubmed": 0}
    """

    try:
        result = string_api.get_functional_annotation(
            identifiers=identifiers,
            species=species,
            allow_pubmed=allow_pubmed,
            only_pubmed=only_pubmed,
        )
    except Exception as e:
        return [
            {
                "error": f"An error occurred while getting functional annotation for proteins: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_ppi_enrichment(identifiers: list[str], species: int):
    """获取由其 STRING 标识符表示的基因列表的蛋白质-蛋白质相互作用富集。
    
    Args:
        identifiers: 基因的 STRING 标识符列表
        species: NCBI/STRING 分类单元编号（例如人类为 9606，或小鼠为 STRG0A10090）
    
    Returns:
        包含以下字段的字典：
        number_of_nodes: 网络中的蛋白质数量
        number_of_edges: 网络中的边数量
        average_node_degree: 网络中节点的平均度数
        local_clustering_coefficient: 平均局部聚类系数
        expected_number_of_edges: 基于节点度数的预期边数
        p_value: 你的网络具有比预期更多相互作用的显著性
    
    Query example: {"identifiers": ["Pax6", "Sox2", "Nanog"], "species": 10090}
    """

    try:
        result = string_api.get_ppi_enrichment(identifiers=identifiers, species=species)
    except Exception as e:
        return {"error": f"An error occurred while getting ppi enrichment: {str(e)}"}
    return result


@mcp.prompt()
def system_prompt() -> str:
    """客户端的系统提示。"""
    prompt = """你可以访问用于搜索 STRING 的工具：功能性蛋白质关联网络。
    使用 API 工具提取相关信息。
    如果用户没有提供缺失的参数（如 STRING 标识符），请用合理的值填充。"""
    return prompt
