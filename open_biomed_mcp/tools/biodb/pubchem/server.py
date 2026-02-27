from mcp.server.fastmcp import FastMCP

from tools.biodb.pubchem.pubchem_api import PubChemAPI


mcp = FastMCP(
    "pubchem_mcp",
    stateless_http=True,
)
pubchem_api = PubChemAPI()


@mcp.tool()
async def search_pubchem_by_name(name: str):
    """通过化学名称在 PubChem 中搜索化合物。请注意，将化学名称匹配到结构充其量是一门不精确的科学，一个名称可能经常指代多个记录。
    
    Args:
        name: 名称（字符串）
        kwargs: 关键字参数（字符串）
    
    Query example: {"name": "aspirin", "kwargs": "{}"}
    
    Returns:
        sth
    """

    try:
        result = pubchem_api.search_pubchem_by_name(name)
    except Exception as e:
        return {"error": f"An error occurred while searching PubChem by name: {str(e)}"}
    return result

@mcp.tool()
async def search_pubchem_by_smiles(smiles: str):
    """通过 SMILES 字符串在 PubChem 中搜索化合物。
    
    Args:
        smiles: 要搜索的 SMILES 表示法
    
    Returns:
        包含与 SMILES 匹配的化合物搜索结果的字典
    
    Query example: {"smiles": "C[C@H](N)C(=O)O"}
    """


    try:
        result = pubchem_api.search_pubchem_by_smiles(smiles)
    except Exception as e:
        return {"error": f"An error occurred while searching PubChem by SMILES: {str(e)}"}
    return result

@mcp.tool()
async def get_pubchem_compound_by_cid(cid: str):
    """通过 PubChem CID 获取详细的化合物信息。
    
    Args:
        cid: PubChem 化合物 ID（整数或字符串）
    
    Returns:
        包含化合物详细信息的字典（完整的化学性质、结构信息、相关生物活性等）
    
    Query example: {"cid": 2244}
    """


    try:
        result = pubchem_api.get_pubchem_compound_by_cid(cid)
    except Exception as e:
        return {"error": f"An error occurred while getting PubChem compound by CID: {str(e)}"}
    return result

@mcp.tool()
async def search_pubchem_advanced(query: str):
    """使用复杂查询在 PubChem 上执行高级搜索。
    
    Args:
        query: 遵循 PubChem 语法的高级搜索查询字符串
        **kwargs: API 请求的附加参数
            
    Returns:
        包含与高级查询匹配的搜索结果的字典
    """
    try:
        result = pubchem_api.search_pubchem_advanced(query)
    except Exception as e:
        return {"error": f"An error occurred during advanced PubChem search: {str(e)}"}
    return result

@mcp.tool()
async def get_substance_by_sid(sid: str):
    """通过 PubChem SID 获取物质信息。
    
    Args:
        sid: PubChem 物质 ID
    
    Returns:
        包含物质信息的字典。此示例返回 Substance(sid)
    
    Query example: {"sid": 347827035}
    """


    try:
        result = pubchem_api.get_substance_by_sid(sid)
    except Exception as e:
        return {"error": f"An error occurred while getting substance by SID: {str(e)}"}
    return result

@mcp.tool()
async def get_compound_by_cid(cid: str):
    """通过 PubChem CID 获取化合物信息。
    
    Args:
        cid: PubChem 化合物 ID

    Returns:
        包含化合物信息的字典
    """
    try:
        result = pubchem_api.get_compound_by_cid(cid)
    except Exception as e:
        return {"error": f"An error occurred while getting compound by CID: {str(e)}"}
    return result

@mcp.tool()
async def get_compound_by_name(name: str):
    """通过化学名称获取化合物信息。请注意，将化学名称匹配到结构充其量是一门不精确的科学，一个名称可能经常指代多个记录。
    
    Args:
        name: 化学名称
    
    Returns:
        包含化合物信息的字典（CID、结构、性质等）
    
    Query example: {"name": "aspirin"}
    """


    try:
        result = pubchem_api.get_compound_by_name(name)
    except Exception as e:
        return {"error": f"An error occurred while getting compound by name: {str(e)}"}
    return result

