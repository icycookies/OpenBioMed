from open_biomed.tools.tool_misc import *
from open_biomed.tools.web_request_tools import *
from open_biomed.tools.visualization_tools import *
from open_biomed.tools.third_party_tools import *
from open_biomed.data.molecule import *
from open_biomed.scripts.inference import *
from open_biomed.tools.mcp_tools import get_mcp_tool_registry


# TODO: Add pocket prediction as a tool
class LazyDictForTool(dict):
    def __init__(self):
        super().__init__()
        self._mcp_tools_loaded = False
        self._mcp_tool_names = []


    def _ensure_mcp_tools_loaded(self):
        """Lazy-load the MCP tool list"""
        if not self._mcp_tools_loaded:
            try:
                mcp_registry = get_mcp_tool_registry()
                mcp_registry.load()
                self._mcp_tool_names = mcp_registry.available_tools()
                self._mcp_tools_loaded = True
                if self._mcp_tool_names:
                    print(f"✓ Loaded {len(self._mcp_tool_names)} MCP tools into registry")
            except Exception as e:
                print(f"Warning: Failed to load MCP tools: {e}")
                self._mcp_tool_names = []
                self._mcp_tools_loaded = True

    
    def available_tools(self):
        builtin_tools = [
            "text_based_molecule_editing", "molecule_property_prediction", "structure_based_drug_design", 
            "molecule_question_answering", "protein_question_answering", "mutation_explanation", 
            "mutation_engineering", "apply_mutation_to_sequence", "pocket_molecule_docking", 
            "protein_molecule_docking_score", "protein_folding", "protein_binding_site_prediction", 
            "visualize_molecule", "visualize_protein", "visualize_complex", 
            "visualize_protein_pocket", "molecule_name_request", "pubchemid_search", 
            "molecule_structure_request", "protein_uniprot_request", "protein_pdb_request", 
            "web_search", "import_pocket", "export_molecule", "export_protein", 
            "molecule_qed", "molecule_sa", "molecule_logp", "molecule_lipinski", "molecule_similarity", 
            "extract_molecules_from_pdb_file", "summarize_content"
        ]
        # Dynamically add MCP tools
        self._ensure_mcp_tools_loaded()
        return builtin_tools + self._mcp_tool_names
    
    def __missing__(self, key):
        # Check if it is an MCP tool first
        self._ensure_mcp_tools_loaded()
        if key in self._mcp_tool_names:
            mcp_registry = get_mcp_tool_registry()
            mcp_tools = mcp_registry.get_tools()
            self[key] = mcp_tools[key]
            return self[key]

        if key == "text_based_molecule_editing":
            self[key] = test_text_based_molecule_editing(unit_test=False)
        elif key == "molecule_property_prediction":
            self[key] = test_molecule_property_prediction(unit_test=False)
        elif key == "structure_based_drug_design":
            self[key] = test_structure_based_drug_design(unit_test=False)
        elif key == "molecule_question_answering":
            self[key] = test_molecule_question_answering(unit_test=False)
        elif key == "protein_question_answering":
            self[key] = test_protein_question_answering(unit_test=False)
        elif key == "mutation_explanation":
            self[key] = test_mutation_explanation(unit_test=False)
        elif key == "mutation_engineering":
            self[key] = test_mutation_engineering(unit_test=False)
        elif key == "apply_mutation_to_sequence":
            self[key] = MutationToSequence()
        elif key == "pocket_molecule_docking":
            self[key] = test_pocket_molecule_docking(unit_test=False)
        elif key == "protein_molecule_docking_score":
            self[key] = test_protein_molecule_docking(unit_test=False)
        elif key == "protein_folding":
            self[key] = test_protein_folding(unit_test=False)
        elif key == "protein_binding_site_prediction":
            self[key] = ProteinBindingSitePrediction()
        elif key == "visualize_molecule":
            self[key] = PyMolVisualizerWrapper(task="visualize_molecule")
        elif key == "visualize_protein":
            self[key] = PyMolVisualizerWrapper(task="visualize_protein")
        elif key == "visualize_complex":
            self[key] = PyMolVisualizerWrapper(task="visualize_complex")
        elif key == "visualize_protein_pocket":
            self[key] = PyMolVisualizerWrapper(task="visualize_protein_pocket")
        # TODO: update the name mapping between frontend and backend
        elif key == "molecule_name_request" or key == "pubchemid_search":
            self[key] = PubChemRequester()
        elif key == "molecule_structure_request":
            self[key] = PubChemStructureRequester()
        elif key == "pubchem_bioactivity":
            self[key] = PubChemBioactivityRequester()
        elif key == "protein_uniprot_request":
            self[key] = UniProtRequester()
        elif key == "protein_pdb_request":
            self[key] = PDBRequester()
        elif key == "extract_molecules_from_pdb_file":
            self[key] = ExtractAllMoleculesFromPDB()
        elif key == "web_search":
            self[key] = WebSearchRequester()
        # elif key == "key_info_extract":
        #    self[key] = KeyInfoExtractor()
        elif key == "import_pocket":
            self[key] = ImportPocket()
        elif key == "export_molecule":
            self[key] = ExportMolecule()
        elif key == "export_protein":
            self[key] = ExportProtein()
        elif key == "molecule_qed":
            self[key] = MoleculeQEDTool()  # TODO
        elif key == "molecule_sa":
            self[key] = MoleculeSATool()
        elif key == "molecule_logp":
            self[key] = MoleculeLogPTool()
        elif key == "molecule_lipinski":
            self[key] = MoleculeLipinskiTool()
        # elif key == "molecule_property_calculation":
        #    self[key] = MoleculePropertyCalculationTool()
        elif key == "molecule_similarity":
            self[key] = MoleculeSimilarityTool()
        elif key == "summarize_content":
            self[key] = LLMSummarize()
        else:
            raise NotImplementedError(f"{key} is currently not supported!")
        return self[key]

TOOLS = LazyDictForTool()