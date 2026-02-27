from mcp import types
from mcp.server.fastmcp import FastMCP

from tools.biodb.pdb.pdb_api import PDBAPI


mcp = FastMCP(
    name="pdb_mcp",
    stateless_http=True,
)

pdb_api = PDBAPI()


# Entry-related tools
@mcp.tool()
async def pdb_get_structure(entry_id: str):
    """获取 PDB 条目的详细结构信息。
    
    Args:
        entry_id (str): 4 字符的 PDB 条目 ID（例如 "1CRN"、"1TUP"）
        
    Returns:
        List[types.TextContent]: 包含一个 TextContent 对象的列表，其中：
            - text: 结构信息的 JSON 字符串，包括：
                - 'rcsb_id': PDB ID
                - 'rcsb_accession_info': 登录号详情  
                - 'struct': 结构元数据
                - 'exptl': 实验详情
                - 'citation': 出版物信息
                - 'cell': 单位晶胞参数
                - 'symmetry': 对称性信息
                - 'pdbx_database_status': 条目状态
                
        如果未找到条目或发生错误，则返回空列表。
    
    Query example: {"entry_id": "1CRN"}
    """
    result = pdb_api.get_structure(entry_id)
    return result

@mcp.tool()
async def pdb_get_pubmed_annotations(entry_id: str):
    """获取 PDB 条目的 PubMed 文献注释。
    
    Args:
        entry_id (str): 4 字符的 PDB 条目 ID（例如 "1CRN"、"1TUP"）
        
    Returns:
        List[types.TextContent]: 包含一个 TextContent 对象的列表，其中：
            - text: PubMed 注释的 JSON 字符串，包括：
                - 'rcsb_id': PDB ID
                - 'pubmed': PubMed 文章列表，包含：
                    - 'id': PubMed ID
                    - 'title': 文章标题
                    - 'journal': 期刊信息
                    - 'authors': 作者列表
                    - 'year': 发表年份
                    
        如果未找到注释或发生错误，则返回空列表。
        
    Query example: {"entry_id": "1CRN"}
    """
    result = pdb_api.get_pubmed_annotations(entry_id)
    return result

# Entity-related tools
@mcp.tool()
async def pdb_get_polymer_entity(entry_id: str, entity_id: str):
    """获取 PDB 条目中聚合物实体的详细信息。
    
    Args:
        entry_id (str): 4 字符的 PDB 条目 ID（例如 "1CRN"、"1TUP"）
        entity_id (str): 聚合物实体标识符（通常为 "1"、"2" 等）
        
    Returns:
        List[types.TextContent]: 包含一个 TextContent 对象的列表，其中：
            - text: 聚合物实体信息的 JSON 字符串，包括：
                - 'entity': 
                    - 'id': 实体 ID
                    - 'type': 实体类型（例如 "polymer"）
                    - 'src_method': 来源方法
                    - 'pdbx_description': 描述
                    - 'pdbx_number_of_molecules': 分子数量
                    - 'pdbx_ec': EC 编号
                    - 'pdbx_mutation': 突变信息
                    - 'pdbx_fragment': 片段信息
                - 'rcsb_polymer_entity':
                    - 'container_identifiers': 容器信息
                    - 'entity_poly': 聚合物详情
                    
        如果未找到实体或发生错误，则返回空列表。
        
    Query example: {"entry_id": "1CRN", "entity_id": "1"}
    """
    result = pdb_api.get_polymer_entity(entry_id, entity_id)
    return result

@mcp.tool()
async def pdb_get_branched_entity(entry_id: str, entity_id: str):
    """获取 PDB 条目中分支实体的详细信息。
    
    Args:
        entry_id (str): 4 字符的 PDB 条目 ID（例如 "1CRN"、"1TUP"）
        entity_id (str): 分支实体标识符（通常为 "1"、"2" 等）
        
    Returns:
        List[types.TextContent]: 包含一个 TextContent 对象的列表，其中：
            - text: 分支实体信息的 JSON 字符串，包括：
                - 'entity':
                    - 'id': 实体 ID
                    - 'type': 实体类型（例如 "branched"）
                    - 'pdbx_description': 描述
                    - 'pdbx_number_of_molecules': 分子数量
                - 'rcsb_branched_entity':
                    - 'container_identifiers': 容器信息
                    - 'branched_entity': 分支详情
                    - 'branched_entity_instance_count': 实例数量
                    
        如果未找到实体或发生错误，则返回空列表。
        
    Query example: {"entry_id": "1CRN", "entity_id": "1"}
    """
    result = pdb_api.get_branched_entity(entry_id, entity_id)
    return result

