from asyncio import to_thread
from typing import Union
from mcp.server.fastmcp import FastMCP

from tools.biodb.ncbi.ncbi_api import NCBIAPI


mcp = FastMCP(
    "ncbi_mcp", 
    stateless_http=True
)
ncbi_api = NCBIAPI()


@mcp.tool()
async def get_gene_metadata_by_gene_name(name: str, species: str = 'human'):
    """通过基因符号获取基因摘要。默认以分页 JSON 格式返回。
    
    返回的 JSON 包含详细的基因信息，包括：
    - 基本基因信息：基因 ID、符号、描述、税号 ID、物种名称
    - 基因类型和方向
    - 参考标准和基因组位置
    - 染色体位置
    - 外部数据库 ID（HGNC、Swiss-Prot、Ensembl、OMIM）
    - 基因同义词
    - 转录本和蛋白质计数
    - 基因摘要/描述
    - 基因本体注释：
        - 分子功能（例如 DNA 结合、转录调控）
        - 生物过程（例如凋亡、细胞周期调控）
        - 细胞组分（例如细胞核、细胞质）

    Args:
        name: 要搜索的基因名称/符号
        species: 要搜索的物种（默认：'human'）

    Returns:
        包含 JSON 格式基因元数据的文本响应

    Raises:
        requests.exceptions.RequestException: 如果 API 请求失败
        
    Query example: {"name": "BRCA1", "species": "human"}
    """
    try:
        return await to_thread(ncbi_api.get_gene_metadata_by_gene_name, name, species)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_gene_by_ids(gene_ids: Union[int, list[int]]):
    """通过基因 ID 获取基因信息。
    
    Args:
        gene_ids: 单个基因 ID 或基因 ID 列表
        
    Returns:
        包含基因信息的 json 格式响应
        
    Query example: {"gene_ids": [59067, 50615]}
    
    """
    try:
        return await to_thread(ncbi_api.get_gene_by_ids, gene_ids)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_gene_by_accession(accessions: Union[str, list[str]]):
    """通过登录号获取基因信息。
    
    Args:
        accessions: 单个登录号或登录号列表
        
    Returns:
        包含基因信息的 json 格式响应
        
    Query example: {"accessions": ["NP_068575.1", "NP_851564.1"]}
    
    """
    try:
        return await to_thread(ncbi_api.get_gene_by_accession, accessions)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_gene_by_accession_dataset_report(accessions: Union[str, list[str]]):
    """通过登录号 ID 获取数据集报告。
    
    Args:
        accessions: 单个登录号或登录号列表
    
    Query example: {"accessions": ["NP_068575.1", "NP_851564.1"]}
    """
    try:
        return await to_thread(ncbi_api.get_gene_by_accession_dataset_report, accessions)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_gene_by_accession_product_report(accessions: Union[str, list[str]]):
    """通过登录号 ID 获取基因产物报告。
    
    Args:
        accessions: 单个登录号或登录号列表
        
    Query example: {"accessions": ["NP_068575.1", "NP_851564.1"]}
    """
    try:
        return await to_thread(ncbi_api.get_gene_by_accession_product_report, accessions)
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
async def get_gene_download_summary_by_id(gene_ids: Union[int, list[int]]):
    """通过 GeneID 获取基因下载摘要。
    
    Args:
        gene_ids: 单个基因 ID 或基因 ID 列表
        
    Query example: {"gene_ids": [59067, 50615]}
    """
    try:
        return await to_thread(ncbi_api.get_gene_download_summary_by_id, gene_ids)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_gene_links_by_id(gene_ids: Union[int, list[int]]):
    """通过基因 ID 获取基因链接。
    
    Args:
        gene_ids: 单个基因 ID 或基因 ID 列表
        
    Query example: {"gene_ids": [59067, 50615]}
    """
    try:
        return await to_thread(ncbi_api.get_gene_links_by_id, gene_ids)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_gene_dataset_report_by_locus_tag(locus_tags: Union[str, list[str]]):
    """通过基因座标签获取基因数据集报告。
    
    Args:
        locus_tags: 单个基因座标签或基因座标签列表
        
    Query example: {"locus_tags": ["b0001", "b0002"]}
    """
    try:
        return await to_thread(ncbi_api.get_gene_dataset_report_by_locus_tag, locus_tags)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_gene_product_report_by_locus_tag(locus_tags: Union[str, list[str]]):
    """通过基因座标签获取基因产物报告。
    
    Args:
        locus_tags: 单个基因座标签或基因座标签列表
        
    Query example: {"locus_tags": ["b0001", "b0002"]}
    """
    try:
        return await to_thread(ncbi_api.get_gene_product_report_by_locus_tag, locus_tags)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_gene_by_symbol_dataset_report(symbols: str, taxon: str = 'human'):
    """通过分类单元获取数据集报告。
    
    Args:
        symbols: 基因符号
        taxon: 分类单元
        
    Query example: {"symbols": "TP53", "taxon": "human"}
    """
    try:
        return await to_thread(ncbi_api.get_gene_by_symbol_dataset_report, symbols, taxon)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_gene_by_symbol_product_report(symbols: str, taxon: str = 'human'):
    """通过分类单元获取产物报告。
    
    Args:
        symbols: 基因符号
        taxon: 分类单元
        
    Query example: {"symbols": "TP53", "taxon": "human"}
    """
    try:
        return await to_thread(ncbi_api.get_gene_by_symbol_product_report, symbols, taxon)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_gene_by_taxon_dataset_report(taxon: str):
    """通过分类学标识符获取基因数据集报告。
    
    Args:
        taxon: 分类单元
        
    Query example: {"taxon": "human"}
    """
    try:
        return await to_thread(ncbi_api.get_gene_by_taxon_dataset_report, taxon)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_gene_by_taxon_product_report(taxon: str):
    """通过分类学标识符获取基因产物报告。
    
    Args:
        taxon: 分类单元
        
    Query example: {"taxon": "human"}
    """
    try:
        return await to_thread(ncbi_api.get_gene_by_taxon_product_report, taxon)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_gene_dataset_report_by_id(gene_ids: Union[int, list[int]]):
    """通过数据集报告获取基因信息。
    
    Args:
        gene_ids: 单个基因 ID 或基因 ID 列表
        
    Query example: {"gene_ids": [59067, 50615]}
    """
    try:
        return await to_thread(ncbi_api.get_gene_dataset_report_by_id, gene_ids)
    except Exception as e:
        return f"Error: {e}"