@mcp.tool()
async def get_substance_by_name(name: str):
    """通过名称获取物质信息。
    
    Args:
        name: 物质名称（字符串）
        
    Returns:
        包含物质信息的字典
    
    Query example: {"name": "aspirin"}
    """


    try:
        result = pubchem_api.get_substance_by_name(name)
    except Exception as e:
        return {"error": f"An error occurred while getting substance by name: {str(e)}"}
    return result

@mcp.tool()
async def get_compound_property_by_name(name: str, property_name: str):
    """通过化合物名称从 PubChem 检索特定的化学性质。
    响应返回包含匹配化合物所请求性质的表格。
    
    Args:
        name: 化合物的化学名称（字符串）
        property_name: 要检索的性质名称，例如：
            - MolecularWeight
            - MolecularFormula
            - XLogP
            - TPSA
            - 等
    
    Returns:
        包含以下内容的字典：
        - PropertyTable:
            • Properties: 性质条目列表，每个包含：
                - CID:               PubChem 化合物 ID
                - <property_name>:   化合物所请求的性质值
    
    Query example:
        {"name": "caffeine", "property_name": "MolecularFormula"}
    """


    try:
        result = pubchem_api.get_compound_property_by_name(name, property_name)
    except Exception as e:
        return {"error": f"An error occurred while getting compound property by name: {str(e)}"}
    return result

@mcp.tool()
async def get_compound_synonyms_by_name(name: str):
    """通过化学名称从 PubChem 检索给定化合物的所有已知同义词。
    响应返回同义词列表，包括注册号、替代名称、商品名、数据库标识符和系统名称。
    
    Args:
        name: 化合物的化学名称（字符串）
    
    Returns:
        包含以下内容的字典：
        - InformationList:
            • Information: 条目列表，每个包含：
                - CID:     PubChem 化合物 ID
                - Synonym: 化合物的同义词字符串列表
    
    Query example:
        {"name": "caffeine"}
    """


    try:
        result = pubchem_api.get_compound_synonyms_by_name(name)
    except Exception as e:
        return {"error": f"An error occurred while getting compound synonyms by name: {str(e)}"}
    return result

@mcp.tool()
async def get_description_by_sid(sid: str):
    """通过 SID 获取 PubChem 物质的详细描述信息。
    响应包括完整的 Record 结构，包含以下部分：
    2D 结构、身份、来源、外部 ID、同义词、存储/修改日期、
    状态以及从该物质标准化的相关化合物。
    
    Args:
        sid: PubChem 物质 ID（整数或字符串）
    
    Returns:
        包含物质完整 Record 的字典，包含以下字段：
        - RecordType:      记录类型（"SID"）
        - RecordNumber:    数字 SID
        - RecordTitle:     物质标题/名称
        - Section:         部分列表，每个包含：
            • TOCHeading:       部分标题（例如 "2D Structure"、"Identity"）
            • Description:      描述该部分的文本
            • Information:      信息条目列表（值、参考、URL）
        - Reference:       参考列表，每个包含：
            • SourceName、SourceID、Description、URL
    
    Query example:
        {"sid": "12345"}
    """


    try:
        result = pubchem_api.get_description_by_sid(sid)
    except Exception as e:
        return {"error": f"An error occurred while getting description by SID: {str(e)}"}
    return result