@mcp.tool()
async def pdb_get_nonpolymer_entity(entry_id: str, entity_id: str):
    """获取 PDB 条目中非聚合物实体的详细信息。
    
    Args:
        entry_id (str): 4 字符的 PDB 条目 ID（例如 "1CRN"、"1TUP"）
        entity_id (str): 非聚合物实体标识符（通常为 "1"、"2" 等）
        
    Returns:
        List[types.TextContent]: 包含一个 TextContent 对象的列表，其中：
            - text: 非聚合物实体信息的 JSON 字符串，包括：
                - 'entity':
                    - 'id': 实体 ID
                    - 'type': 实体类型（例如 "non-polymer"）
                    - 'pdbx_description': 描述
                    - 'pdbx_number_of_molecules': 分子数量
                - 'rcsb_non_polymer_entity':
                    - 'container_identifiers': 容器信息
                    - 'non_polymer_comp': 化学组分详情
                    - 'non_polymer_entity_instance_count': 实例数量
                    
        如果未找到实体或发生错误，则返回空列表。
        
    Query example: {"entry_id": "1CRN", "entity_id": "1"}
    """
    result = pdb_api.get_non_polymer_entity(entry_id, entity_id)
    return result

# Entity instance tools
@mcp.tool()
async def pdb_get_polymer_entity_instance(entry_id: str, instance_id: str):
    """获取 PDB 条目中聚合物实体实例的详细信息。
    
    Args:
        entry_id (str): 4 字符的 PDB 条目 ID（例如 "1CRN"、"1TUP"）
        instance_id (str): 聚合物实体实例标识符（通常为 "1"、"2" 等）
        
    Returns:
        List[types.TextContent]: 包含一个 TextContent 对象的列表，其中：
            - text: 聚合物实体实例信息的 JSON 字符串，包括：
                - 'rcsb_polymer_entity_instance':
                    - 'id': 实例 ID
                    - 'asym_id': 不对称单元 ID
                    - 'auth_asym_id': 作者不对称单元 ID
                    - 'entity_id': 父实体 ID
                    - 'transformation': 变换矩阵
                    - 'struct_asym': 结构不对称单元信息
                    - 'rcsb_polymer_entity_instance_container_identifiers': 容器信息
                    
        如果未找到实例或发生错误，则返回空列表。
        
    Query example: {"entry_id": "1CRN", "instance_id": "1"}
    """
    result = pdb_api.get_polymer_entity_instance(entry_id, instance_id)
    return result

@mcp.tool()
async def pdb_get_branched_entity_instance(entry_id: str, instance_id: str):
    """获取 PDB 条目中分支实体实例的详细信息。
    
    Args:
        entry_id (str): 4 字符的 PDB 条目 ID（例如 "1CRN"、"1TUP"）
        instance_id (str): 分支实体实例标识符（通常为 "1"、"2" 等）
        
    Returns:
        List[types.TextContent]: 包含一个 TextContent 对象的列表，其中：
            - text: 分支实体实例信息的 JSON 字符串，包括：
                - 'rcsb_branched_entity_instance':
                    - 'id': 实例 ID
                    - 'asym_id': 不对称单元 ID
                    - 'auth_asym_id': 作者不对称单元 ID
                    - 'entity_id': 父实体 ID
                    - 'transformation': 变换矩阵
                    - 'struct_asym': 结构不对称单元信息
                    - 'rcsb_branched_entity_instance_container_identifiers': 容器信息
                    
        如果未找到实例或发生错误，则返回空列表。
        
    Query example: {"entry_id": "1CRN", "instance_id": "1"}
    """
    result = pdb_api.get_branched_entity_instance(entry_id, instance_id)
    return result