# Genome related endpoints
@mcp.tool()
async def get_genome_annotation_report(accession: str):
    """通过基因组登录号获取基因组注释报告。
    
    Args:
        accession: 基因组登录号
        
    Returns:
        包含注释报告的 json 格式响应
        
    Query example: {"accession": "GCF_000001635.27"}
    """
    try:
        return await to_thread(ncbi_api.get_genome_annotation_report, accession)
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
async def get_genome_annotation_summary(accession: str):
    """获取基因组注释报告摘要信息。
    
    Args:
        accession: 基因组登录号
        
    Returns:
        包含注释摘要的 json 格式响应
        
    Query example: {"accession": "GCF_000001635.27"}
    """
    try:
        return await to_thread(ncbi_api.get_genome_annotation_summary, accession)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_genome_revision_history(accession: str):
    """通过登录号获取组装的修订历史。
    
    Args:
        accession: 基因组登录号
        
    Query example: {"accession": "GCF_000001635.27"}
    """
    try:
        return await to_thread(ncbi_api.get_genome_revision_history, accession)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_genome_sequence_reports(accession: str):
    """通过登录号获取序列报告。
    
    Args:
        accession: 基因组登录号
        
    Query example: {"accession": "GCF_000001635.27"}
    """
    try:
        return await to_thread(ncbi_api.get_genome_sequence_reports, accession)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def check_genome_accessions(accessions: Union[str, list[str]]):
    """检查基因组登录号的有效性。
    
    Args:
        accessions: 基因组登录号
        
    Query example: {"accessions": "GCF_000001635.27"}
    """
    try:
        return await to_thread(ncbi_api.check_genome_accessions, accessions)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_genome_dataset_report_by_accession(accessions: Union[str, list[str]]):
    """通过登录号获取数据集报告。
    
    Args:
        accessions: 基因组登录号
        
    Query example: {"accessions": "GCF_000001635.27"}
    """
    try:
        return await to_thread(ncbi_api.get_genome_dataset_report_by_accession, accessions)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_genome_download(accessions: Union[str, list[str]]):
    """通过登录号获取基因组数据集。
    
    Args:
        accessions: 基因组登录号
        
    Query example: {"accessions": "GCF_000001635.27"}
    """
    try:
        return await to_thread(ncbi_api.get_genome_download, accessions)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_genome_download_summary(accessions: Union[str, list[str]]):
    """预览基因组数据集下载。
    
    Args:
        accessions: 基因组登录号
        
    Query example: {"accessions": "GCF_000001635.27"}
    """
    try:
        return await to_thread(ncbi_api.get_genome_download_summary, accessions)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_genome_links(accessions: Union[str, list[str]]):
    """通过登录号获取组装链接。
    
    Args:
        accessions: 基因组登录号
        
    Query example: {"accessions": "GCF_000001635.27"}
    """
    try:
        return await to_thread(ncbi_api.get_genome_links, accessions)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_genome_dataset_report_by_assembly_name(assembly_names: Union[str, list[str]]):
    """通过组装名称获取数据集报告。
    
    Args:
        assembly_names: 组装名称
        
    Query example: {"assembly_names": "GCF_000001635.27"}
    """
    try:
        return await to_thread(ncbi_api.get_genome_dataset_report_by_assembly_name, assembly_names)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_genome_dataset_report_by_bioproject(bioprojects: Union[str, list[str]]):
    """通过生物项目获取数据集报告。
    
    Args:
        bioprojects: 生物项目
        
    Query example: {"bioprojects": ["PRJNA489243", "PRJNA31257"]}
    """
    try:
        return await to_thread(ncbi_api.get_genome_dataset_report_by_bioproject, bioprojects)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_genome_dataset_report_by_biosample(biosample_ids: Union[str, list[str]]):
    """通过生物样本 ID 获取数据集报告。
    
    Args:
        biosample_ids: 生物样本 ID
        
    Query example: {"biosample_ids": ["SAMN15960293"]}
    """
    try:
        return await to_thread(ncbi_api.get_genome_dataset_report_by_biosample, biosample_ids)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_sequence_assemblies(accession: str):
    """通过序列登录号获取组装登录号。
    
    Args:
        accession: 序列登录号
        
    Query example: {"accession": "NC_000001.11"}
    """
    try:
        return await to_thread(ncbi_api.get_sequence_assemblies, accession)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_genome_dataset_report_by_taxon(taxons: str):
    """通过分类单元获取数据集报告。
    
    Args:
        taxons: 分类单元
        
    Query example: {"taxons": "human"}
    """
    try:
        return await to_thread(ncbi_api.get_genome_dataset_report_by_taxon, taxons)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_genome_dataset_report_by_wgs(wgs_accessions: Union[str, list[str]]):
    """通过 WGS 登录号获取数据集报告。
    
    Args:
        wgs_accessions: WGS 登录号
        
    Query example: {"wgs_accessions": ["JAHLSK02", "JAAKGM02"]}
    """
    try:
        return await to_thread(ncbi_api.get_genome_dataset_report_by_wgs, wgs_accessions)
    except Exception as e:
        return f"Error: {e}"

