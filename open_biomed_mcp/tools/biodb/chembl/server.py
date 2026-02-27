import json

from mcp.server.fastmcp import FastMCP
from tools.biodb.chembl.chembl_api import ChemblAPI

mcp = FastMCP(
    "chembl_mcp",
    stateless_http=True,
)
chembl_api = ChemblAPI()


@mcp.tool()
async def get_activity():
    """
    从 ChEMBL 数据库检索生物活性数据条目列表。注意：此工具不接受任何过滤参数，将返回整个数据库中前几个活性条目的默认列表。要搜索特定活性，请改用 'search_activity' 工具。
    
    Args:
    
    Query example: {}
    
    Returns:
        来自 ChEMBL 数据库的活性对象列表。
    """

    try:
        result = chembl_api.get_activity()
    except Exception as e:
        return [{"error": f"An error occurred while querying get_activity: {str(e)}"}]
    return result


@mcp.tool()
async def get_activity_by_id(activity_id: int):
    """
    通过唯一的活性 ID 从 ChEMBL 数据库检索单个生物活性条目的详细信息。
    
    Args:
        activity_id: ChEMBL 活性条目的唯一整数标识符。
    
    Query example: {"activity_id": 31863}
    
    Returns:
        包含指定活性条目详细属性的字典。
    """

    try:
        result = chembl_api.get_activity_by_id(activity_id)
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_activity_by_id: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_activity_by_ids(activity_ids: list[int]):
    """
    从 ChEMBL 数据库检索生物活性条目列表。注意：此工具目前无法按预期工作。它不会根据提供的 ID 列表正确过滤，而是返回数据库中的默认活性列表。
    
    Args:
        activity_ids: ChEMBL 活性条目的唯一整数标识符列表。
    
    Query example: {"activity_ids": [31863, 31864]}
    
    Returns:
        来自 ChEMBL 数据库的默认活性对象列表，不限于提供的 ID。
    """

    try:
        result = chembl_api.get_activity_by_ids(activity_ids)
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_activity_by_ids: {str(e)}"}
        ]
    return result


@mcp.tool()
async def search_activity(query_str: str):
    """
    使用查询字符串在 ChEMBL 数据库中对生物活性数据执行全文搜索。此工具可以搜索活性记录中的各个字段，例如检测描述、靶点名称或分子信息。
    
    Args:
        query_str: 搜索字符串。可以是关键字、靶点名称、期刊或预期在活性记录中找到的任何其他文本。
    
    Query example: {"query_str": "cyclooxygenase"}
    
    Returns:
        与搜索查询匹配的活性对象列表。
    """

    try:
        result = chembl_api.search_activity(query_str)
    except Exception as e:
        return [
            {"error": f"An error occurred while querying search_activity: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_activity_supplementary_data_by_activity():
    """
    从 ChEMBL 数据库检索补充生物活性数据的默认列表。注意：此工具存在缺陷，不接受任何过滤参数，会忽略任何提供的输入。要检索特定活性的数据，请改用 'get_activity_supplementary_data_by_activity_id' 工具。
    
    Args:
    
    Query example: {}
    
    Returns:
        来自 ChEMBL 数据库的补充活性数据对象的默认列表。
    """

    try:
        result = chembl_api.get_activity_supplementary_data_by_activity()
    except Exception as e:
        return [{"error": f"An error occurred while querying get_activity: {str(e)}"}]
    return result


@mcp.tool()
async def get_activity_supplementary_data_by_activity_by_id(activity_id: int):
    """
    通过 ID 检索单个活性补充数据对象的详细信息。
    
    Args:
        activity_id: 活性的唯一 ID（整数）
    
    Returns:
        活性补充数据对象的详细信息。
    """
    try:
        result = chembl_api.get_activity_supplementary_data_by_activity_by_id(
            activity_id
        )
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_activity_supplementary_data_by_activity_by_id: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_activity_supplementary_data_by_activity_by_ids(activity_ids: list[int]):
    """
    通过 ID 列表检索多个活性补充数据对象。
    
    Args:
        activity_ids: 活性的唯一 ID 列表
    
    Returns:
        活性补充数据对象列表。
    """
    try:
        result = chembl_api.get_activity_supplementary_data_by_activity_by_ids(
            activity_ids
        )
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_activity_supplementary_data_by_activity_by_ids: {str(e)}"
            }
        ]
    return result




@mcp.tool()
async def get_assay_by_id(assay_chembl_id: str):
    """
    使用唯一的 ChEMBL ID 从 ChEMBL 数据库检索单个检测（实验程序）的详细信息。
    
    Args:
        assay_chembl_id: 检测的唯一 ChEMBL 标识符（例如 'CHEMBL663853'）。必须是字符串。
    
    Query example: {"assay_chembl_id": "CHEMBL663853"}
    
    Returns:
        包含指定检测详细属性的字典。
    """

    try:
        result = chembl_api.get_assay_by_id(assay_chembl_id)
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_assay_by_id: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_assay_by_ids(assay_chembl_ids: list[str]):
    """
    使用唯一 ChEMBL ID 列表从 ChEMBL 数据库检索多个检测的详细信息。
    
    Args:
        assay_chembl_ids: 检测的唯一 ChEMBL 字符串标识符列表（例如 ['CHEMBL663853', 'CHEMBL872937']）。
    
    Query example: {"assay_chembl_ids": ["CHEMBL663853", "CHEMBL872937"]}
    
    Returns:
        字典列表，每个字典包含指定检测的详细属性。
    """

    try:
        result = chembl_api.get_assay_by_ids(assay_chembl_ids)
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_assay_by_ids: {str(e)}"}
        ]
    return result


@mcp.tool()
async def search_assay(query_str: str):
    """
    使用查询字符串在 ChEMBL 数据库中对检测（实验程序）执行全文搜索。可以搜索各种字段，如检测描述。
    
    Args:
        query_str: 搜索字符串，例如蛋白质名称如 'Heparanase' 或检测描述中的其他关键字。
    
    Query example: {"query_str": "Heparanase"}
    
    Returns:
        与搜索查询匹配的检测对象列表。
    """

    try:
        result = chembl_api.search_assay(query_str)
    except Exception as e:
        return [{"error": f"An error occurred while querying search_assay: {str(e)}"}]
    return result