@mcp.tool()
async def pdb_get_nonpolymer_entity_instance(entry_id: str, instance_id: str):
    """获取 PDB 条目中非聚合物实体实例的详细信息。
    
    Args:
        entry_id (str): 4 字符的 PDB 条目 ID（例如 "1CRN"、"1TUP"）
        instance_id (str): 非聚合物实体实例标识符（通常为 "1"、"2" 等）
        
    Returns:
        List[types.TextContent]: 包含一个 TextContent 对象的列表，其中：
            - text: 非聚合物实体实例信息的 JSON 字符串，包括：
                - 'rcsb_non_polymer_entity_instance':
                    - 'id': 实例 ID
                    - 'asym_id': 不对称单元 ID
                    - 'auth_asym_id': 作者不对称单元 ID
                    - 'entity_id': 父实体 ID
                    - 'transformation': 变换矩阵
                    - 'struct_asym': 结构不对称单元信息
                    - 'rcsb_non_polymer_entity_instance_container_identifiers': 容器信息
                    
        如果未找到实例或发生错误，则返回空列表。
        
    Query example: {"entry_id": "1CRN", "instance_id": "1"}
    """
    result = pdb_api.get_non_polymer_entity_instance(entry_id, instance_id)
    return result

# Annotation tools
@mcp.tool()
async def pdb_get_uniprot_annotations(entry_id: str, entity_id: str):
    """获取 PDB 条目中聚合物实体的 UniProt 注释。
    
    Args:
        entry_id (str): 4 字符的 PDB 条目 ID（例如 "1CRN"、"1TUP"）
        entity_id (str): 聚合物实体标识符（通常为 "1"、"2" 等）
        
    Returns:
        List[types.TextContent]: 包含一个 TextContent 对象的列表，其中：
            - text: UniProt 注释的 JSON 字符串，包括：
                - 'rcsb_id': PDB ID
                - 'entity_id': 实体 ID
                - 'uniprot_accession': UniProt 登录号
                - 'uniprot_id': UniProt ID
                - 'uniprot_name': 蛋白质名称
                - 'uniprot_description': 蛋白质描述
                - 'uniprot_sequence': 蛋白质序列
                - 'uniprot_organism': 来源生物
                - 'uniprot_gene': 基因名称
                - 'uniprot_domain': 结构域注释
                
        如果未找到注释或发生错误，则返回空列表。
        
    Query example: {"entry_id": "1CRN", "entity_id": "1"}
    """
    result = pdb_api.get_uniprot_annotations(entry_id, entity_id)
    return result

@mcp.tool()
async def pdb_get_drugbank_annotations(component_id: str):
    """获取 PDB 中化学组分的 DrugBank 注释。
    
    Args:
        component_id (str): 3 字母化学组分 ID（例如 "ATP"、"HEM"）
        
    Returns:
        List[types.TextContent]: 包含一个 TextContent 对象的列表，其中：
            - text: DrugBank 注释的 JSON 字符串，包括：
                - 'drugbank_id': DrugBank ID
                - 'name': 药物名称
                - 'description': 药物描述
                - 'groups': 药物组别（例如已批准、实验性）
                - 'indication': 治疗适应症
                - 'pharmacology': 药理作用
                - 'mechanism_of_action': 作用机制描述
                - 'toxicity': 毒性信息
                - 'metabolism': 代谢途径
                - 'targets': 药物靶点列表，包含：
                    - 'uniprot_id': UniProt ID
                    - 'gene_name': 基因名称
                    - 'action': 药物对靶点的作用
                    
        如果未找到注释或发生错误，则返回空列表。
        
    Query example: {"component_id": "ATP"}
    """
    result = pdb_api.get_drugbank_annotations(component_id)
    return result

