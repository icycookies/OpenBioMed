"""
MCP Tools Registry
统一管理所有MCP工具服务的注册和FastAPI转换
"""

import logging
from typing import List, Dict, Any
from fastapi import APIRouter, FastAPI
from mcp.server.fastmcp import FastMCP

from mcp_to_fastapi import create_mcp_fastapi_router

logger = logging.getLogger(__name__)

BIOCOMPUTING_MODULE_NAME_MAP = {
    "literature": "文献检索相关",
    "biochemistry": "生物化学相关",
    "bioimaging": "生物成像相关",
    "bioengineering": "生物工程相关",
    "biophysics": "生物物理相关",
    "glycoengineering": "糖工程相关",
    "cancer_biology": "癌症生物学相关",
    "cell_biology": "细胞生物学相关",
    "molecular_biology": "分子生物学相关",
    "genetics": "遗传学相关",
    "genomics": "基因组学相关",
    "immunology": "免疫学相关",
    "microbiology": "微生物学相关",
    "pathology": "病理学相关",
    "pharmacology": "药理学相关",
    "physiology": "生理学相关",
    "synthetic_biology": "合成生物学相关",
    "systems_biology": "系统生物学相关",
    "support_tools": "辅助工具相关",
    "lab_automation": "实验室自动化相关",
}


class MCPToolsRegistry:
    """MCP工具注册中心"""
    
    def __init__(self):
        self.mcp_servers: List[FastMCP] = []
        self.tool_configs: List[Dict[str, Any]] = []
        
    def register_mcp_server(
        self,
        mcp_server: FastMCP,
        prefix: str,
        tags: List[str],
        description: str = ""
    ):
        """
        注册一个MCP服务器
        
        Args:
            mcp_server: FastMCP服务器实例
            prefix: API路径前缀，例如 "/chembl"
            tags: FastAPI标签列表
            description: 服务描述
        """
        self.mcp_servers.append(mcp_server)
        self.tool_configs.append({
            "mcp_server": mcp_server,
            "prefix": prefix,
            "tags": tags,
            "description": description
        })
        # logger.info(f"Registered MCP server: {mcp_server.name} at {prefix}")
    
    def create_fastapi_routers(self) -> List[APIRouter]:
        """
        为所有注册的MCP服务器创建FastAPI路由器
        
        Returns:
            APIRouter列表
        """
        routers = []
        for config in self.tool_configs:
            router = create_mcp_fastapi_router(
                mcp_server=config["mcp_server"],
                prefix=config["prefix"],
                tags=config["tags"]
            )
            routers.append(router)
        return routers
    
    def register_to_app(self, app: FastAPI, base_prefix: str = "/tools"):
        """
        将所有MCP工具注册到FastAPI应用
        
        Args:
            app: FastAPI应用实例
            base_prefix: 基础路径前缀，默认 "/tools"
        """
        routers = self.create_fastapi_routers()
        for router in routers:
            app.include_router(router, prefix=base_prefix)
            # logger.info(f"Included router with prefix: {base_prefix}")
    
    def get_tools_summary(self) -> Dict[str, Any]:
        """
        获取所有工具的摘要信息
        
        Returns:
            工具摘要字典
        """
        summary = {
            "total_servers": len(self.mcp_servers),
            "servers": []
        }
        
        for config in self.tool_configs:
            mcp_server = config["mcp_server"]
            
            # 区分 FastMCP 和 FastApiMCP 两种类型
            tools = {}
            if hasattr(mcp_server, '_tool_manager') and hasattr(mcp_server._tool_manager, '_tools'):
                # FastMCP 类型
                tools = mcp_server._tool_manager._tools
            elif hasattr(mcp_server, '_tools'):
                # FastApiMCP 类型
                tools = mcp_server._tools
            
            server_info = {
                "name": getattr(mcp_server, 'name', 'Unknown'),
                "prefix": config["prefix"],
                "tags": config["tags"],
                "description": config["description"],
                "tool_count": len(tools),
                "tools": list(tools.keys()) if tools else []
            }
            summary["servers"].append(server_info)
        
        return summary


# 创建全局注册中心实例
registry = MCPToolsRegistry()