@mcp.tool()
async def get_description_by_cid(cid: str):
    """通过 CID 检索 PubChem 化合物的详细描述信息。
    响应返回完整的 Record 结构，包括以下部分：
    • 结构（2D/3D 描绘）
    • 身份（来源、外部 ID、同义词、版本控制）
    • 存储/修改/可用日期
    • 记录状态
    • 相关记录（相关化合物、晶体数据、文章等）
    
    Args:
        cid: PubChem 化合物 ID（整数或字符串）
    
    Returns:
        包含化合物完整 Record 的字典，包含以下字段：
        - RecordType:      记录类型（"CID"）
        - RecordNumber:    数字 CID
        - RecordTitle:     化合物名称/标题
        - Section:         部分列表，每个包含：
            • TOCHeading:       部分标题（例如 "Structures"、"3D Conformer"）
            • Description:      描述该部分的文本
            • Information:      详细条目列表（值、参考、URL、表格）
        - Reference:       参考条目列表（来源名称、描述、URL）
    
    Query example:
        {"cid": "2244"}
    """


    try:
        result = pubchem_api.get_description_by_cid(cid)
    except Exception as e:
        return {"error": f"An error occurred while getting description by CID: {str(e)}"}
    return result

@mcp.tool() 
async def get_general_info_by_compound_name(name: str):
    """通过名称获取化合物的详细描述，包括总体信息、药物和药物信息、药理学和生物化学信息。
    
    Args:
        name: PubChem 化合物名称

    Returns:
        包含化合物描述的字典
    """
    try:
        result = pubchem_api.get_description_by_name(name)
    except Exception as e:
        return {"error": f"An error occurred while getting description by name: {str(e)}"}
    return result

@mcp.tool()
async def get_description_by_aid(aid: str):
    """通过 AID 检索 PubChem 生物测定的详细描述信息。
    响应返回完整的 Record 结构，包括以下部分：
    • 记录描述（存储者提供的摘要）
    • 描述（生物测定概述和测定背景）
    • 协议（实验协议详情）
    • 注释（存储者注释和参考）
    • 结果定义（数据表列定义）
    • 数据表（生物活性结果和标志）
    • 靶点（蛋白质/基因靶点）
    • 相关靶点、Entrez 交叉链接
    • 身份（测定元数据：名称、来源、类型、日期）
    • 生物测定注释（格式、检测方法等）
    
    Args:
        aid: PubChem 测定 ID（整数或字符串）
    
    Returns:
        包含测定完整 Record 的字典，包含以下字段：
        - RecordType:      记录类型（"AID"）
        - RecordNumber:    数字 AID
        - RecordTitle:     测定标题/名称
        - Section:         部分列表，每个包含：
            • TOCHeading:       部分标题（例如 "Protocol"、"Target"）
            • Description:      描述该部分的文本
            • Information:      详细条目列表（值、参考编号、URL）
        - Reference:       参考条目列表（来源名称、描述、URL）
    
    Query example:
        {"aid": "450"}
    """


    try:
        result = pubchem_api.get_description_by_aid(aid)
    except Exception as e:
        return {"error": f"An error occurred while getting description by AID: {str(e)}"}
    return result

@mcp.tool()
async def get_assay_summary_by_cid(cid: str):
    """检索给定 PubChem 化合物 CID 的生物测定活性摘要。
    响应包括化合物已测试的测定表，
    包含活性结果、靶点信息、测定元数据和参考的详情。
    
    Args:
        cid: PubChem 化合物 ID（整数或字符串）
    
    Returns:
        包含测定摘要表的字典，包含以下字段：
        - Table:
            • Columns:
                - AID:             PubChem 测定 ID
                - Panel Member ID: 测定面板标识符（如适用）
                - SID:             PubChem 物质 ID
                - CID:             PubChem 化合物 ID
                - Activity Outcome: 例如 "Active"、"Inactive"
                - Target GI:       靶点的 GenInfo 标识符
                - Target GeneID:   靶点的 NCBI 基因 ID
                - Activity Value [uM]: 数值活性测量（µM）
                - Activity Name:   活性指标名称（例如 "Kd"）
                - Assay Name:      测定描述
                - Assay Type:      测定类别（例如 "Other"、"Primary Screening"）
                - PubMed ID:       PubMed 文献参考
                - RNAi:            RNA 干扰注释（如有）
            • Row: 测定结果条目列表
    
    Query example:
        {"cid": "2144"}
    """


    try:
        result = pubchem_api.get_assay_summary_by_cid(cid)
    except Exception as e:
        return {"error": f"An error occurred while getting assay summary by CID: {str(e)}"}
    return result