# Assembly tools
@mcp.tool()
async def pdb_get_structural_assembly(entry_id: str, assembly_id: str = "1"):
    """获取 PDB 条目的结构组装信息。
    
    Args:
        entry_id (str): 4 字符的 PDB 条目 ID（例如 "1CRN"、"1TUP"）
        assembly_id (str): 组装标识符（默认："1"）
        
    Returns:
        List[types.TextContent]: 包含一个 TextContent 对象的列表，其中：
            - text: 组装信息的 JSON 字符串，包括：
                - 'rcsb_struct_assembly':
                    - 'id': 组装 ID
                    - 'details': 组装描述
                    - 'method': 组装方法
                    - 'oligomeric_details': 寡聚状态
                    - 'polymer_entity_instance_count': 实例数量
                    - 'rcsb_struct_assembly_provenance': 来源信息
                    - 'rcsb_struct_assembly_container_identifiers': 容器信息
                - 'assemblies': 组装组件列表，包含：
                    - 'assembly_id': 组件 ID
                    - 'asym_id_list': 不对称单元 ID 列表
                    - 'transformation': 变换矩阵
                    
        如果未找到组装或发生错误，则返回空列表。
        
    Query example: {"entry_id": "1CRN", "assembly_id": "1"}
    """
    result = pdb_api.get_structural_assembly(entry_id, assembly_id)
    return result

# Interface tools
@mcp.tool()
async def pdb_get_polymer_interface(entry_id: str, assembly_id: str, interface_id: str):
    """获取 PDB 条目中聚合物界面的详细信息。
    
    Args:
        entry_id (str): 4 字符的 PDB 条目 ID（例如 "1CRN"、"1TUP"）
        assembly_id (str): 组装标识符（通常为 "1"、"2" 等）
        interface_id (str): 界面标识符（通常为 "1"、"2" 等）
        
    Returns:
        List[types.TextContent]: 包含一个 TextContent 对象的列表，其中：
            - text: 界面信息的 JSON 字符串，包括：
                - 'rcsb_interface_info':
                    - 'id': 界面 ID
                    - 'interface_area': 界面面积（单位：Å²）
                    - 'solvent_content': 溶剂含量百分比
                    - 'interface_type': 界面分类
                    - 'interface_chemistry': 化学组成
                - 'interface_partner':
                    - 'asym_id': 不对称单元 ID 列表
                    - 'entity_id': 实体 ID 列表
                    - 'interface_residues': 界面残基列表
                - 'interface_features':
                    - 'hydrogen_bonds': 氢键数量和详情
                    - 'salt_bridges': 盐桥数量和详情
                    - 'disulfide_bonds': 二硫键数量和详情
                    
        如果未找到界面或发生错误，则返回空列表。
        
    Query example: {"entry_id": "1CRN", "assembly_id": "1", "interface_id": "1"}
    """
    result = pdb_api.get_polymer_interface(entry_id, assembly_id, interface_id)
    return result

# Chemical component tools
@mcp.tool()
async def pdb_get_chemical_component(component_id: str):
    """获取 PDB 中化学组分的详细信息。
    
    Args:
        component_id (str): 3 字母化学组分 ID（例如 "ATP"、"HEM"）
        
    Returns:
        List[types.TextContent]: 包含一个 TextContent 对象的列表，其中：
            - text: 化学组分信息的 JSON 字符串，包括：
                - 'chem_comp':
                    - 'id': 组分 ID
                    - 'name': 组分名称
                    - 'type': 组分类型
                    - 'formula': 化学式
                    - 'formula_weight': 分子量
                    - 'pdbx_formal_charge': 形式电荷
                    - 'pdbx_initial_date': 添加日期
                    - 'pdbx_modified_date': 最后修改日期
                    - 'pdbx_release_status': 发布状态
                - 'pdbx_chem_comp_descriptor': 描述符
                - 'pdbx_chem_comp_identifier': 标识符
                - 'pdbx_chem_comp_feature': 特征
                - 'pdbx_chem_comp_audit': 审计信息
                - 'rcsb_chem_comp_container_identifiers': 容器信息
                - 'rcsb_chem_comp_related': 相关组分
                - 'rcsb_chem_comp_synonyms': 同义词
                    
        如果未找到组分或发生错误，则返回空列表。
        
    Query example: {"component_id": "ATP"}
    """
    result = pdb_api.get_chemical_component(component_id)
    return result