def setup_mcp_tools():
    """
    设置所有MCP工具服务
    这个函数会导入所有工具的MCP服务器并注册到registry
    """
    # ChEMBL
    try:
        from tools.biodb.chembl.server import mcp as chembl_mcp
        registry.register_mcp_server(
            chembl_mcp,
            prefix="/chembl",
            tags=["生物活性相关"],
            description="ChEMBL数据库API - 生物活性数据"
        )
    except Exception as e:
        logger.warning(f"Failed to register chembl: {e}")
    
    # NCBI
    try:
        from tools.biodb.ncbi.server import mcp as ncbi_mcp
        registry.register_mcp_server(
            ncbi_mcp,
            prefix="/ncbi",
            tags=["基因相关"],
            description="NCBI数据库API - 基因和基因组数据"
        )
    except Exception as e:
        logger.warning(f"Failed to register ncbi: {e}")
    
    # PubChem
    try:
        from tools.biodb.pubchem.server import mcp as pubchem_mcp
        registry.register_mcp_server(
            pubchem_mcp,
            prefix="/pubchem",
            tags=["化合物信息相关"],
            description="PubChem数据库API - 化合物信息"
        )
    except Exception as e:
        logger.warning(f"Failed to register pubchem: {e}")
    
    # UniProt
    try:
        from tools.biodb.uniprot.server import mcp as uniprot_mcp
        registry.register_mcp_server(
            uniprot_mcp,
            prefix="/uniprot",
            tags=["蛋白质信息相关"],
            description="UniProt数据库API - 蛋白质信息"
        )
    except Exception as e:
        logger.warning(f"Failed to register uniprot: {e}")
    
    # KEGG
    try:
        from tools.biodb.kegg.server import mcp as kegg_mcp
        registry.register_mcp_server(
            kegg_mcp,
            prefix="/kegg",
            tags=["通路与基因组相关"],
            description="KEGG数据库API - 通路和基因组信息"
        )
    except Exception as e:
        logger.warning(f"Failed to register kegg: {e}")
    
    # STRING
    try:
        from tools.biodb.STRING.server import mcp as string_mcp
        registry.register_mcp_server(
            string_mcp,
            prefix="/string",
            tags=["蛋白质网络相关"],
            description="STRING数据库API - 蛋白质相互作用网络"
        )
    except Exception as e:
        logger.warning(f"Failed to register string: {e}")
    
    # Search
    try:
        from tools.biodb.search.server import mcp as search_mcp
        registry.register_mcp_server(
            search_mcp,
            prefix="/search_tools",
            tags=["搜索工具"],
            description="搜索工具 - Tavily和Jina搜索"
        )
    except Exception as e:
        logger.warning(f"Failed to register search: {e}")
    
    # TCGA
    try:
        from tools.biodb.tcga.server import mcp as tcga_mcp
        registry.register_mcp_server(
            tcga_mcp,
            prefix="/tcga",
            tags=["癌症基因组相关"],
            description="TCGA数据库API - 癌症基因组数据"
        )
    except Exception as e:
        logger.warning(f"Failed to register tcga: {e}")
    
    # Ensembl
    try:
        from tools.biodb.ensembl.server import mcp as ensembl_mcp
        registry.register_mcp_server(
            ensembl_mcp,
            prefix="/ensembl",
            tags=["基因组注释相关"],
            description="Ensembl数据库API - 基因组注释"
        )
    except Exception as e:
        logger.warning(f"Failed to register ensembl: {e}")
    
    # UCSC
    try:
        from tools.biodb.ucsc.server import mcp as ucsc_mcp
        registry.register_mcp_server(
            ucsc_mcp,
            prefix="/ucsc",
            tags=["基因组API相关"],
            description="UCSC基因组浏览器API"
        )
    except Exception as e:
        logger.warning(f"Failed to register ucsc: {e}")
    
    # ClinicalTrials
    try:
        from tools.biodb.clinicaltrials.server import mcp as clinicaltrials_mcp
        registry.register_mcp_server(
            clinicaltrials_mcp,
            prefix="/clinicaltrials",
            tags=["临床试验相关"],
            description="ClinicalTrials.gov API - 临床试验数据"
        )
    except Exception as e:
        logger.warning(f"Failed to register clinicaltrials: {e}")
    
    # PDB
    try:
        from tools.biodb.pdb.server import mcp as pdb_mcp
        registry.register_mcp_server(
            pdb_mcp,
            prefix="/pdb",
            tags=["蛋白质结构相关"],
            description="PDB数据库API - 蛋白质结构数据"
        )
    except Exception as e:
        logger.warning(f"Failed to register pdb: {e}")
    
    # DBSearch
    try:
        from tools.biodb.dbsearch.server import mcp as dbsearch_mcp
        registry.register_mcp_server(
            dbsearch_mcp,
            prefix="/dbsearch",
            tags=["数据库搜索相关"],
            description="数据库搜索工具"
        )
    except Exception as e:
        logger.warning(f"Failed to register dbsearch: {e}")
    
    # Biocomputing - 生物医学综合工具集
    try:
        from tools.biocomputing.mcp_to_fastapi import BiocomputingMcp
        
        
        biocomputing = BiocomputingMcp()
        
        # 为每个模块创建独立的 MCP 服务器
        biocomputing_servers = biocomputing.create_mcp_servers_per_module()
        
        # 注册每个模块的服务器
        registered_count = 0
        for module_name, mcp_server in biocomputing_servers.items():
            try:
                # 格式化模块名称用于显示 - 使用更明确的标签名称
                display_name = BIOCOMPUTING_MODULE_NAME_MAP.get(module_name, module_name.replace('_', '-').title())
                
                # 获取该服务器中的工具数量
                tool_count = len(mcp_server._tool_manager._tools)
                
                registry.register_mcp_server(
                    mcp_server,
                    prefix=f"/{module_name}",
                    tags=[display_name],    # fastapi中的类别标签
                    description=f"Biocomputing {module_name.replace('_', ' ').title()} 工具集"
                )
                registered_count += 1
                # logger.info(f"  ✓ Registered Biocomputing module: {module_name} ({tool_count} tools) with tag [{display_name}]")
            except Exception as e:
                logger.warning(f"Failed to register module {module_name}: {e}")
        
        # logger.info(f"Successfully registered {registered_count} Biocomputing module servers")
        
    except Exception as e:
        logger.warning(f"Failed to setup Biocomputing tools: {e}")
        import traceback
        traceback.print_exc()
    
    
    # logger.info(f"Total registered MCP servers: {len(registry.mcp_servers)}")
    return registry