@mcp.tool()
async def get_assay_class():
    """
    从 ChEMBL 数据库检索检测分类的默认列表。注意：此工具存在缺陷，不接受任何过滤参数，会忽略任何提供的输入。
    
    Args:
    
    Query example: {}
    
    Returns:
        来自 ChEMBL 数据库的检测分类对象的默认列表。
    """

    try:
        result = chembl_api.get_assay_class()
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_assay_class: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_assay_class_by_id(assay_class_id: int):
    """
    使用唯一整数 ID 从 ChEMBL 数据库检索单个检测分类的详细信息。
    
    Args:
        assay_class_id: 检测分类的唯一整数标识符。
    
    Query example: {"assay_class_id": 1}
    
    Returns:
        包含指定检测分类详细属性的字典。
    """

    try:
        result = chembl_api.get_assay_class_by_id(assay_class_id)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_assay_class_by_id: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_assay_class_by_ids(assay_class_ids: list[int]):
    """
    使用唯一整数 ID 列表从 ChEMBL 数据库检索多个检测分类的详细信息。
    
    Args:
        assay_class_ids: 检测分类的唯一整数标识符列表。
    
    Query example: {"assay_class_ids": [1, 2]}
    
    Returns:
        字典列表，每个字典包含指定检测分类的详细属性。
    """

    try:
        result = chembl_api.get_assay_class_by_ids(assay_class_ids)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_assay_class_by_ids: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_atc_class():
    """
    从 ChEMBL 数据库检索 ATC（解剖学治疗学化学分类系统）分类的默认列表。注意：此工具存在缺陷，不接受任何过滤参数，会忽略任何提供的输入。
    
    Args:
    
    Query example: {}
    
    Returns:
        来自 ChEMBL 数据库的 ATC 类对象的默认列表。
    """

    try:
        result = chembl_api.get_atc_class()
    except Exception as e:
        return [{"error": f"An error occurred while querying get_atc_class: {str(e)}"}]
    return result


@mcp.tool()
async def get_atc_class_by_id(level5: str):
    """
    从 ChEMBL 数据库检索单个 ATC（解剖学治疗学化学分类系统）分类的详细信息。注意：此工具名为 '_by_id'，但它通过 level 5 ATC 代码字符串搜索，而非数字 ID。
    
    Args:
        level5: 所需分类的 level 5 ATC 代码字符串（例如 'A01AA01'）。
    
    Query example: {"level5": "A01AA01"}
    
    Returns:
        包含指定 ATC 分类详细属性的字典。
    """

    try:
        result = chembl_api.get_atc_class_by_id(level5)
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_atc_class_by_id: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_atc_class_by_ids(level5s: list[str]):
    """
    使用 level 5 ATC 代码列表从 ChEMBL 数据库检索多个 ATC（解剖学治疗学化学分类系统）分类的详细信息。注意：此工具名为 '_by_ids'，但它通过 level 5 ATC 代码字符串列表搜索。
    
    Args:
        level5s: 所需分类的 level 5 ATC 代码字符串列表（例如 ['A01AA01', 'A01AA02']）。
    
    Query example: {"level5s": ["A01AA01", "A01AA02"]}
    
    Returns:
        字典列表，每个字典包含指定 ATC 分类的详细属性。
    """

    try:
        result = chembl_api.get_atc_class_by_ids(level5s)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_atc_class_by_ids: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_binding_site():
    """
    从 ChEMBL 数据库检索结合位点的默认列表。注意：此工具存在缺陷，不接受任何过滤参数，会忽略任何提供的输入。
    
    Args:
    
    Query example: {}
    
    Returns:
        来自 ChEMBL 数据库的结合位点对象的默认列表。
    """

    try:
        result = chembl_api.get_binding_site()
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_binding_site: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_binding_site_by_id(site_id: int):
    """
    使用唯一整数 ID 从 ChEMBL 数据库检索单个结合位点的详细信息。
    
    Args:
        site_id: 结合位点的唯一整数标识符。
    
    Query example: {"site_id": 2}
    
    Returns:
        包含指定结合位点详细属性的字典。
    """

    try:
        result = chembl_api.get_binding_site_by_id(site_id)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_binding_site_by_id: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_binding_site_by_ids(site_ids: list):
    """
    Retrieves detailed information for multiple binding sites from the ChEMBL database using a list of their unique integer IDs. Note: The schema for this tool does not explicitly define the type of items in the list, but it expects integers.
    
    Args:
        site_ids: A list of unique integer identifiers for the binding sites.
    
    Query example: {"site_ids": [2, 3]}
    
    Returns:
        A list of dictionaries, where each dictionary contains the detailed properties of a specified binding site.
    """

    try:
        result = chembl_api.get_binding_site_by_ids(site_ids)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_binding_site_by_ids: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_biotherapeutic():
    """
    Retrieves a default list of biotherapeutics from the ChEMBL database. Note: This tool is flawed as it does not accept any filtering parameters and ignores any provided input.
    
    Args:
    
    Query example: {}
    
    Returns:
        A default list of biotherapeutic objects from the ChEMBL database.
    """

    try:
        result = chembl_api.get_biotherapeutic()
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_biotherapeutic: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_biotherapeutic_by_id(molecule_chembl_id: str):
    """
    Retrieves the details for a single biotherapeutic from the ChEMBL database using its unique molecule ChEMBL ID.
    
    Args:
        molecule_chembl_id: The unique ChEMBL identifier (string) for the biotherapeutic.
    
    Query example: {"molecule_chembl_id": "CHEMBL448105"}
    
    Returns:
        A dictionary containing the detailed properties of the specified biotherapeutic.
    """

    try:
        result = chembl_api.get_biotherapeutic_by_id(molecule_chembl_id)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_biotherapeutic_by_id: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_biotherapeutic_by_ids(molecule_chembl_ids: list[str]):
    """
    Retrieves detailed information for multiple biotherapeutics from the ChEMBL database using a list of their unique molecule ChEMBL IDs.
    
    Args:
        molecule_chembl_ids: A list of unique ChEMBL identifier strings for the biotherapeutics.
    
    Query example: {"molecule_chembl_ids": ["CHEMBL448105", "CHEMBL266571"]}
    
    Returns:
        A list of dictionaries, where each dictionary contains the detailed properties of a specified biotherapeutic.
    """

    try:
        result = chembl_api.get_biotherapeutic_by_ids(molecule_chembl_ids)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_biotherapeutic_by_ids: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_cell_line():
    """
    从 ChEMBL 数据库检索细胞系的默认列表。注意：此工具存在缺陷，不接受任何过滤参数，会忽略任何提供的输入。
    
    Args:
    
    Query example: {}
    
    Returns:
        来自 ChEMBL 数据库的细胞系对象的默认列表。
    """

    try:
        result = chembl_api.get_cell_line()
    except Exception as e:
        return [{"error": f"An error occurred while querying get_cell_line: {str(e)}"}]
    return result