@mcp.tool()
async def get_assay_summary_by_sid(sid: str):
    """检索给定 PubChem 物质 SID 的生物测定活性摘要。
    响应包括物质已测试的测定列表表，
    包含结果、靶点信息、测定元数据和参考的详情。
    
    Args:
        sid: PubChem 物质 ID（整数或字符串）
    
    Returns:
        包含测定摘要表的字典，包含以下字段：
        - Table:
            • Columns:
                - AID:              PubChem 测定 ID
                - Panel Member ID:  测定面板标识符（如适用）
                - SID:              PubChem 物质 ID
                - CID:              PubChem 化合物 ID
                - Activity Outcome: 例如 "Active"、"Inconclusive"、"Unspecified"
                - Target GI:        靶点的 GenInfo 标识符
                - Target GeneID:    靶点的 NCBI 基因 ID
                - Activity Value [uM]: 数值活性测量（µM），如可用
                - Activity Name:    活性指标名称（例如 "Kd"）
                - Assay Name:       测定描述/标题
                - Assay Type:       测定类别（例如 "Other"、"Primary Screening"）
                - PubMed ID:        PubMed 文献参考（如有）
                - RNAi:             RNA 干扰注释（如有）
            • Row: 测定结果条目列表，每个为包含 "Cell" 列表的字典
    
    Query example:
        {"sid": "8149208"}
    """


    try:
        result = pubchem_api.get_assay_summary_by_sid(sid)
    except Exception as e:
        return {"error": f"An error occurred while getting assay summary by SID: {str(e)}"}
    return result

@mcp.tool()
async def get_gene_summary_by_geneid(gene_id: str):
    """通过基因 ID 获取基因的摘要信息。
    
    Args:
        gene_id: 基因 ID

    Returns:
        包含基因摘要信息的字典
    """
    try:
        result = pubchem_api.get_gene_summary_by_geneid(gene_id)
    except Exception as e:
        return {"error": f"An error occurred while getting gene summary by Gene ID: {str(e)}"}
    return result

@mcp.tool()
async def get_protein_summary_by_accession(accession: str):
    """通过 UniProt 或其他登录号从 PubChem 检索蛋白质的摘要信息。
    响应包括基本注释，如蛋白质名称、分类学和已知同义词。
    
    Args:
        accession: 蛋白质登录号（字符串），例如 UniProt ID 或 NCBI 登录号
    
    Returns:
        包含以下内容的字典：
        - ProteinSummaries:
            • ProteinSummary: 摘要条目列表，每个包含：
                - ProteinAccession: 查询的登录号
                - Name: 官方蛋白质名称
                - TaxonomyID: NCBI 分类学标识符（例如 9606）
                - Taxonomy: 生物的拉丁名和通用名
                - Synonym: 替代名称或酶分类列表
    
    Query example:
        {"accession": "P00734"}
    """


    try:
        result = pubchem_api.get_protein_summary_by_accession(accession)
    except Exception as e:
        return {"error": f"An error occurred while getting protein summary by accession: {str(e)}"}
    return result

