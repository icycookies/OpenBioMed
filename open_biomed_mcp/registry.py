"""
MCP Tools Registry
Unified management of registration and FastAPI conversion for all MCP tool services
"""

import logging
from typing import List, Dict, Any
from fastapi import APIRouter, FastAPI
from mcp.server.fastmcp import FastMCP

from mcp_to_fastapi import create_mcp_fastapi_router

logger = logging.getLogger(__name__)

BIOCOMPUTING_MODULE_NAME_MAP = {
    "literature": "Literature Retrieval",
    "biochemistry": "Biochemistry",
    "bioimaging": "Bioimaging",
    "bioengineering": "Bioengineering",
    "biophysics": "Biophysics",
    "glycoengineering": "Glycoengineering",
    "cancer_biology": "Cancer Biology",
    "cell_biology": "Cell Biology",
    "molecular_biology": "Molecular Biology",
    "genetics": "Genetics",
    "genomics": "Genomics",
    "immunology": "Immunology",
    "microbiology": "Microbiology",
    "pathology": "Pathology",
    "pharmacology": "Pharmacology",
    "physiology": "Physiology",
    "synthetic_biology": "Synthetic Biology",
    "systems_biology": "Systems Biology",
    "support_tools": "Support Tools",
    "lab_automation": "Lab Automation",
}