# Group tools
@mcp.tool()
async def pdb_get_aggregation_group_provenance(group_id: str):
    """获取 PDB 中聚合组的来源信息。
    
    Args:
        group_id (str): 聚合组标识符（例如 "1"、"2"）
        
    Returns:
        List[types.TextContent]: 包含一个 TextContent 对象的列表，其中：
            - text: 聚合组来源的 JSON 字符串，包括：
                - 'rcsb_aggregation_group_provenance':
                    - 'group_id': 组 ID
                    - 'aggregation_method': 使用的方法
                    - 'aggregation_criteria': 标准详情
                    - 'aggregation_version': 版本信息
                    - 'aggregation_date': 聚合日期
                    - 'aggregation_software': 使用的软件
                    - 'aggregation_parameters': 使用的参数
                    - 'aggregation_references': 参考信息
                    - 'aggregation_notes': 附加说明
                    
        如果未找到组或发生错误，则返回空列表。
        
    Query example: {"group_id": "1"}
    """
    result = pdb_api.get_aggregation_group_provenance(group_id)
    return result

@mcp.tool()
async def pdb_get_pdb_cluster_data_aggregation(cluster_id: str):
    """获取 PDB 聚类的数据聚合信息。
    
    Args:
        cluster_id (str): 聚类标识符（例如 "1"、"2"）
        
    Returns:
        List[types.TextContent]: 包含一个 TextContent 对象的列表，其中：
            - text: 聚类数据聚合的 JSON 字符串，包括：
                - 'rcsb_cluster_data_aggregation':
                    - 'cluster_id': 聚类 ID
                    - 'cluster_size': 成员数量
                    - 'cluster_method': 聚类方法
                    - 'cluster_cutoff': 相似性阈值
                    - 'cluster_members': 成员 PDB ID 列表
                    - 'cluster_representative': 代表性 PDB ID
                    - 'cluster_sequence_identity': 平均序列一致性
                    - 'cluster_rmsd': 平均结构 RMSD
                    - 'cluster_coverage': 序列覆盖度
                    
        如果未找到聚类或发生错误，则返回空列表。
        
    Query example: {"cluster_id": "1"}
    """
    result = pdb_api.get_pdb_cluster_data_aggregation(cluster_id)
    return result

@mcp.tool()
async def pdb_get_pdb_cluster_data_aggregation_method(method_id: str):
    """获取 PDB 聚类数据聚合方法的详细信息。
    
    Args:
        method_id (str): 方法标识符（例如 "sequence_identity"、"structure_similarity"）
        
    Returns:
        List[types.TextContent]: 包含一个 TextContent 对象的列表，其中：
            - text: 方法详情的 JSON 字符串，包括：
                - 'rcsb_cluster_data_aggregation_method':
                    - 'id': 方法 ID
                    - 'name': 方法名称
                    - 'description': 方法描述
                    - 'version': 方法版本
                    - 'parameters': 方法参数
                    - 'reference': 参考信息
                    - 'software': 使用的软件
                    - 'cutoff': 相似性阈值
                    - 'coverage': 序列覆盖度值
                    
        如果未找到方法或发生错误，则返回空列表。
        
    Query example: {"method_id": "sequence_identity"}
    """
    result = pdb_api.get_pdb_cluster_data_aggregation_method(method_id)
    return result

# Residue tools
@mcp.tool()
async def pdb_get_residue_chains(entry_id: str):
    """获取 PDB 条目的残基链信息。
    
    Args:
        entry_id (str): 4 字符的 PDB 条目 ID（例如 "1CRN"、"1TUP"）
        
    Returns:
        List[types.TextContent]: 包含一个 TextContent 对象的列表，其中：
            - text: 残基链信息的 JSON 字符串，包括：
                - 'rcsb_id': PDB ID
                - 'chains': 链列表，包含：
                    - 'asym_id': 不对称单元 ID
                    - 'auth_asym_id': 作者不对称单元 ID
                    - 'entity_id': 父实体 ID
                    - 'entity_type': 实体类型（聚合物/分支/非聚合物）
                    - 'residues': 残基列表，包含：
                        - 'residue_number': 残基编号
                        - 'residue_name': 残基名称
                        - 'chem_comp_id': 化学组分 ID
                        - 'pdbx_PDB_ins_code': 插入代码
                        - 'pdbx_formal_charge': 形式电荷
                        - 'pdbx_polymer_type': 聚合物类型
                    
        如果未找到链或发生错误，则返回空列表。
        
    Query example: {"entry_id": "1CRN"}
    """
    result = pdb_api.get_residue_chains(entry_id)
    return result