# Virus related endpoints
@mcp.tool()
async def get_virus_annotation_report(accessions: Union[str, list[str]]):
    """通过登录号获取病毒注释报告。
    
    Args:
        accessions: 病毒登录号
        
    Returns:
        包含注释报告的 json 格式响应
        
    Query example: {"accessions": ["NC_038294.1"]}
    """
    try:
        return await to_thread(ncbi_api.get_virus_annotation_report, accessions)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def check_virus_accessions(accessions: Union[str, list[str]]):
    """检查病毒登录号的有效性。
    
    Args:
        accessions: 病毒登录号
        
    Query example: {"accessions": ["NC_038294.1"]}
    """
    try:
        return await to_thread(ncbi_api.check_virus_accessions, accessions)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_virus_dataset_report(accessions: Union[str, list[str]]):
    """通过登录号获取病毒数据集报告。
    
    Args:
        accessions: 病毒登录号
        
    Query example: {"accessions": ["NC_038294.1"]}
    """
    try:
        return await to_thread(ncbi_api.get_virus_dataset_report, accessions)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_virus_genome_download(accessions: Union[str, list[str]]):
    """通过登录号下载病毒基因组。
    
    Args:
        accessions: 病毒登录号
        
    Query example: {"accessions": ["NC_038294.1"]}
    """
    try:
        return await to_thread(ncbi_api.get_virus_genome_download, accessions)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_virus_by_taxon_annotation_report(taxon: str):
    """通过分类单元获取病毒注释报告。
    
    Args:
        taxon: 病毒分类单元
        
    Query example: {"taxon": "SARS-COV-2"}
    """
    try:
        return await to_thread(ncbi_api.get_virus_by_taxon_annotation_report, taxon)
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
async def get_virus_by_taxon_genome(taxon: str):
    """通过分类单元获取病毒基因组。
    
    Args:
        taxon: 病毒分类单元
        
    Query example: {"taxon": "2697049"}
    """
    try:
        return await to_thread(ncbi_api.get_virus_by_taxon_genome, taxon)
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
async def get_virus_by_taxon_genome_table(taxon: str):
    """通过分类单元获取病毒基因组表。
    
    Args:
        taxon: 病毒分类单元
        
    Query example: {"taxon": "2697049"}
    """
    try:
        return await to_thread(ncbi_api.get_virus_by_taxon_genome_table, taxon)
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
async def get_version():
    """获取所有服务的当前版本。
    
    Returns:
        包含版本信息的 json 格式响应
    """
    try:
        return await to_thread(ncbi_api.get_version)
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
async def get_taxonomy_related_ids(tax_id: int):
    """获取相关的分类学 ID。
    
    Args:
        tax_id: 分类学 ID
        
    Query example: {"tax_id": 9606}
    """
    try:
        return await to_thread(ncbi_api.get_taxonomy_related_ids, tax_id)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_taxonomy_download(tax_ids: Union[int, list[int]]):
    """下载分类学数据。
    
    Args:
        tax_ids: 分类学 ID
        
    Query example: {"tax_ids": [9606, 9605]}
    """
    try:
        return await to_thread(ncbi_api.get_taxonomy_download, tax_ids)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_taxonomy_links(taxon: str):
    """获取分类学链接。
    
    Args:
        taxon: 分类学 ID
        
    Query example: {"taxon": "9606"}
    """
    try:
        return await to_thread(ncbi_api.get_taxonomy_links, taxon)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_taxonomy(taxons: Union[str, list[str]]):
    """获取分类学信息。
    
    Args:
        taxons: 分类学 ID
        
    Returns:
        包含分类学信息的 json 格式响应
        
    Query example: {"taxons": ["9606", "9605"]}
    """
    try:
        return await to_thread(ncbi_api.get_taxonomy, taxons)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_taxonomy_dataset_report(taxons: Union[str, list[str]]):
    """获取分类学数据集报告。
    
    Args:
        taxons: 分类学 ID
        
    Returns:
        包含数据集报告的 json 格式响应
        
    Query example: {"taxons": ["9606", "9605"]}
    """
    try:
        return await to_thread(ncbi_api.get_taxonomy_dataset_report, taxons)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_taxonomy_filtered_subtree(taxons: Union[str, list[str]]):
    """获取过滤后的分类学子树。
    
    Args:
        taxons: 分类学 ID
        
    Query example: {"taxons": ["9606", "9605"]}
    """
    try:
        return await to_thread(ncbi_api.get_taxonomy_filtered_subtree, taxons)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_taxonomy_name_report(taxons: Union[str, list[str]]):
    """获取分类学名称报告。
    
    Args:
        taxons: 分类学 ID
        
    Query example: {"taxons": ["9606", "9605"]}
    """
    try:
        return await to_thread(ncbi_api.get_taxonomy_name_report, taxons)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_taxonomy_taxon_suggest(taxon_query: str):
    """获取分类学建议。
    
    Args:
        taxon_query: 分类学查询
        
    Query example: {"taxon_query": "hum"}
    """
    try:
        return await to_thread(ncbi_api.get_taxonomy_taxon_suggest, taxon_query)
    except Exception as e:
        return f"Error: {e}"