@mcp.tool()
async def get_cell_line_by_id(cell_id: int):
    """
    使用唯一整数 ID 从 ChEMBL 数据库检索单个细胞系的详细信息。
    
    Args:
        cell_id: 细胞系的唯一整数标识符。
    
    Query example: {"cell_id": 1}
    
    Returns:
        包含指定细胞系详细属性的字典。
    """

    try:
        result = chembl_api.get_cell_line_by_id(cell_id)
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_cell_line_by_id: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_cell_line_by_ids(cell_ids: list[int]):
    """
    使用唯一整数 ID 列表从 ChEMBL 数据库检索多个细胞系的详细信息。
    
    Args:
        cell_ids: 细胞系的唯一整数标识符列表。
    
    Query example: {"cell_ids": [1, 2]}
    
    Returns:
        字典列表，每个字典包含指定细胞系的详细属性。
    """

    try:
        result = chembl_api.get_cell_line_by_ids(cell_ids)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_cell_line_by_ids: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_chembl_id_lookup():
    """
    检索 chembl_id_lookup 对象列表。
    
    Args:
    
    Query example: {"kwargs": {}}
    
    Returns:
        XML 格式的数据，包含 ChEMBL ID 查找信息，包括标识符映射和相关属性
    """

    try:
        result = chembl_api.get_chembl_id_lookup()
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_chembl_id_lookup: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_chembl_id_lookup_by_id(chembl_id: str):
    """
    通过指定的 chembl_id 获取 ChEMBL 标识符映射，实现与 ChEMBL ID 关联的实体详细信息（例如化合物结构、靶点注释）的反向查找。
    
    Args:
        chembl_id: ChEMBL 标识符（例如 'CHEMBL123'）进行查询，格式为字符串（例如 'CHEMBL123'）
    
    
    Query example: {"chembl_id": "CHEMBL145"}
    
    Returns:
        返回一个 JSON 对象，包含映射到 chembl_id 的详细实体信息。
    """

    try:
        result = chembl_api.get_chembl_id_lookup_by_id(chembl_id)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_chembl_id_lookup_by_id: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_chembl_id_lookup_by_ids(chembl_ids: list[str]):
    """
    通过 ID 列表检索多个 chembl_id_lookup 对象。
    
    Args:
        chembl_ids: ChEMBL ID 数组进行查询（例如 ["CHEMBL145", "CHEMBL235"]）。每个 ID 必须遵循格式 CHEMBL[0-9]+
    
    
    Query example: {"chembl_ids": ["CHEMBL145", "CHEMBL235"]}
    
    Returns:
        返回包含批量查询结果的 JSON 对象。
    """

    try:
        result = chembl_api.get_chembl_id_lookup_by_ids(chembl_ids)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_chembl_id_lookup_by_ids: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def search_chembl_id_lookup(query_str: str):
    """
    使用查询字符串搜索 chemblidlookup。
    
    Args:
        query_str: Lucene 语法的搜索查询字符串（例如 'compound:aspirin' 或 'target_name:EGFR AND activity_value:<=10'）
    
    
    Query example: {"query_str": "compound:aspirin OR target_name:cyclooxygenase"}
    
    Returns:
        返回包含搜索结果的分页 JSON 响应。
    """

    try:
        result = chembl_api.search_chembl_id_lookup(query_str)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying search_chembl_id_lookup: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_chembl_release():
    """
    检索 chembl_release 对象列表。
    
    Args:
    
    Returns:
        返回包含发布元数据的 JSON 对象。
    """

    try:
        result = chembl_api.get_chembl_release()
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_chembl_release: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_chembl_release_by_id(chembl_release: str):
    """
    通过 ID 检索单个 chembl_release 对象的详细信息。
    
    Args:
        chembl_release: 表示 ChEMBL 发布版本的字符串（例如 "35"）。必须是有效的发布编号（例如与现有发布匹配的数字字符串）。
    
    
    Query example: {"chembl_release": "35"}
    
    Returns:
        返回包含指定发布的元数据的 JSON 对象。
    """

    try:
        result = chembl_api.get_chembl_release_by_id(chembl_release)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_chembl_release_by_id: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_chembl_release_by_ids(chembl_releases: list[str]):
    """
    通过 ID 列表检索多个 chembl_release 对象。
    
    Args:
        chembl_releases: ChEMBL 发布版本字符串数组（例如 ["35", "34"]）。每个版本必须是与现有发布匹配的有效数字字符串（例如 "35", "34"）。
    
    
    Query example: {"chembl_releases": ["35", "34"]}
    
    Returns:
        返回一个 JSON 对象，包含每个指定发布的元数据数组。
    """

    try:
        result = chembl_api.get_chembl_release_by_ids(chembl_releases)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_chembl_release_by_ids: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_compound_record():
    """
    检索化合物记录对象列表。
    
    Args: 
    
    Query example: {"chembl_id": "CHEMBL145"}
    
    Returns:
        返回包含全面化合物元数据的 JSON 对象。
    """

    try:
        result = chembl_api.get_compound_record()
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_compound_record: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_compound_record_by_id(record_id: int):
    """
    通过 ID 检索单个 compound_record 对象的详细信息。
    
    Args:
        record_id: 表示 ChEMBL 数据库中化合物内部记录 ID 的整数（例如 12345）。此 ID 与 ChEMBL ID（例如 CHEMBL145）不同。
    
    
    Query example: {"record_id": 12345}
    
    Returns:
        返回包含化合物元数据的 JSON 对象，类似于 get_compound_record，但通过内部记录 ID 链接。
    """

    try:
        result = chembl_api.get_compound_record_by_id(record_id)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_compound_record_by_id: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_compound_record_by_ids(record_ids: list[int]):
    """
    通过 ID 列表检索多个 compound_record 对象。
    
    Args:
        record_ids: 表示 ChEMBL 中化合物内部记录 ID 的整数值数组（例如 [12345, 67890]）。每个 ID 必须是数据库中的有效数字记录 ID。
    
    
    Query example: {"record_ids": [12345, 67890]}
    
    Returns:
        返回一个 JSON 对象，包含每个有效记录 ID 的化合物元数据数组。
    """

    try:
        result = chembl_api.get_compound_record_by_ids(record_ids)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_compound_record_by_ids: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_compound_structural_alert():
    """
    检索化合物结构警报对象列表。
    
    Args:
    
    Query example: {"chembl_id": "CHEMBL145"}
    
    Returns:
        返回包含化合物结构警报元数据的 JSON 对象。
    """

    try:
        result = chembl_api.get_compound_structural_alert()
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_compound_structural_alert: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_compound_structural_alert_by_id(cpd_str_alert_id: int):
    """
    通过 ID 检索化合物结构警报对象的详细信息。
    
    Args:
        cpd_str_alert_id: 表示 ChEMBL 数据库中结构警报内部 ID 的整数（例如 123）。此 ID 引用与化合物关联的特定子结构注释。
    
    
    Query example: {"cpd_str_alert_id": 123}
    
    Returns:
        返回包含结构警报详细信息的 JSON 对象。
    """

    try:
        result = chembl_api.get_compound_structural_alert_by_id(cpd_str_alert_id)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_compound_structural_alert_by_id: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_compound_structural_alert_by_ids(cpd_str_alert_ids: list[int]):
    """
    通过 ID 列表检索多个化合物结构警报对象。
    
    Args:
        cpd_str_alert_ids: 表示 ChEMBL 中结构警报内部 ID 的整数值数组（例如 [123, 456]）。每个 ID 引用与化合物关联的特定子结构注释。
    
    
    Query example: {"cpd_str_alert_ids": [1, 6]}
    
    Returns:
        返回一个 JSON 对象，包含每个有效 ID 的结构警报详细信息数组。
    """

    try:
        result = chembl_api.get_compound_structural_alert_by_ids(cpd_str_alert_ids)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_compound_structural_alert_by_ids: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_document():
    """
    检索文档对象列表。
    
    Args:
    
    Query example: {"document_chembl_id": "DOC123"}
    
    Returns:
        返回包含全面文档元数据的 JSON 对象。
    """

    try:
        result = chembl_api.get_document()
    except Exception as e:
        return [{"error": f"An error occurred while querying get_document: {str(e)}"}]
    return result