@mcp.tool()
async def get_taxonomy_summary_by_taxonomyid(taxonomy_id: str):
    """通过 NCBI 分类学 ID 检索生物分类学条目的摘要信息。
    响应包括科学名称和通用名称、等级、谱系和同义词。
    
    Args:
        taxonomy_id: NCBI 分类学 ID（整数或字符串）
    
    Returns:
        包含以下内容的字典：
        - TaxonomySummaries:
            • TaxonomySummary: 摘要条目列表，每个包含：
                - TaxonomyID:      数字分类学标识符
                - ScientificName:  拉丁科学名称（例如 "Homo sapiens"）
                - CommonName:      通用名称（例如 "human"）
                - Rank:            分类学等级（例如 "species"）
                - RankedLineage:   分层谱系，包含键：
                    • Superkingdom、Kingdom、Phylum、Class、Order、Family、Genus、Species
                - Synonym:         替代名称或历史名称列表
    
    Query example:
        {"taxonomy_id": "9606"}
    """


    try:
        result = pubchem_api.get_taxonomy_summary_by_taxonomyid(taxonomy_id)
    except Exception as e:
        return {"error": f"An error occurred while getting taxonomy summary by Taxonomy ID: {str(e)}"}
    return result

@mcp.tool()
async def get_conformers_by_cid(cid: str):
    """检索给定 PubChem 化合物 CID 的可用构象异构体标识符。
    构象异构体表示为化合物计算或提供的不同 3D 几何结构。
    
    Args:
        cid: PubChem 化合物 ID（整数或字符串）
    
    Returns:
        包含以下内容的字典：
        - InformationList:
            • Information: 条目列表，每个包含：
                - CID:          PubChem 化合物 ID
                - ConformerID:  化合物的构象异构体标识符列表
    
    Query example:
        {"cid": "2244"}
    """


    try:
        result = pubchem_api.get_conformers_by_cid(cid)
    except Exception as e:
        return {"error": f"An error occurred while getting conformers by CID: {str(e)}"}
    return result

@mcp.tool()
async def get_compounds_by_smiles(smiles: str):
    """基于给定的 SMILES 字符串从 PubChem 检索化合物对象。
    每个返回的对象代表一个匹配的化合物条目。
    
    Args:
        smiles: 查询结构的 SMILES 字符串（例如 "CCO" 表示乙醇）
    
    Returns:
        与 SMILES 查询匹配的化合物对象列表。
        例如，"Compound(702)" 表示 CID 为 702 的 PubChem 化合物。
    
    Query example:
        {"smiles": "CCO"}
    """


    try:
        result = pubchem_api.get_compounds_by_smiles(smiles)
    except Exception as e:
        return {"error": f"An error occurred while getting compounds by SMILES: {str(e)}"}
    return result

@mcp.tool()
async def get_compounds_by_formula(formula: str):
    """基于分子式从 PubChem 检索化合物对象。
    响应返回匹配的化合物条目列表。
    
    Args:
        formula: 分子式字符串（例如 "C2H6O"）
    
    Returns:
        与分子式匹配的化合物对象列表。
        每个条目表示为 "Compound(<CID>)"，其中 <CID> 是 PubChem 化合物 ID。
    
    Query example:
        {"formula": "C2H6O"}
    """


    try:
        result = pubchem_api.get_compounds_by_formula(formula)
    except Exception as e:
        return {"error": f"An error occurred while getting compounds by formula: {str(e)}"}
    return result

@mcp.tool()
async def get_molecular_formula(compound):
    """获取化合物的分子式。
    
    Args:
        compound: PubChemPy 化合物对象
            
    Returns:
        化合物的分子式
    """
    try:
        result = pubchem_api.get_molecular_formula(compound)
    except Exception as e:
        return {"error": f"An error occurred while getting molecular formula: {str(e)}"}
    return result

@mcp.tool()
async def get_molecular_weight(compound):
    """获取化合物的分子量。
    
    Args:
        compound: PubChemPy 化合物对象
            
    Returns:
        化合物的分子量
    """
    try:
        result = pubchem_api.get_molecular_weight(compound)
    except Exception as e:
        return {"error": f"An error occurred while getting molecular weight: {str(e)}"}
    return result

@mcp.tool()
async def get_isomeric_smiles(compound):
    """获取化合物的异构 SMILES。
    
    Args:
        compound: PubChemPy 化合物对象
            
    Returns:
        化合物的异构 SMILES
    """
    try:
        result = pubchem_api.get_isomeric_smiles(compound)
    except Exception as e:
        return {"error": f"An error occurred while getting isomeric SMILES: {str(e)}"}
    return result

