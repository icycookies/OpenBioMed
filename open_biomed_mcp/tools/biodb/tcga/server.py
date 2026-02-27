from mcp.server.fastmcp import FastMCP

from tools.biodb.tcga.tcga_api import TCGA_API


mcp = FastMCP("tcga_mcp", stateless_http=True)
tcga_api = TCGA_API()


@mcp.tool()
async def get_gene_specific_expression_in_cancer_type(gene: str):
    """使用 Firebrowse API（TCGA mRNASeq）分析给定基因在不同癌症类型中的组织特异性表达模式。
    它计算每种癌症（队列）的平均表达量，计算平均表达量的 z 分数，并返回基因高表达或低表达的癌症类型。

    Args:
        gene: 基因符号，例如 "TP53"、"BRCA1"、"EGFR"

    Returns:
        包含两个键的字典：
        - high_expression_cancers: 基因高表达的癌症类型列表（z > 1）
        - low_expression_cancers: 基因低表达的癌症类型列表（z < -1）
        
    Query example: {"gene": "TP53"}
    """
    try:
        result = tcga_api.get_gene_specific_expression_in_cancer_type(gene=gene)
    except Exception as e:
        return [{"error": f"An error occurred while search gene: {str(e)}"}]
    return result

@mcp.prompt()
def system_prompt():
    """客户端的系统提示。"""
    prompt ="""你是一个智能生物医学助手，可以访问癌症基因组学工具。
    当用户询问特定基因在癌症类型中的表达模式时，
    你的目标是识别哪些癌症类型显示该基因的高表达或低表达。
    如果用户没有提供缺失的参数（如基因），请用合理的值填充。
    清晰简洁地回答，并引用提到的基因符号。"""
    return prompt