@mcp.tool()
async def get_document_by_id(document_chembl_id: str):
    """
    通过 ID 检索单个文档对象的详细信息。
    
    Args:
        document_chembl_id: 文档的 ChEMBL 标识符，格式为字符串（例如 'DOC123'）。ID 遵循模式 DOC[0-9]+（例如 DOC100, DOC256）。
    
    
    Query example: {"document_chembl_id": "DOC123"}
    
    Returns:
        返回包含全面文档元数据的 JSON 对象。
    """

    try:
        result = chembl_api.get_document_by_id(document_chembl_id)
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_document_by_id: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_document_by_ids(document_chembl_ids: list[str]):
    """
    通过 ID 列表检索多个文档对象。
    
    Args:
        document_chembl_ids: ChEMBL 文档标识符数组（例如 ['DOC123', 'DOC456']）。每个 ID 必须遵循格式 DOC[0-9]+（例如 DOC100, DOC256）。
    
    
    Query example: {"document_chembl_ids": ["DOC123", "DOC456"]}
    
    Returns:
        返回一个 JSON 对象，包含每个有效 ID 的文档元数据数组
    """

    try:
        result = chembl_api.get_document_by_ids(document_chembl_ids)
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_document_by_ids: {str(e)}"}
        ]
    return result


@mcp.tool()
async def search_document(query_str: str):
    """
    使用查询字符串搜索文档。
    
    Args:
        query_str: Lucene 语法的搜索查询字符串（例如 'aspirin AND 2020' 或 'title:cyclooxygenase'）。支持字段特定搜索（例如 `author:Smith`, `year:2022`）。
    
    
    Query example: {"query_str": "title:aspirin AND year:[2018 TO 2022]"}
    
    Returns:
        返回包含搜索结果的分页 JSON 响应。
    """

    try:
        result = chembl_api.search_document(query_str)
    except Exception as e:
        return [
            {"error": f"An error occurred while querying search_document: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_document_similarity():
    """
    检索文档相似度对象列表。
    
    Args:
    
    Query example: {"document_chembl_id": "DOC123"}
    
    Returns:
        返回包含相似文档和相似度分数的 JSON 对象。
    """

    try:
        result = chembl_api.get_document_similarity()
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_document_similarity: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_document_similarity_by_id(document_1_chembl_id: str):
    """
    通过 ID 检索单个文档相似度对象的详细信息。
    
    Args:
        document_1_chembl_id: 参考文档的 ChEMBL 标识符（例如 'DOC123'），用作相似度计算的基础。
    
    
    Query example: {"document_1_chembl_id": "DOC123"}
    
    Returns:
        返回包含相似度结果的 JSON 对象。
    """

    try:
        result = chembl_api.get_document_similarity_by_id(document_1_chembl_id)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_document_similarity_by_id: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_document_similarity_by_ids(document_1_chembl_ids: list[str]):
    """
    通过 ID 列表检索多个文档相似度对象。
    
    Args:
        document_1_chembl_ids: ChEMBL 文档标识符数组（例如 ['DOC123', 'DOC456']），用作相似度计算的参考点。每个 ID 必须遵循格式 DOC[0-9]+
    
    
    Query example: {"document_1_chembl_ids": ["DOC123", "DOC456"]}
    
    Returns:
        返回一个 JSON 对象，包含每个有效输入 ID 的相似度结果。
    """

    try:
        result = chembl_api.get_document_similarity_by_ids(document_1_chembl_ids)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_document_similarity_by_ids: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_drug():
    """
    检索药物对象列表。
    
    Args:
    
    Query example: {"drug_chembl_id": "DRUGB123"}
    
    Returns:
        返回包含全面药物元数据的 JSON 对象。
    """

    try:
        result = chembl_api.get_drug()
    except Exception as e:
        return [{"error": f"An error occurred while querying get_drug: {str(e)}"}]
    return result


@mcp.tool()
async def get_drug_by_id(molecule_chembl_id):
    """
    通过 ID 检索单个药物对象的详细信息。
    
    Args:
        molecule_chembl_id: 药物的 ChEMBL 标识符，格式为字符串（例如 'CHEMBL145'）。ID 遵循模式 CHEMBL[0-9]+（例如 CHEMBL100, CHEMBL256）。
    
    
    Query example: {"molecule_chembl_id": "CHEMBL145"}
    
    Returns:
        返回包含全面药物元数据的 JSON 对象。
    """

    try:
        result = chembl_api.get_drug_by_id(molecule_chembl_id)
    except Exception as e:
        return [{"error": f"An error occurred while querying get_drug_by_id: {str(e)}"}]
    return result


@mcp.tool()
async def get_drug_by_ids(molecule_chembl_ids: list[str]):
    """
    通过 ID 列表检索多个药物对象。
    
    Args:
        molecule_chembl_ids: 药物的 ChEMBL 标识符数组（例如 ['CHEMBL145', 'CHEMBL235']）。每个 ID 必须遵循格式 CHEMBL[0-9]+（例如 CHEMBL100, CHEMBL256）。
    
    
    Query example: {"molecule_chembl_ids": ["CHEMBL145", "CHEMBL235"]}
    
    Returns:
        返回一个 JSON 对象，包含每个有效 ID 的药物元数据数组。
    """

    try:
        result = chembl_api.get_drug_by_ids(molecule_chembl_ids)
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_drug_by_ids: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_drug_indication():
    """
    检索药物适应症对象列表。
    
    Args: 
    
    Query example: {"molecule_chembl_id": "CHEMBL145"}
    
    Returns:
        返回包含临床适应症数据的 JSON 对象。
    """

    try:
        result = chembl_api.get_drug_indication()
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_drug_indication: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_drug_indication_by_id(drugind_id: int):
    """
    通过 ID 检索药物适应症对象的详细信息。
    
    Args:
        drugind_id: 表示 ChEMBL 数据库中临床适应症内部 ID 的整数（例如 123）。此 ID 引用药物的特定治疗用途注释。
    
    
    Query example: {"drugind_id": 123}
    
    Returns:
        返回包含全面适应症详细信息的 JSON 对象。
    """

    try:
        result = chembl_api.get_drug_indication_by_id(drugind_id)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_drug_indication_by_id: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_drug_indication_by_ids(drugind_ids: list[int]):
    """
    通过 ID 列表检索多个药物适应症对象。
    
    Args:
        drugind_ids: 药物适应症对象的主键列表
    
    Returns:
        药物适应症对象列表。
    """
    try:
        result = chembl_api.get_drug_indication_by_ids(drugind_ids)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_drug_indication_by_ids: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_drug_warning():
    """
    检索 drug_warning 对象列表。
    
    Args: 
    
    Query example: {"molecule_chembl_id": "CHEMBL145"}
    
    Returns:
        返回包含全面安全警告数据的 JSON 对象。
    """

    try:
        result = chembl_api.get_drug_warning()
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_drug_warning: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_drug_warning_id(warning_id: int):
    """
    通过 ID 检索单个 drug_warning 对象的详细信息。
    
    Args:
        warning_id: 表示 ChEMBL 数据库中安全警告内部 ID 的整数（例如 789）。此 ID 引用药物的特定安全注释。
    
    
    Query example: {"warning_id": 145}
    
    Returns:
        返回包含全面警告详细信息的 JSON 对象。
    """

    try:
        result = chembl_api.get_drug_warning_id(warning_id)
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_drug_warning_id: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_drug_warning_ids(warning_ids: list[int]):
    """
    通过 ID 列表检索多个 drug_warning 对象。
    
    Args:
        warning_ids: 表示 ChEMBL 中安全警告内部 ID 的整数值数组（例如 [789, 910]）。每个 ID 引用药物的特定安全注释。
    
    
    Query example: {"warning_ids": [145, 910]}
    
    Returns:
        返回一个 JSON 对象，包含每个有效 ID 的警告元数据数组。
    """

    try:
        result = chembl_api.get_drug_warning_ids(warning_ids)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_drug_warning_ids: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_go_slim():
    """
    从 ChEMBL 数据库检索 GO（基因本体）精简分类的默认列表。注意：此工具存在缺陷，不接受任何过滤参数，会忽略任何提供的输入。
    
    Args:
    
    Query example: {}
    
    Returns:
        来自 ChEMBL 数据库的 GO 精简对象的默认列表。
    """

    try:
        result = chembl_api.get_go_slim()
    except Exception as e:
        return [{"error": f"An error occurred while querying get_go_slim: {str(e)}"}]
    return result


@mcp.tool()
async def get_go_slim_id(go_id: str):
    """
    使用唯一的 GO ID 从 ChEMBL 数据库检索单个 GO（基因本体）精简分类的详细信息。注意：此工具的命名（'_id'）与其他工具系列使用的 '_by_id' 约定不一致。
    
    Args:
        go_id: GO 精简术语的唯一 GO 标识符字符串（例如 'GO:0000003'）。
    
    Query example: {"go_id": "GO:0000003"}
    
    Returns:
        包含指定 GO 精简分类详细属性的字典。
    """

    try:
        result = chembl_api.get_go_slim_id(go_id)
    except Exception as e:
        return [{"error": f"An error occurred while querying get_go_slim_id: {str(e)}"}]
    return result


@mcp.tool()
async def get_go_slim_ids(go_ids: list[str]):
    """
    使用唯一 GO ID 列表从 ChEMBL 数据库检索多个 GO（基因本体）精简分类的详细信息。注意：此工具的命名（'_ids'）与其他工具系列使用的 '_by_ids' 约定不一致。
    
    Args:
        go_ids: GO 精简术语的唯一 GO 标识符字符串列表（例如 ['GO:0000003', 'GO:0000149']）。
    
    Query example: {"go_ids": ["GO:0000003", "GO:0000149"]}
    
    Returns:
        字典列表，每个字典包含指定 GO 精简分类的详细属性。
    """

    try:
        result = chembl_api.get_go_slim_ids(go_ids)
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_go_slim_ids: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_mechanism():
    """
    从 ChEMBL 数据库检索作用机制的默认列表。注意：此工具存在缺陷，不接受任何过滤参数，会忽略任何提供的输入。
    
    Args:
    
    Query example: {}
    
    Returns:
        来自 ChEMBL 数据库的机制对象的默认列表。
    """

    try:
        result = chembl_api.get_mechanism()
    except Exception as e:
        return [{"error": f"An error occurred while querying get_mechanism: {str(e)}"}]
    return result


@mcp.tool()
async def get_mechanism_id(mec_id: int):
    """
    从 ChEMBL 数据库检索单个药物作用机制的详细信息。注意：此工具的命名（'_id'）与其他工具系列使用的 '_by_id' 约定不一致。
    
    Args:
        mec_id: 药物作用机制的唯一整数标识符。
    
    Query example: {"mec_id": 13}
    
    Returns:
        包含指定机制详细属性的字典。
    """

    try:
        result = chembl_api.get_mechanism_id(mec_id)
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_mechanism_id: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_mechanism_ids(mec_ids: list[int]):
    """
    使用唯一整数 ID 列表从 ChEMBL 数据库检索多个药物作用机制的详细信息。注意：此工具的命名（'_ids'）与其他工具系列使用的 '_by_ids' 约定不一致。
    
    Args:
        mec_ids: 药物作用机制的唯一整数标识符列表。
    
    Query example: {"mec_ids": [13, 14]}
    
    Returns:
        字典列表，每个字典包含指定机制的详细属性。
    """

    try:
        result = chembl_api.get_mechanism_ids(mec_ids)
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_mechanism_ids: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_metabolism():
    """
    从 ChEMBL 数据库检索代谢记录的默认列表。注意：此工具存在缺陷，不接受任何过滤参数，会忽略任何提供的输入。
    
    Args:
    
    Query example: {}
    
    Returns:
        来自 ChEMBL 数据库的代谢对象的默认列表。
    """

    try:
        result = chembl_api.get_metabolism()
    except Exception as e:
        return [{"error": f"An error occurred while querying get_metabolism: {str(e)}"}]
    return result


@mcp.tool()
async def get_metabolism_id(met_id: int):
    """
    通过 ID 检索单个代谢对象的详细信息。
    
    Args:
        met_id: 代谢的主键
    
    Returns:
        代谢对象的详细信息。
    """
    try:
        result = chembl_api.get_metabolism_id(met_id)
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_metabolism_id: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_metabolism_ids(met_ids: list[int]):
    """
    使用唯一整数 ID 列表从 ChEMBL 数据库检索多个药物代谢记录的详细信息。注意：此工具的命名（'_ids'）与其他工具系列使用的 '_by_ids' 约定不一致。
    
    Args:
        met_ids: 药物代谢记录的唯一整数标识符列表。
    
    Query example: {"met_ids": [119, 120]}
    
    Returns:
        字典列表，每个字典包含指定代谢记录的详细属性。
    """

    try:
        result = chembl_api.get_metabolism_ids(met_ids)
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_metabolism_ids: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_molecule():
    """
    从 ChEMBL 数据库检索分子的默认列表。注意：此工具存在缺陷，不接受任何过滤参数，会忽略任何提供的输入。要查找特定分子，请使用 'search_molecule' 工具。
    
    Args:
    
    Query example: {}
    
    Returns:
        来自 ChEMBL 数据库的分子对象的默认列表。
    """

    try:
        result = chembl_api.get_molecule()
    except Exception as e:
        return [{"error": f"An error occurred while querying get_molecule: {str(e)}"}]
    return result


@mcp.tool()
async def get_molecule_id(molecule_chembl_id: str):
    """
    使用唯一的分子 ChEMBL ID 从 ChEMBL 数据库检索单个分子的详细信息。注意：此工具的命名（'_id'）与其他工具系列使用的 '_by_id' 约定不一致。
    
    Args:
        molecule_chembl_id: 分子的唯一 ChEMBL 标识符（字符串）。
    
    Query example: {"molecule_chembl_id": "CHEMBL6329"}
    
    Returns:
        包含指定分子详细属性的字典。
    """

    try:
        result = chembl_api.get_molecule_id(molecule_chembl_id)
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_molecule_id: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_molecule_ids(molecule_chembl_ids: list[str]):
    """
    使用唯一分子 ChEMBL ID 列表从 ChEMBL 数据库检索多个分子的详细信息。注意：此工具的命名（'_ids'）与其他工具系列使用的 '_by_ids' 约定不一致。
    
    Args:
        molecule_chembl_ids: 分子的唯一 ChEMBL 标识符字符串列表。
    
    Query example: {"molecule_chembl_ids": ["CHEMBL6329", "CHEMBL19"]}
    
    Returns:
        字典列表，每个字典包含指定分子的详细属性。
    """

    try:
        result = chembl_api.get_molecule_ids(molecule_chembl_ids)
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_molecule_ids: {str(e)}"}
        ]
    return result


@mcp.tool()
async def search_molecule(query_str: str):
    """
    使用查询字符串在 ChEMBL 数据库中对分子执行全文搜索。可以搜索各种字段，如首选名称、同义词或其他分子属性。
    
    Args:
        query_str: 搜索字符串，例如分子名称如 'METHAZOLAMIDE'。
    
    Query example: {"query_str": "METHAZOLAMIDE"}
    
    Returns:
        与搜索查询匹配的分子对象列表。
    """

    try:
        result = chembl_api.search_molecule(query_str)
    except Exception as e:
        return [
            {"error": f"An error occurred while querying search_molecule: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_molecule_form():
    """
    从 ChEMBL 数据库检索分子形式的默认列表。注意：此工具存在缺陷，不接受任何过滤参数，会忽略任何提供的输入。
    
    Args:
    
    Query example: {}
    
    Returns:
        来自 ChEMBL 数据库的分子形式对象的默认列表。
    """

    try:
        result = chembl_api.get_molecule_form()
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_molecule_form: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_molecule_form_id(molecule_chembl_id: str):
    """
    使用唯一的分子 ChEMBL ID 从 ChEMBL 数据库检索给定分子的分子形式信息。注意：此工具的命名（'_id'）与其他工具系列使用的 '_by_id' 约定不一致。
    
    Args:
        molecule_chembl_id: 分子的唯一 ChEMBL 标识符（字符串）。
    
    Query example: {"molecule_chembl_id": "CHEMBL6329"}
    
    Returns:
        包含分子形式详细信息的字典列表。
    """

    try:
        result = chembl_api.get_molecule_form_id(molecule_chembl_id)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_molecule_form_id: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_molecule_form_ids(molecule_chembl_ids: list[str]):
    """
    使用唯一分子 ChEMBL ID 列表从 ChEMBL 数据库检索多个分子的分子形式信息。注意：此工具的命名（'_ids'）与其他工具系列使用的 '_by_ids' 约定不一致。
    
    Args:
        molecule_chembl_ids: 分子的唯一 ChEMBL 标识符字符串列表。
    
    Query example: {"molecule_chembl_ids": ["CHEMBL6329", "CHEMBL6328"]}
    
    Returns:
        字典列表，每个字典包含给定输入 ID 的分子形式详细信息。
    """

    try:
        result = chembl_api.get_molecule_form_ids(molecule_chembl_ids)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_molecule_form_ids: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_organism():
    """
    从 ChEMBL 数据库检索生物体的默认列表。注意：此工具存在缺陷，不接受任何过滤参数，会忽略任何提供的输入。
    
    Args:
    
    Query example: {}
    
    Returns:
        来自 ChEMBL 数据库的生物体对象的默认列表。
    """

    try:
        result = chembl_api.get_organism()
    except Exception as e:
        return [{"error": f"An error occurred while querying get_organism: {str(e)}"}]
    return result


@mcp.tool()
async def get_organism_id(oc_id: int):
    """
    使用唯一整数 ID 从 ChEMBL 数据库检索单个生物体的详细信息。注意：此工具的命名（'_id'）与其他工具系列使用的 '_by_id' 约定不一致。
    
    Args:
        oc_id: 生物体的唯一整数标识符。
    
    Query example: {"oc_id": 1}
    
    Returns:
        包含指定生物体详细属性的字典。
    """

    try:
        result = chembl_api.get_organism_id(oc_id)
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_organism_id: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_organism_ids(oc_ids: list[int]):
    """
    使用唯一整数 ID 列表从 ChEMBL 数据库检索多个生物体的详细信息。注意：此工具的命名（'_ids'）与其他工具系列使用的 '_by_ids' 约定不一致。
    
    Args:
        oc_ids: 生物体的唯一整数标识符列表。
    
    Query example: {"oc_ids": [1, 2]}
    
    Returns:
        字典列表，每个字典包含指定生物体的详细属性。
    """

    try:
        result = chembl_api.get_organism_ids(oc_ids)
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_organism_ids: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_protein_classification():
    """
    从 ChEMBL 数据库检索蛋白质分类的默认列表。注意：此工具存在缺陷，不接受任何过滤参数，会忽略任何提供的输入。
    
    Args:
    
    Query example: {}
    
    Returns:
        来自 ChEMBL 数据库的蛋白质分类对象的默认列表。
    """

    try:
        result = chembl_api.get_protein_classification()
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_protein_classification: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_protein_classification_id(protein_class_id: int):
    """
    使用唯一整数 ID 从 ChEMBL 数据库检索单个蛋白质分类的详细信息。注意：此工具的命名（'_id'）与其他工具系列使用的 '_by_id' 约定不一致。
    
    Args:
        protein_class_id: 蛋白质分类的唯一整数标识符。
    
    Query example: {"protein_class_id": 1}
    
    Returns:
        包含指定蛋白质分类详细属性的字典。
    """

    try:
        result = chembl_api.get_protein_classification_id(protein_class_id)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_protein_classification_id: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_protein_classification_ids(protein_class_ids: list[int]):
    """
    使用唯一整数 ID 列表从 ChEMBL 数据库检索多个蛋白质分类的详细信息。注意：此工具的命名（'_ids'）与其他工具系列使用的 '_by_ids' 约定不一致。
    
    Args:
        protein_class_ids: 蛋白质分类的唯一整数标识符列表。
    
    Query example: {"protein_class_ids": [0, 1]}
    
    Returns:
        字典列表，每个字典包含指定蛋白质分类的详细属性。
    """

    try:
        result = chembl_api.get_protein_classification_ids(protein_class_ids)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_protein_classification_ids: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def search_protein_classification(query_str: str):
    """
    使用查询字符串搜索 protein_classification 对象。
    
    Args:
        query_str: protein_classification 的查询字符串数据值（例如定义）
        type: string
    
    Query example: {"query_str": "kinase"}
    
    Returns:
        字典列表，每个字典包含分类详细信息，包括 protein_class_id、pref_name 和层次级别。
    """

    try:
        result = chembl_api.search_protein_classification(query_str)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying search_protein_classification: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_similarity_smiles(standard_inchi_key: str, similarity: int):
    """
    通过 ID 检索单个相似度对象的详细信息。
    
    Args:
        standard_inchi_key: 化合物的 IUPAC 标准 InChI 键
        similarity: 指定相似度阈值的固定精度数值数据
        type_of_standard_inchi_key: string
        type_of_similarity: integer
    
    Query example: {"standard_inchi_key": "CCO", "similarity": 85}
    
    Returns:
        具有相似度分数和元数据的化合物列表
    """

    try:
        result = chembl_api.get_similarity_smiles(standard_inchi_key, similarity)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_similarity_smiles: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_source():
    """
    检索 source 对象列表。
    
    Args:
    
    Returns:
        包含 src_id、src_description、src_short_name 等的字典列表。
    """

    try:
        result = chembl_api.get_source()
    except Exception as e:
        return [{"error": f"An error occurred while querying get_source: {str(e)}"}]
    return result


@mcp.tool()
async def get_source_id(src_id: int):
    """
    通过 ID 检索单个 source 对象的详细信息。
    
    Args:
        src_id: 每个来源的标识符（用于 compound_records 和 assays 表）
        type: integer
    
    Query example: {"src_id": 1}
    
    Returns:
        包含 src_id、src_description 等的字典。
    """

    try:
        result = chembl_api.get_source_id(src_id)
    except Exception as e:
        return [{"error": f"An error occurred while querying get_source_id: {str(e)}"}]
    return result


@mcp.tool()
async def get_source_ids(src_ids: list[int]):
    """
    通过 ID 列表检索多个 source 对象的详细信息。
    
    Args:
        src_ids: 来源的 src 标识符列表
        type: array
    
    Query example: {"src_ids": [1, 2, 3]}
    
    Returns:
        来源字典列表，包括 src_short_name、src_comment、src_description
    """

    try:
        result = chembl_api.get_source_ids(src_ids)
    except Exception as e:
        return [{"error": f"An error occurred while querying get_source_ids: {str(e)}"}]
    return result


@mcp.tool()
async def get_status():
    """
    检索 status 对象列表。
    
    Args:
    
    Returns:
        状态字典列表，包括 activities、chembl_db_version、chembl_release_date、compound_records、disinct_compounds、publications、status 和 targets
    """

    try:
        result = chembl_api.get_status()
    except Exception as e:
        return [{"error": f"An error occurred while querying get_status: {str(e)}"}]
    return result


@mcp.tool()
async def substructure_info(molecule_chembl_id: str):
    """
    通过 ID 检索单个子结构对象的详细信息。
    
    Args:
        molecule_chembl_id: 子结构的 SMILES 字符串数据
        type: string
    
    Query example: {"molecule_chembl_id": "c1ccccc1"}
    
    Returns:
        化合物匹配列表，每个包含 molecule_chembl_id、pref_name、max_phase、molecule_type、first_approval、black_box_warning 等。
    """

    try:
        result = chembl_api.substructure_info(molecule_chembl_id)
    except Exception as e:
        return [
            {"error": f"An error occurred while querying substructure_info: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_target():
    """
    检索 target 对象列表。
    
    Args:
    
    Returns:
        包含 target_chembl_id、pref_name、organism、target_type、protein_classifications、target_components 等的字典列表。
    """

    try:
        result = chembl_api.get_target()
    except Exception as e:
        return [{"error": f"An error occurred while querying get_target: {str(e)}"}]
    return result


@mcp.tool()
async def get_target_id(target_chembl_id: str):
    """
    通过 ID 检索单个 target 对象的详细信息。
    
    Args:
        target_chembl_id: Target Chembl Id
        type: string
    
    Query example: {"target_chembl_id": "CHEMBL203"}
    
    Returns:
        包含 target_chembl_id、pref_name、organism、target_type、包含蛋白质/登录号信息的 target_components、protein_classifications 的字典
    """

    try:
        result = chembl_api.get_target_id(target_chembl_id)
    except Exception as e:
        return [{"error": f"An error occurred while querying get_target_id: {str(e)}"}]
    return result


@mcp.tool()
async def get_target_ids(target_chembl_ids: list[str]):
    """
    通过 ID 列表检索多个 target 对象。
    
    Args:
        target_chembl_ids: target_chembl_ids 列表
        type: array
    
    Query example: {"target_chembl_ids": ["CHEMBL203", "CHEMBL240", "CHEMBL210"]}
    
    Returns:
        包含 target_chembl_id、pref_name、organism、target_type、包含蛋白质/登录号信息的 target_components、protein_classifications 的字典列表
    """

    try:
        result = chembl_api.get_target_ids(target_chembl_ids)
    except Exception as e:
        return [{"error": f"An error occurred while querying get_target_ids: {str(e)}"}]
    return result


@mcp.tool()
async def search_target(query_str: str):
    """
    使用查询字符串搜索 target。
    
    Args:
        query_str: target 的字符串数据值（例如 pref_name）
        type: string
    
    Query example: {"query_str": "kinase"}
    
    Returns:
        匹配的 target 列表，每个包含 target_chembl_id、pref_name、organism、target_type、protein_classifications、target_components
    """

    try:
        result = chembl_api.search_target(query_str)
    except Exception as e:
        return [{"error": f"An error occurred while querying search_target: {str(e)}"}]
    return result


@mcp.tool()
async def get_target_component():
    """
    检索 target_component 对象列表。
    
    Args:
    
    Returns:
        字典列表，每个描述一个靶点组件（通常是蛋白质或其他生物分子），包括 component_chembl_id、UniProt 登录号 ID、component_type、物种名称、蛋白质家族分类列表、结构或描述性注释等字段
    """

    try:
        result = chembl_api.get_target_component()
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_target_component: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_target_component_id(component_id: int):
    """
    通过 ID 检索单个 target_component 对象的详细信息。
    
    Args:
        component_id: ChEMBL 组件 ID
        type: integer
    
    Query example: {"component_id": "135"}
    
    Returns:
        包含指定靶点组件详细信息的字典，包括：component_chembl_id（唯一组件 ID）、UniProt 登录号、物种名称、component_type、序列、tax ID 或交叉引用等附加元数据
    """

    try:
        result = chembl_api.get_target_component_id(component_id)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_target_component_id: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_target_component_ids(component_ids: list[int]):
    """
    通过 ID 列表检索多个 target_component 对象的详细信息。
    
    Args:
        component_ids: 组件的唯一标识符列表
        type: array
    
    Query example: {"component_ids": [135, 136, 137]}
    
    Returns:
        包含指定靶点组件详细信息的字典列表，包括：component_chembl_id（唯一组件 ID）、UniProt 登录号、物种名称、component_type、序列、tax ID 或交叉引用等附加元数据
    """

    try:
        result = chembl_api.get_target_component_ids(component_ids)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_target_component_ids: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_target_relation():
    """
    检索 target relation 对象列表。
    
    Args:
    
    Returns:
        字典列表，每个描述一个靶点到靶点的关系，包括来源和目标 ChEMBL ID、关系类型以及可用的置信度级别等信息。
    """

    try:
        result = chembl_api.get_target_relation()
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_target_relation: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_target_relation_id(related_target_chembl_id: str):
    """
    通过 ID 检索单个 target_relation 对象的详细信息。
    
    Args:
        related_target_chembl_id: Related Target Chembl Id
        type: string
    
    Query example: {"related_target_chembl_id": "CHEMBL2096619"}
    
    Returns:
        包含靶点关系信息的字典，包括来源和目标 ChEMBL ID、关系类型以及任何相关注释。
    """

    try:
        result = chembl_api.get_target_relation_id(related_target_chembl_id)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_target_relation_id: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_target_relation_ids(related_target_chembl_ids: list[str]):
    """
    通过 ID 列表检索多个 target_relation 对象。
    
    Args:
        related_target_chembl_ids: related target chembl Ids 列表
        type: array
    
    Query example: {"related_target_chembl_ids": ["CHEMBL_TC_5607"]}
    
    Returns:
        字典列表，每个描述一个靶点到靶点的关系。每个字典包括靶点关系的唯一 ID、来源靶点的 ChEMBL ID、相关（子）靶点的 ChEMBL ID、关系类型、可用的 confidence_score、target_relation_type 等附加元数据
    """

    try:
        result = chembl_api.get_target_relation_ids(related_target_chembl_ids)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_target_relation_ids: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_tissue():
    """
    检索 tissue 对象列表。
    
    Args:
    
    Returns:
        字典列表，每个包含组织的信息，例如其 ChEMBL ID、名称、Uberon ID 和附加注释。
    """

    try:
        result = chembl_api.get_tissue()
    except Exception as e:
        return [{"error": f"An error occurred while querying get_tissue: {str(e)}"}]
    return result


@mcp.tool()
async def get_tissue_id(tissue_chembl_id: str):
    """
    通过 ID 检索单个 tissue 对象的详细信息。
    
    Args:
        tissue_chembl_id: Unicode 字符串数据，例如 tissue_chembl_id（字符串）
    
    Query example: {"tissue_chembl_id": "CHEMBL3559723"}
    
    Returns:
        包含组织信息的字典，例如其 pref_name、关联的 Uberon ID、bto_id、caloha_id、efo_id。
    """

    try:
        result = chembl_api.get_tissue_id(tissue_chembl_id)
    except Exception as e:
        return [{"error": f"An error occurred while querying get_tissue_id: {str(e)}"}]
    return result


@mcp.tool()
async def get_tissue_ids(tissue_chembl_ids: list[str]):
    """
    通过 ID 列表检索单个 tissue 对象的详细信息。
    
    Args:
        tissue_chembl_ids: unicode 字符串数据列表（Tissue Chembl Ids）
        type: array
    
    Query example: {"tissue_chembl_ids": ["CHEMBL3559723", "CHEMBL3307558", "CHEMBL3307556"]}
    """

    try:
        result = chembl_api.get_tissue_ids(tissue_chembl_ids)
    except Exception as e:
        return [{"error": f"An error occurred while querying get_tissue_ids: {str(e)}"}]
    return result


@mcp.tool()
async def get_xref_source():
    """
    检索 xref_source 对象列表。
    
    Args:
    
    Returns:
        字典列表，每个包含交叉引用来源的信息，例如其名称、描述、URL 和 ID 前缀。
    """

    try:
        result = chembl_api.get_xref_source()
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_xref_source: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_xref_source_id(xref_src_db: str):
    """
    通过 ID 检索单个 xref_source 对象的详细信息。
    
    Args:
        xref_src_db: 从 chembl 交叉引用的来源数据库名称
        type: string
    
    Query example: {"xref_src_db": "UniProt"}
    
    Returns:
        包含 xref 来源详细信息的字典，例如名称、描述、URL 和 ID 前缀。
    """

    try:
        result = chembl_api.get_xref_source_id(xref_src_db)
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_xref_source_id: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_xref_source_ids(xref_src_dbs: list[str]):
    """
    通过 ID 列表检索多个 xref_source 对象。
    
    Args:
        xref_src_dbs: 从 chembl 交叉引用的来源数据库名称列表（数组）
    
    Query example: {"xref_src_dbs": ["PDB", "UniProt"]}
    
    Returns:
        字典列表，每个包含一个 xref 来源的详细信息，例如名称、描述、URL 和 ID 前缀。
    """

    try:
        result = chembl_api.get_xref_source_ids(xref_src_dbs)
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_xref_source_ids: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_image(chembl_id: str):
    """
    获取由 ChEMBL ID 或标准 InChI 键指定的化合物图像。
    您可以指定可选参数：
    engine - 用于渲染的化学工具包，只能是 rdkit，默认：rdkit。
    dimensions - 图像大小（正方形图像边的长度）。不能超过 500，默认：500。
    ignoreCoords - 忽略 molfile 中编码的 2D 坐标，让化学工具包重新计算它们。
    
    Args:
        chembl_id: Chembl Id 或标准 InChI 键
        type_of_chembl_id: string
        smiles(optional): 有效的 SMILES
        type_of_smiles(optional): string
        engine(optional): 用于渲染的化学工具包，只能是 rdkit，默认：rdkit。
        dimensions(optional): 图像大小（正方形图像边的长度）。不能超过 500，默认：500。
        ignoreCoords(optional): 忽略 molfile 中编码的 2D 坐标，让化学工具包重新计算它们。
    
    Query example: {"chembl_id": "CHEMBL25"}
    
    Returns:
        返回表示化合物 2D 化学结构的图像文件（通常为 PNG 格式）。
    """

    try:
        result = chembl_api.get_image(chembl_id)
    except Exception as e:
        return [{"error": f"An error occurred while querying get_image: {str(e)}"}]
    return result


@mcp.tool()
async def get_compound_chembl_id_by_name(name: str):
    """
    通过名称获取化合物 ChEMBL ID。
    
    Args:
        name: 要搜索的化合物名称
        
    Query example: {"name": "aspirin"}
    
    Returns:
        如果找到则返回化合物的 ChEMBL ID，否则返回 "No compound found"
    """
    try:
        result = chembl_api.search_molecule(name)
        if isinstance(result, str):
            result = json.loads(result)
        chembl_id = result['molecules'][0]['molecule_chembl_id']
    except Exception as e:
        print(e)
        chembl_id = 'No compound found'
    return chembl_id


@mcp.prompt()
def system_prompt():
    """客户端的系统提示。"""
    prompt = """您可以访问用于搜索 CHEMBL 的工具：ChEMBL 数据 Web 服务。
    使用 API 工具提取相关信息。
    如果用户未提供缺失的参数，请用合理的值填充。"""
    return prompt