@mcp.tool()
async def get_xlogp(compound):
    """获取化合物的 XLogP 值。
    
    Args:
        compound: PubChemPy 化合物对象
            
    Returns:
        化合物的 XLogP 值
    """
    try:
        result = pubchem_api.get_xlogp(compound)
    except Exception as e:
        return {"error": f"An error occurred while getting XLogP: {str(e)}"}
    return result

@mcp.tool()
async def get_iupac_name(compound):
    """获取化合物的 IUPAC 名称。
    
    Args:
        compound: PubChemPy 化合物对象
            
    Returns:
        化合物的 IUPAC 名称
    """
    try:
        result = pubchem_api.get_iupac_name(compound)
    except Exception as e:
        return {"error": f"An error occurred while getting IUPAC name: {str(e)}"}
    return result

@mcp.tool()
async def get_synonyms(compound):
    """获取化合物的同义词。
    
    Args:
        compound: PubChemPy 化合物对象
            
    Returns:
        化合物的同义词列表
    """
    try:
        result = pubchem_api.get_synonyms(compound)
    except Exception as e:
        return {"error": f"An error occurred while getting synonyms: {str(e)}"}
    return result

@mcp.tool()
async def get_cids_by_smiles(smiles: str):
    """获取与药物 SMILES 对应的 CID。
    
    Args:
        smiles: SMILES 表示法
        
    Returns:
        CID 列表
    
    Args:
        smiles: SMILES（字符串）
    
    Query example: {"smiles": "CC(=O)OC1=CC=CC=C1C(=O)O"}
    
    Returns:
        CID 列表
    """


    try:
        result = pubchem_api.get_cids_by_smiles(smiles)
    except Exception as e:
        return {"error": f"An error occurred while getting CIDs by SMILES: {str(e)}"}
    return result

@mcp.tool()
async def get_cids_by_formula(formula: str):
    """通过分子式获取 CID 列表。
    
    Args:
        formula: 药物的分子式（字符串）
    
    Query example: {"formula": "C9H8O4"}
    
    Returns:
        CID 列表
    """


    try:
        result = pubchem_api.get_cids_by_formula(formula)
    except Exception as e:
        return {"error": f"An error occurred while getting CIDs by formula: {str(e)}"}
    return result

@mcp.tool()
async def get_sids_by_name(name: str):
    """通过名称获取 SID 列表。
    
    Args:
        name: 物质名称
    
    Query example: {"name": "aspirin"}
    
    Returns:
        包含以下字段的字典：
            CID: 药物的 CID
            SID: SID 列表
    """


    try:
        result = pubchem_api.get_sids_by_name(name)
    except Exception as e:
        return {"error": f"An error occurred while getting SIDs by name: {str(e)}"}
    return result

@mcp.tool()
async def get_substance_by_sid_pcp(sid: str):
    """使用 PubChemPy 通过 SID 获取物质对象。
    
    Args:
        sid: PubChem 物质 ID
        
    Returns:
        PubChemPy 物质对象（但此工具返回 Substance(sid)）
    
    Query example: {"sid": 4594}
    """


    try:
        result = pubchem_api.get_substance_by_sid(sid)
    except Exception as e:
        return {"error": f"An error occurred while getting substance by SID (PubChemPy): {str(e)}"}
    return result

@mcp.tool()
async def get_substances_by_name_pcp(name: str):
    """使用 PubChemPy 通过名称获取物质对象列表。
    
    Args:
        name: 物质名称
        
    Returns:
        PubChemPy 物质对象列表（元素为 "Substance(sid)" 的列表）
    
    Query example: {"name": "aspirin"}
    """


    try:
        result = pubchem_api.get_substances_by_name(name)
    except Exception as e:
        return {"error": f"An error occurred while getting substances by name (PubChemPy): {str(e)}"}
    return result