# BioSample endpoint
@mcp.tool()
async def get_biosample_report(accessions: Union[str, list[str]]):
    """获取生物样本报告。
    
    Args:
        accessions: 生物样本登录号
        
    Returns:
        包含生物样本报告的 json 格式响应
        
    Query example: {"accessions": ["SAMN15960293"]}
    """
    try:
        return await to_thread(ncbi_api.get_biosample_report, accessions)
    except Exception as e:
        return f"Error: {e}"

# Organelle related endpoints
@mcp.tool()
async def get_organelle_download(accessions: Union[str, list[str]]):
    """下载细胞器数据。
    
    Args:
        accessions: 细胞器登录号
        
    Query example: {"accessions": ["NC_001643.1", "NC_002082.1"]}
    """
    try:
        return await to_thread(ncbi_api.get_organelle_download, accessions)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_organelle_dataset_report(accessions: Union[str, list[str]]):
    """获取细胞器数据集报告。
    
    Args:
        accessions: 细胞器登录号
        
    Returns:
        包含数据集报告的 json 格式响应
        
    Query example: {"accessions": ["NC_001643.1", "NC_002082.1"]}
    """
    try:
        return await to_thread(ncbi_api.get_organelle_dataset_report, accessions)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_organelle_by_taxon_dataset_report(taxons: Union[str, list[str]]):
    """通过分类单元获取细胞器数据集报告。
    
    Args:
        taxons: 分类学 ID
        
    Returns:
        包含数据集报告的 json 格式响应
        
    Query example: {"taxons": ["9606", "9605"]}
    """
    try:
        return await to_thread(ncbi_api.get_organelle_by_taxon_dataset_report, taxons)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_gene_product_report_by_id(gene_ids: Union[int, list[int]]):
    """通过基因 ID 获取基因产物报告。
    
    Args:
        gene_ids: 基因 ID
        
    Query example: {"gene_ids": [59067, 50615]}
    """
    try:
        return await to_thread(ncbi_api.get_gene_product_report_by_id, gene_ids)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_gene_orthologs(gene_id: int):
    """通过基因 ID 获取基因直系同源物。
    
    Args:
        gene_ids: 基因 ID
        
    Query example: {"gene_ids": 59067}
    """
    try:
        return await to_thread(ncbi_api.get_gene_orthologs, gene_id)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_gene_by_taxon(taxon: str):
    """通过分类单元获取基因信息。
    
    Args:
        taxon: 分类单元
        
    Query example: {"taxon": "9606"}
    """
    try:
        return await to_thread(ncbi_api.get_gene_by_taxon, taxon)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_gene_counts_by_taxon(taxon: str):
    """通过分类单元获取基因计数。
    
    Args:
        taxon: 分类单元
        
    Query example: {"taxon": "9606"}
    """
    try:
        return await to_thread(ncbi_api.get_gene_counts_by_taxon, taxon)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_chromosome_summary(taxon: str, annotation_name: str):
    """通过分类单元和注释名称获取染色体摘要。
    
    Args:
        taxon: 分类单元
        annotation_name: 注释名称
        
    Query example: {"taxon": "9606", "annotation_name": "GCF_028858705.1-RS_2023_03"}
    """
    try:
        return await to_thread(ncbi_api.get_chromosome_summary, taxon, annotation_name)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_genome_by_accession(accession: str):
    """通过登录号获取基因组信息。
    
    Args:
        accession: 基因组登录号
        
    Query example: {"accession": "GCF_028858705.1"}
    """
    try:
        return await to_thread(ncbi_api.get_genome_by_accession, accession)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_prokaryote_gene_dataset_by_refseq_protein_accession(refseq_protein_accession: str):
    """通过 RefSeq 蛋白质登录号获取原核生物基因数据集。
    
    Args:
        refseq_protein_accession: RefSeq 蛋白质登录号
        
    Query example: {"refseq_protein_accession": "WP_015878339.1"}
    """
    try:
        return await to_thread(ncbi_api.get_prokaryote_gene_dataset_by_refseq_protein_accession, refseq_protein_accession)
    except Exception as e:
        return f"Error: {e}"