class MCPToolsRegistry:
    """MCP Tools Registry"""
    
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
        Register an MCP server
        
        Args:
            mcp_server: FastMCP server instance
            prefix: API path prefix, e.g. "/chembl"
            tags: FastAPI tag list
            description: Service description
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
        Create FastAPI routers for all registered MCP servers
        
        Returns:
            List of APIRouters
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
        Register all MCP tools to a FastAPI application
        
        Args:
            app: FastAPI application instance
            base_prefix: Base path prefix, default "/tools"
        """
        routers = self.create_fastapi_routers()
        for router in routers:
            app.include_router(router, prefix=base_prefix)
            # logger.info(f"Included router with prefix: {base_prefix}")
    
    def get_tools_summary(self) -> Dict[str, Any]:
        """
        Get summary information of all tools
        
        Returns:
            Tools summary dictionary
        """
        summary = {
            "total_servers": len(self.mcp_servers),
            "servers": []
        }
        
        for config in self.tool_configs:
            mcp_server = config["mcp_server"]
            
            # Distinguish between FastMCP and FastApiMCP types
            tools = {}
            if hasattr(mcp_server, '_tool_manager') and hasattr(mcp_server._tool_manager, '_tools'):
                # FastMCP type
                tools = mcp_server._tool_manager._tools
            elif hasattr(mcp_server, '_tools'):
                # FastApiMCP type
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


# Create global registry instance
registry = MCPToolsRegistry()


def setup_mcp_tools():
    """
    Set up all MCP tool services.
    This function imports all tool MCP servers and registers them to the registry.
    """
    # ChEMBL
    try:
        from tools.biodb.chembl.server import mcp as chembl_mcp
        registry.register_mcp_server(
            chembl_mcp,
            prefix="/chembl",
            tags=["Bioactivity"],
            description="ChEMBL Database API - Bioactivity Data"
        )
    except Exception as e:
        logger.warning(f"Failed to register chembl: {e}")
    
    # NCBI
    try:
        from tools.biodb.ncbi.server import mcp as ncbi_mcp
        registry.register_mcp_server(
            ncbi_mcp,
            prefix="/ncbi",
            tags=["Genetics"],
            description="NCBI Database API - Gene and Genome Data"
        )
    except Exception as e:
        logger.warning(f"Failed to register ncbi: {e}")
    
    # PubChem
    try:
        from tools.biodb.pubchem.server import mcp as pubchem_mcp
        registry.register_mcp_server(
            pubchem_mcp,
            prefix="/pubchem",
            tags=["Compound Information"],
            description="PubChem Database API - Compound Information"
        )
    except Exception as e:
        logger.warning(f"Failed to register pubchem: {e}")
    
    # UniProt
    try:
        from tools.biodb.uniprot.server import mcp as uniprot_mcp
        registry.register_mcp_server(
            uniprot_mcp,
            prefix="/uniprot",
            tags=["Protein Information"],
            description="UniProt Database API - Protein Information"
        )
    except Exception as e:
        logger.warning(f"Failed to register uniprot: {e}")
    
    # KEGG
    try:
        from tools.biodb.kegg.server import mcp as kegg_mcp
        registry.register_mcp_server(
            kegg_mcp,
            prefix="/kegg",
            tags=["Pathways and Genomics"],
            description="KEGG Database API - Pathway and Genome Information"
        )
    except Exception as e:
        logger.warning(f"Failed to register kegg: {e}")
    
    # STRING
    try:
        from tools.biodb.STRING.server import mcp as string_mcp
        registry.register_mcp_server(
            string_mcp,
            prefix="/string",
            tags=["Protein Networks"],
            description="STRING Database API - Protein Interaction Networks"
        )
    except Exception as e:
        logger.warning(f"Failed to register string: {e}")
    
    # Search
    try:
        from tools.biodb.search.server import mcp as search_mcp
        registry.register_mcp_server(
            search_mcp,
            prefix="/search_tools",
            tags=["Search Tools"],
            description="Search Tools - Tavily and Jina Search"
        )
    except Exception as e:
        logger.warning(f"Failed to register search: {e}")
    
    # TCGA
    try:
        from tools.biodb.tcga.server import mcp as tcga_mcp
        registry.register_mcp_server(
            tcga_mcp,
            prefix="/tcga",
            tags=["Cancer Genomics"],
            description="TCGA Database API - Cancer Genome Data"
        )
    except Exception as e:
        logger.warning(f"Failed to register tcga: {e}")
    
    # Ensembl
    try:
        from tools.biodb.ensembl.server import mcp as ensembl_mcp
        registry.register_mcp_server(
            ensembl_mcp,
            prefix="/ensembl",
            tags=["Genome Annotation"],
            description="Ensembl Database API - Genome Annotation"
        )
    except Exception as e:
        logger.warning(f"Failed to register ensembl: {e}")
    
    # UCSC
    try:
        from tools.biodb.ucsc.server import mcp as ucsc_mcp
        registry.register_mcp_server(
            ucsc_mcp,
            prefix="/ucsc",
            tags=["Genome Browser API"],
            description="UCSC Genome Browser API"
        )
    except Exception as e:
        logger.warning(f"Failed to register ucsc: {e}")
    
    # ClinicalTrials
    try:
        from tools.biodb.clinicaltrials.server import mcp as clinicaltrials_mcp
        registry.register_mcp_server(
            clinicaltrials_mcp,
            prefix="/clinicaltrials",
            tags=["Clinical Trials"],
            description="ClinicalTrials.gov API - Clinical Trial Data"
        )
    except Exception as e:
        logger.warning(f"Failed to register clinicaltrials: {e}")
    
    # PDB
    try:
        from tools.biodb.pdb.server import mcp as pdb_mcp
        registry.register_mcp_server(
            pdb_mcp,
            prefix="/pdb",
            tags=["Protein Structure"],
            description="PDB Database API - Protein Structure Data"
        )
    except Exception as e:
        logger.warning(f"Failed to register pdb: {e}")
    
    # DBSearch
    try:
        from tools.biodb.dbsearch.server import mcp as dbsearch_mcp
        registry.register_mcp_server(
            dbsearch_mcp,
            prefix="/dbsearch",
            tags=["Database Search"],
            description="Database Search Tools"
        )
    except Exception as e:
        logger.warning(f"Failed to register dbsearch: {e}")
    
    # Biocomputing - Comprehensive biomedical toolset
    try:
        from tools.biocomputing.mcp_to_fastapi import BiocomputingMcp
        
        
        biocomputing = BiocomputingMcp()
        
        # Create an independent MCP server for each module
        biocomputing_servers = biocomputing.create_mcp_servers_per_module()
        
        # Register each module's server
        registered_count = 0
        for module_name, mcp_server in biocomputing_servers.items():
            try:
                # Format module name for display - use more explicit tag names
                display_name = BIOCOMPUTING_MODULE_NAME_MAP.get(module_name, module_name.replace('_', '-').title())
                
                # Get the number of tools in this server
                tool_count = len(mcp_server._tool_manager._tools)
                
                registry.register_mcp_server(
                    mcp_server,
                    prefix=f"/{module_name}",
                    tags=[display_name],    # category tag in fastapi
                    description=f"Biocomputing {module_name.replace('_', ' ').title()} Toolset"
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