@mcp.tool()
async def get_substances_source_id(sid: str):
    """通过 SID 获取物质的来源 ID（原始数据库（例如 DrugBank、ChEMBL 等）分配给化合物或物质的唯一标识符）。
    
    Args:
        sid: PubChem 物质 ID
        
    Returns:
        物质的来源 ID
    
    Query example: {"sid": 123456}
    """


    try:
        result = pubchem_api.get_substances_source_id(sid)
    except Exception as e:
        return {"error": f"An error occurred while getting substance source ID: {str(e)}"}
    return result

@mcp.tool()
async def get_substances_synonyms(sid: str):
    """通过 SID 获取物质的同义词（同一化学物质的不同名称或标识符）。
    
    Args:
        sid: PubChem 物质 ID
        
    Returns:
        物质的同义词列表
    
    Query example: {"sid": 123456}
    """


    try:
        result = pubchem_api.get_substances_synonyms(sid)
    except Exception as e:
        return {"error": f"An error occurred while getting substance synonyms: {str(e)}"}
    return result

@mcp.tool()
async def get_compound_dict(compound, properties):
    """获取化合物性质的字典。
    
    Args:
        compound: PubChemPy 化合物对象
        properties: 要包含在字典中的性质名称列表
            
    Returns:
        包含化合物指定性质的字典
    """
    try:
        result = pubchem_api.get_compound_dict(compound, properties)
    except Exception as e:
        return {"error": f"An error occurred while getting compound dictionary: {str(e)}"}
    return result

@mcp.tool()
async def get_compounds_3d(name: str):
    """获取具有 3D 结构的化合物对象列表。
    
    Args:
        name: 化学名称
            
    Returns:
        具有 3D 结构的 PubChemPy 化合物对象列表
    """
    try:
        result = pubchem_api.get_compounds_3d(name)
    except Exception as e:
        return {"error": f"An error occurred while getting 3D compounds: {str(e)}"}
    return result

@mcp.tool()
async def get_compounds_dict(compound_cid: str):
    """通过 CID 获取化合物的字典表示。
    
    Args:
        compound_cid: PubChem 化合物 ID
        
    Returns:
        包含化合物信息的字典
    
    Query example: {"compound_cid": 962}
    """


    try:
        result = pubchem_api.get_compounds_dict(compound_cid)
    except Exception as e:
        return {"error": f"An error occurred while getting compound dictionary by CID: {str(e)}"}
    return result

@mcp.tool()
async def get_substructure_cas(smiles: str):
    """获取包含指定子结构的化合物的 CAS 注册号。
    
    Args:
        smiles: 子结构的 SMILES 表示法（字符串）
    
    Query example: {"smiles": "CN"}
    
    Returns:
        CAS 注册号列表
    """


    try:
        result = pubchem_api.get_substructure_cas(smiles)
    except Exception as e:
        return {"error": f"An error occurred while getting substructure CAS numbers: {str(e)}"}
    return result


@mcp.prompt()
def system_prompt():
    """客户端的系统提示。"""
    prompt = """你可以访问用于从 PubChem 搜索和检索化学信息的工具，PubChem 是一个化学分子及其针对生物测定活性的数据库。PubChem 由美国国立卫生研究院（NIH）下属的国家医学图书馆（NLM）的一个组成部分——国家生物技术信息中心（NCBI）维护。

你可以通过名称、SMILES 表示法、分子量或结构特征搜索化合物。你可以检索有关化合物的详细信息，包括其性质、同义词和描述。

使用 API 工具为用户的查询提取相关的化学信息。当用户询问化学品或药物时，尝试提供全面的信息，包括：
- 基本标识符（CID、分子式）
- 物理性质（分子量等）
- 通用名称和同义词
- 化学结构信息（如可用）
- 相关的生物活性（如相关）

如果用户没有提供缺失的参数，请用合理的值填充。"""
    return prompt
