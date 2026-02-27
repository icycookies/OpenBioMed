from mcp.server.fastmcp import FastMCP

from tools.biodb.dbsearch.dbsearch_api import DBSearch

mcp = FastMCP(
    "dbsearch_mcp",
    stateless_http=True,
)

dbsearch = DBSearch()


@mcp.tool()
async def clinvar_get_best_refseqid_by_sequence(seq: str, retries: int = 3, wait: int = 5):
    """使用 BLASTP 查找蛋白质序列的最佳匹配 RefSeq ID。
    
    Args:
        seq (str): 要搜索的蛋白质序列
        retries (int): BLAST 失败时的重试次数（默认：3）
        wait (int): 重试之间等待的秒数（默认：5）
        
    Returns:
        Optional[str]: 如果找到 100% 一致性的匹配 RefSeq ID（例如 "NP_123456"），
                      如果未找到完全匹配或发生错误则返回 None。
    """
    try:
        return dbsearch.clinvar_get_best_refseqid_by_sequence(seq, retries, wait)
    except Exception:
        return None

@mcp.tool()
async def clinvar_query_variant_significance(refseqid: str = None, variant: str = None, hgvs: str = None):
    """查询 ClinVar 以获取变异分类/显著性。
    
    Args:
        refseqid (str): RefSeq 蛋白质 ID（例如 "NP_123456"）
        variant (str): HGVS 格式的蛋白质变异（例如 "P123L"）
        hgvs (str): 完整的 HGVS 表示法（例如 "NP_123456.1:p.P123L"）
        
    Returns:
        Union[dict, str]: 
            - dict: 如果找到则返回 ClinVar germline_classification 数据
            - str: 如果未找到变异或发生错误则返回错误消息
    """
    try:
        return dbsearch.clinvar_query_variant_significance(refseqid, variant, hgvs)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
async def clinvar_query_sequence_variants(sequence: str, variants: list[str]):
    """查询 ClinVar 以获取蛋白质序列上的多个变异。
    
    Args:
        sequence (str): 参考蛋白质序列
        variants (list[str]): 变异字符串列表（例如 ["P123L", "R456K"]）
        
    Returns:
        dict: 变异到其 ClinVar 显著性结果的映射
              如果未找到序列的 RefSeq ID 或发生错误则返回空字典
    """
    try:
        return dbsearch.clinvar_query_sequence_variants(sequence, variants)
    except Exception as e:
        return str(e)

@mcp.tool()
async def clinvar_find_single_mutation(mutant_seq: str):
    """查找突变体和参考序列之间的单个氨基酸突变。
    
    Args:
        mutant_seq (str): 突变体蛋白质序列
        
    Returns:
        Optional[dict]: 如果找到单个突变则返回包含突变详细信息的字典：
            - ref_id: 参考 RefSeq ID
            - hgvs: HGVS 表示法
            - variant: 变异字符串
            - pos: 突变位置
            - wildtype: 野生型氨基酸
            - mutant: 突变型氨基酸
            如果未找到单个突变或发生错误则返回 None。
    """
    try:
        return dbsearch.clinvar_find_single_mutation(mutant_seq)
    except Exception as e:
        return str(e)

@mcp.tool()
async def get_genes_in_region(chrom: str, start: int, end: int):
    """
    查询 Ensembl REST API 以获取特定基因组区域内的基因。

    Args:
        chrom (str): 染色体（例如 'chr10'）。
        start (int): 起始坐标。
        end (int): 结束坐标。

    Returns:
        List[str]: 该区域内的基因名称列表。
    """
    return dbsearch.get_genes_in_region(chrom, start, end)

@mcp.tool()
async def ensembl_get_genes_by_band(query_band: str):
    """
    提取细胞遗传学带区域中的基因（例如 'chr10q21'）。

    Args:
        query_band (str): 带查询，如 'chr10q21'。

    Returns:
        List[str]: 指定细胞带区域中的基因名称列表。
    """
    return dbsearch.ensembl_get_genes_by_band(query_band)

@mcp.tool()
async def gsea_get_genelist_from_genesetname(genesetname: str):
    """
    从 GSEA 数据库中的特定基因集检索基因列表。

    Args:
        genesetname (str): 要查询的基因集名称（例如 "CAMP_UP.V1_DN"、"SCHERER_PBMC_APSV_WETVAX_AGE_18_40YO_5_TO_7DY_UP"）。
            这应该是 GSEA 数据库中用于基因集的标识符。

    Returns:
        list: 指定基因集中包含的基因符号列表。
                如果未找到基因集或发生错误，则返回空列表。
    """
    return dbsearch.gsea_get_genelist_from_genesetname(genesetname)

@mcp.tool()
async def gtrd_gene_to_entry(gene_name: str, organism: str = None):
    """
    使用 GTRD API 将基因符号转换为 UniProt 蛋白质条目 ID。
    
    Args:
        gene_name (str): 基因符号，例如 "TP53"
        organism (str): 可选的 NCBI 分类 ID（默认：None 使用 API 默认值）
        
    Returns:
        List[types.TextContent]: 包含一个 TextContent 对象的列表，其中包含：
            - text: UniProt 条目 ID（例如 "P04637"）
                
        如果转换失败或未找到结果则返回空列表。
        
    Example:
        >>> await gtrd_gene_to_entry("TP53")
        "P04637"
    """
    try:
        entry = dbsearch.gtrd_gene_to_entry(gene_name, organism)
        return entry
    except Exception as e:
        return str(e)