@mcp.tool()
async def pdb_get_entry_groups(group_id: str):
    """从 RCSB PDB 获取指定组沉积 ID 的详细组信息。
    
    Args:
        group_id (str): PDB 组沉积 ID（例如 "G_1002011"）
        
    Returns:
        List[types.TextContent]: 包含一个 TextContent 对象的列表，其中：
            - text: 包含以下内容的 JSON 字符串：
                - rcsb_id: 组级 RCSB 标识符
                - rcsb_group_container_identifiers: 组和成员 ID 关系
                    - group_id
                    - group_provenance_id
                    - parent_member_ids
                    - group_member_ids
                - rcsb_group_info: 名称、描述、粒度和成员数量
                - rcsb_group_statistics: 相似性分数阈值和分数范围
                - rcsb_group_accession_info: 版本信息
                - rcsb_group_related: 相关组结构（如有）
                
        如果未找到组或发生错误，则返回空列表。
        
    Query example: {"group_id": "G_1002011"}
    """
    result = pdb_api.get_entry_groups(group_id)
    return result

@mcp.tool()
async def pdb_get_polymer_entity_groups(group_id: str):
    """通过 UniProt ID 或序列聚类 ID 从 RCSB PDB 获取聚合物实体组。
    
    Args:
        group_id (str): UniProt ID（例如 "Q3Y9I6"）或 RCSB 序列聚类 ID
        
    Returns:
        List[types.TextContent]: 包含一个 TextContent 对象的列表，其中：
            - text: 包含以下内容的 JSON 字符串：
                - rcsb_id: 实体组标识符
                - rcsb_group_container_identifiers:
                    - group_id
                    - group_provenance_id
                    - parent_member_ids
                    - group_member_ids
                - rcsb_group_info:
                    - group_name
                    - group_description
                    - group_members_granularity（例如 assembly、chain）
                    - group_members_count
                - rcsb_group_statistics:
                    - similarity_cutoff
                    - similarity_score_min / max
                - rcsb_group_accession_info:
                    - version
                - rcsb_group_related: 相关组条目
                - rcsb_polymer_entity_group_members_rankings: 排名信息
                - rcsb_polymer_entity_group_sequence_alignment:
                    - abstract_reference: 参考序列信息
                    - group_members_alignment: 对齐的成员序列
                    
        如果未找到组或发生错误，则返回空列表。
        
    Query example: {"group_id": "Q3Y9I6"}
    """
    result = pdb_api.get_polymer_entity_groups(group_id)
    return result

@mcp.tool()
async def pdb_get_nonpolymer_entity_groups(group_id: str):
    """通过化学组分 ID 从 RCSB PDB 获取非聚合物实体组对象。
    
    Args:
        group_id (str): 化学组分 ID（例如 "HEM" 表示血红素基团）
        
    Returns:
        List[types.TextContent]: 包含一个 TextContent 对象的列表，其中：
            - text: 包含以下内容的 JSON 字符串：
                - rcsb_id: 组级标识符
                - rcsb_group_container_identifiers:
                    - group_id
                    - group_provenance_id
                    - parent_member_ids
                    - group_member_ids
                - rcsb_group_info:
                    - group_name
                    - group_description
                    - group_members_granularity
                    - group_members_count
                - rcsb_group_statistics:
                    - similarity_cutoff
                    - similarity_score_min / max
                - rcsb_group_accession_info:
                    - version
                - rcsb_group_related: 相关组（如有）
                - rcsb_polymer_entity_group_members_rankings: 排名信息
                - rcsb_polymer_entity_group_sequence_alignment:
                    - abstract_reference
                    - group_members_alignment
                    
        如果未找到组或发生错误，则返回空列表。
        
    Query example: {"group_id": "HEM"}
    """
    result = pdb_api.get_nonpolymer_entity_groups(group_id)
    return result

@mcp.prompt()
def system_prompt():
    return """你是蛋白质数据库（PDB）MCP 服务器。
    你可以使用 PDB API 回答有关蛋白质结构和相关数据的问题。
    始终在最终答案中包含工具调用的结果。"""