@mcp.tool() 
async def gtrd_entry_to_target_genes(entry: str, promoter_dir: str = None):
    """
    使用 GTRD 启动子数据检索 UniProt 条目的靶基因。
    
    Args:
        entry (str): UniProt 登录号 ID（例如 "P04637"）
        promoter_dir (str): 启动子文件目录的可选路径
        
    Returns:
        List[types.TextContent]: 包含一个 TextContent 对象的列表，其中包含：
            - text: 靶基因符号的 JSON 数组
                
        如果未找到靶基因或发生错误则返回空列表。
        
    Example:
        >>> await gtrd_entry_to_target_genes("P04637")
        ["GENE1", "GENE2", ...]
    """
    try:
        target_genes = dbsearch.gtrd_entry_to_target_genes(entry, promoter_dir)
        return target_genes
    except Exception as e:
        return str(e)

@mcp.tool()
async def mirdb_get_geneset_by_mirname(mirname: str, candidates: list[str]):
    """
    从 miRDB 数据库查询特定人类 miRNA（例如 hsa-miR-3140-5p）的预测靶基因符号。

    Args:
        mirname (str): 人类 miRNA 的名称。必须遵循以下标准命名格式之一：
            - 3 部分格式：hsa-mir-8068
            - 4 部分格式：hsa-mir-3140-5p 或 hsa-let-7g-5p
            所有有效的 miRNA 名称必须以 "hsa-" 前缀开头。
        candidates (list[str]): 靶基因符号的候选列表

   Returns:
        {
            "predicted_targets": ["HECTD1"],
            "not_predicted_targets": ["SPAG9", "SPATA31C2", "OR10J4"]
        }
    """
    return dbsearch.mirdb_get_geneset_by_mirname(mirname, candidates)

@mcp.tool()
async def mousemine_get_geneset_from_mpid(mpid: str):
    """
    从 MouseMine 关键字搜索结果页面检索与给定 MGI 表型 ID（MPID）相关的小鼠基因符号列表。

    Args:
        mpid (str): 要在 MouseMine 中查询的小鼠表型 ID（例如 "MP:0005386"）。

    Returns:
        List[str]: 与给定 MPID 相关的基因符号（字符串）列表。
                仅包括类型为 "Protein Coding Gene" 的基因。

    Example:
        >>> self.mousemine_get_geneset_from_mpid("MP:0005386")
        ['Trp53', 'Cdkn1a', 'Brca1']
    """
    return dbsearch.mousemine_get_geneset_from_mpid(mpid)

@mcp.tool()
async def phipster_vpname2vpid(vpname: str):
    """
    使用 PHIPSTER vpid2name 映射 API 将病毒蛋白名称（vpname）转换为其对应的 VPID。

    Args:
        vpname (str): 病毒蛋白的**纯名称**，已删除病毒物种前缀。

    如果病毒蛋白名称类似于：
        `"Japanese encephalitis virus envelope protein"`

    您必须仅传递**蛋白质名称部分**：
        `"envelope protein"`

    不要包含病毒前缀：
        `"Japanese encephalitis virus"` ← 必须去除此部分。

    有效 `vpname` 的格式示例：
        - "hypothetical protein (gene: A11R)"
        - "Kelch-like protein (gene: C9L)"
        - "envelope protein"
        - "72L protein (gene: 72L)"
        - "encoded endoprotease (Late protein 3)"

    Returns:
        如果找到则返回对应的 VPID 字符串（例如 "23488"），否则返回 None。
        
        Example:
            "23488"
    """
    return dbsearch.phipster_vpname2vpid(vpname)

@mcp.tool()
async def phipster_get_hpid_list_by_vpid(vpid: str):
    """
    通过病毒蛋白 ID（VPID）从 Phipster 数据库检索病毒蛋白与人类蛋白之间的蛋白质-蛋白质相互作用（PPI）记录列表。

    Args:
        vpid: 要查询相互作用的病毒蛋白 ID。

    Returns:
    hpid 列表，每个人类蛋白 ID 与给定病毒蛋白相互作用。
        Example:
            ["23488", "23485", ...]
    """
    return dbsearch.phipster_get_hpid_list_by_vpid(vpid)

@mcp.tool()
async def phipster_hpid_list_to_hpname_list(hpid_list: list[int]):
    """
    使用 PHIPSTER 数据库映射将 hpid 记录列表转换为人类蛋白质名称记录。

    Args:
        hpid_list: hpid 列表

    Returns:
        通过对应的 'humanprotein_name' 获得的 hpname 列表。
        如果未找到给定 ID 的名称，它将被标记为 'Unknown_{id}'。
        
        Example:
        Input:
        [5095, 4427, 5539, 15404, 6385, 3727, 5161, 17652, 6447, 3758, 7540]
        Output:
        ['STAT3', 'CDK2', 'GSK3B', 'TRIB3', 'GRB2', 'SRC', 'STAT1', 'ARHGEF4', 'CSNK2A1', 'ITGA4', 'IL18']
    """
    return dbsearch.phipster_hpid_list_to_hpname_list(hpid_list)
