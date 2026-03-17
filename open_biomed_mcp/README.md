# OpenBioMed MCP Service Documentation

## Project Overview

`open_biomed_mcp` is a biomedical tool service platform built on FastAPI and MCP (Model Context Protocol). It addresses the fragmentation of current biomedical tools by integrating, deduplicating, and standardizing tools from mainstream open-source projects such as OrigeneMCP and Biomni. The platform natively supports the MCP standard and simultaneously exposes RESTful interfaces powered by FastAPI, providing out-of-the-box multi-modal access for LLM invocation, intelligent agent development, and traditional research workflows.

Project version: `0.2.0`

---

## Service Overview

This project integrates **32 tool modules** in two categories:

### 1. Biological Database API Services (13 modules)

| Module | Path Prefix | Description |
|--------|-------------|-------------|
| **ChEMBL** | `/chembl` | Bioactivity database: compound activity, assays, drugs, targets |
| **NCBI** | `/ncbi` | National Center for Biotechnology Information: genes, genomes, taxonomy, viruses |
| **PubChem** | `/pubchem` | Compound database: search by name/SMILES/CID/formula, properties |
| **UniProt** | `/uniprot` | Protein knowledgebase: UniProtKB, UniRef, UniParc, proteomes |
| **KEGG** | `/kegg` | Pathway and genome database: pathways, genes, compounds |
| **STRING** | `/string` | Protein interaction network database: PPI, functional enrichment |
| **TCGA** | `/tcga` | The Cancer Genome Atlas: gene expression across cancer types |
| **Ensembl** | `/ensembl` | Genome annotation: gene lookup, VEP, homology, sequence retrieval |
| **UCSC** | `/ucsc` | UCSC Genome Browser API: sequences, tracks, chromosome info |
| **ClinicalTrials** | `/clinicaltrials` | ClinicalTrials.gov: trial search and detail queries |
| **PDB** | `/pdb` | Protein Data Bank: structure, entity, assembly, chemical component queries |
| **DBSearch** | `/dbsearch` | Multi-database search: ClinVar, Ensembl, GSEA, GTRD, miRDB, MouseMine, PHIPSTER |
| **Search** | `/search_tools` | Search engine tools: Tavily search and Jina DeepSearch |

### 2. Biomedical Computing Toolset (19 modules)

| Module | Path Prefix | Description |
|--------|-------------|-------------|
| **Literature** | `/literature` | Supplementary info retrieval, literature search |
| **Biochemistry** | `/biochemistry` | CD spectra analysis, protein structure analysis |
| **Bioimaging** | `/bioimaging` | Image segmentation, microscopy image analysis |
| **Bioengineering** | `/bioengineering` | Cell migration analysis, tissue engineering tools |
| **Biophysics** | `/biophysics` | Protein disorder region prediction (IUPred2A) |
| **Glycoengineering** | `/glycoengineering` | N-glycosylation site finding |
| **Cancer Biology** | `/cancer_biology` | DNA damage response network analysis |
| **Cell Biology** | `/cell_biology` | Cell cycle analysis, cell counting |
| **Molecular Biology** | `/molecular_biology` | ORF annotation, plasmid annotation, PCR simulation, restriction digestion, primer alignment |
| **Genetics** | `/genetics` | Genome coordinate liftover (hg19/hg38) |
| **Immunology** | `/immunology` | ATAC-seq peak calling, differential accessibility analysis |
| **Microbiology** | `/microbiology` | Anaerobic digestion process optimization |
| **Pathology** | `/pathology` | Cardiovascular imaging analysis, aortic geometry |
| **Pharmacology** | `/pharmacology` | Molecular docking (DiffDock) |
| **Physiology** | `/physiology` | MRI facial anatomy 3D reconstruction |
| **Synthetic Biology** | `/synthetic_biology` | Bacterial genome engineering, therapeutic delivery design |
| **Systems Biology** | `/systems_biology` | Flux balance analysis (FBA) |
| **Support Tools** | `/support_tools` | Python REPL execution, source code reading, Synapse data download |
| **Lab Automation** | `/lab_automation` | PyLabRobot script testing |

---

## Core Features per Module

### ChEMBL (Bioactivity Data) — 101 tools
- Activity data query and search (`get_activity`, `search_activity`)
- Assay information query (`get_assay_by_id`, `search_assay`)
- ATC classification query (`get_atc_class`)
- Binding site query (`get_binding_site`)
- Drug information query (`get_drug`, `get_drug_indication`, `get_drug_warning`)
- Compound records and structural alerts (`get_compound_record`, `get_compound_structural_alert`)
- Document query and similarity analysis (`get_document`, `get_document_similarity`)
- ChEMBL ID lookup (`get_chembl_id_lookup`)

### NCBI (Genes and Genomes) — 56 tools
- Gene metadata query (`get_gene_metadata_by_gene_name`)
- Gene ID / accession / symbol / taxon queries
- Genome annotation reports, sequence reports, revision history
- Virus annotation and genome data
- Taxonomy information query and suggestions
- Biosample reports, organelle data
- Gene ortholog queries

### PubChem (Compound Information) — 39 tools
- Search compounds by name/SMILES/CID/formula
- Compound details (properties, synonyms, descriptions, 3D structures)
- Substance information query (SID)
- Bioassay summaries
- Gene/protein/taxonomy summaries
- Conformer queries
- Substructure CAS number queries

### UniProt (Protein Knowledgebase) — 22 tools
- UniProtKB entry query and search
- UniRef cluster query and member retrieval
- UniParc entries and cross-references
- GeneCentric gene-centric queries
- Proteome queries

### KEGG (Pathways and Genomes) — 6 tools
- Database information query (`kegg_info`)
- Data search (`kegg_find`)
- Entry listing (`kegg_list`)
- Entry detail retrieval (`kegg_get`)
- ID conversion (`kegg_conv`)
- Cross-reference links (`kegg_link`)

### STRING (Protein Networks) — 8 tools
- Identifier mapping (`mapping_identifiers`)
- Network interaction query (`get_string_network_interaction`)
- All interaction partners query
- Protein similarity scoring
- Best cross-species similarity matching
- Functional enrichment analysis
- Functional annotation
- PPI enrichment analysis

### Ensembl (Genome Annotation) — 104 tools
- Gene symbol lookup (`get_lookup_symbol`)
- Homology analysis (`get_homology_symbol`, `get_homology_id`)
- Genome sequence retrieval (`get_sequence_region`)
- Variant Effect Predictor VEP (`get_vep_hgvs`, `get_vep_id`, `get_vep_region`)
- Gene trees and CAFE analysis
- Assembly and region information
- Cross-reference queries
- Coordinate mapping (cDNA/CDS/protein → genome)
- Ontology queries
- Phenotype association queries
- Variant information and recoding

### UCSC (Genome Browser) — 9 tools
- Genome list and chromosome list
- Track data queries
- DNA sequence retrieval
- Cytobands information
- Public track hubs

### ClinicalTrials — 8 tools
- Clinical trial search (complex queries, filtering, pagination)
- Single trial detail query
- Metadata, search areas, enumeration value queries
- Field statistics

### PDB (Protein Structure) — 20 tools
- Structure information query
- PubMed/UniProt/DrugBank annotations
- Polymer/branched/non-polymer entity and instance queries
- Structure assembly information
- Polymer interface analysis
- Chemical component queries
- Residue chain information
- Entity group queries

### TCGA (The Cancer Genome Atlas) — 1 tool
- Gene expression pattern analysis across cancer types (`get_gene_specific_expression_in_cancer_type`): Based on the Firebrowse API (TCGA mRNASeq), computes mean expression and z-scores for a given gene across cancer cohorts, returning high-expression (z > 1) and low-expression (z < -1) cancer types

### Search (Search Engine Tools) — 2 tools
- Tavily search (`tavily_search`): Retrieves and filters web results using the Tavily search engine
- Jina DeepSearch (`jina_search`): Performs deep retrieval using the Jina DeepSearch engine

### DBSearch (Multi-Database Search) — 14 tools
- ClinVar variant significance queries
- Protein sequence BLAST matching
- Genomic region gene queries
- Cytogenetic band region gene extraction
- GSEA gene set retrieval
- GTRD transcription factor target gene queries
- miRDB miRNA target gene prediction
- MouseMine phenotype gene queries
- PHIPSTER virus-human protein interaction queries

### Literature — 8 tools
- Fetch supplementary info from DOI (`fetch_supplementary_info_from_doi`)
- arXiv paper search (`query_arxiv`)
- Google Scholar academic search (`query_scholar`)
- PubMed literature search (`query_pubmed`)
- Google search (`search_google`)
- URL content extraction (`extract_url_content`)
- PDF content extraction (`extract_pdf_content`)
- Claude-based advanced web search (`advanced_web_search_claude`)

### Biochemistry — 6 tools
- Circular dichroism (CD) spectra analysis (`analyze_circular_dichroism_spectra`)
- RNA secondary structure feature analysis (`analyze_rna_secondary_structure_features`)
- Protease kinetics analysis (`analyze_protease_kinetics`)
- Enzyme kinetics assay analysis (`analyze_enzyme_kinetics_assay`)
- ITC binding thermodynamics analysis (`analyze_itc_binding_thermodynamics`)
- Protein conservation analysis (`analyze_protein_conservation`)

### Bioimaging — 9 tools
- Multi-modality image splitting (`split_modalities`)
- nnU-Net input preparation (`prepare_input_for_nnunet`)
- nnU-Net image segmentation (`segment_with_nn_unet`)
- Segmentation result visualization (`create_segmentation_visualization`)
- Quick rigid registration (`quick_rigid_registration`)
- Quick affine registration (`quick_affine_registration`)
- Quick deformable registration (`quick_deformable_registration`)
- Batch image registration (`batch_register_images`)
- Similarity metric calculation (`calculate_similarity_metrics`)
- Registration result visualization (`create_registration_visualization`)

### Bioengineering — 7 tools
- Cell migration metrics analysis (`analyze_cell_migration_metrics`)
- CRISPR-Cas9 genome editing simulation (`perform_crispr_cas9_genome_editing`)
- Calcium imaging data analysis (`analyze_calcium_imaging_data`)
- In vitro drug release kinetics analysis (`analyze_in_vitro_drug_release_kinetics`)
- Myofiber morphology analysis (`analyze_myofiber_morphology`)
- Behavior decoding from neural trajectories (`decode_behavior_from_neural_trajectories`)
- Whole-cell ODE model simulation (`simulate_whole_cell_ode_model`)

### Biophysics — 3 tools
- Protein disorder region prediction (`predict_protein_disorder_regions`)
- Cell morphology and cytoskeleton analysis (`analyze_cell_morphology_and_cytoskeleton`)
- Tissue deformation flow analysis (`analyze_tissue_deformation_flow`)

### Glycoengineering — 3 tools
- N-glycosylation motif finding (`find_n_glycosylation_motifs`)
- O-glycosylation hotspot prediction (`predict_o_glycosylation_hotspots`)
- Glycoengineering resource listing (`list_glycoengineering_resources`)

### Cancer Biology — 6 tools
- DDR network analysis in cancer (`analyze_ddr_network_in_cancer`)
- Cell senescence and apoptosis analysis (`analyze_cell_senescence_and_apoptosis`)
- Somatic mutation detection and annotation (`detect_and_annotate_somatic_mutations`)
- Structural variation detection and characterization (`detect_and_characterize_structural_variations`)
- Gene expression NMF analysis (`perform_gene_expression_nmf_analysis`)
- Copy number, purity, ploidy, and focal event analysis (`analyze_copy_number_purity_ploidy_and_focal_events`)

### Cell Biology — 5 tools
- Cell cycle phase quantification from microscopy (`quantify_cell_cycle_phases_from_microscopy`)
- Cell motility quantification and clustering (`quantify_and_cluster_cell_motility`)
- Fluorescence-activated cell sorting FACS (`perform_facs_cell_sorting`)
- Flow cytometry immunophenotyping analysis (`analyze_flow_cytometry_immunophenotyping`)
- Mitochondrial morphology and membrane potential analysis (`analyze_mitochondrial_morphology_and_potential`)

### Molecular Biology — 18 tools
- Open reading frame (ORF) annotation (`annotate_open_reading_frames`)
- Plasmid annotation (`annotate_plasmid`)
- Gene coding sequence retrieval (`get_gene_coding_sequence`)
- Plasmid sequence retrieval (Addgene/NCBI) (`get_plasmid_sequence`)
- Primer alignment (`align_sequences`)
- PCR amplification simulation (`pcr_simple`)
- Restriction digestion simulation (`digest_sequence`)
- Restriction site finding (`find_restriction_sites`, `find_restriction_enzymes`)
- Sequence mutation finding (`find_sequence_mutations`)
- CRISPR sgRNA design (`design_knockout_sgrna`)
- Oligonucleotide annealing protocol (`get_oligo_annealing_protocol`)
- Golden Gate assembly protocol and simulation (`get_golden_gate_assembly_protocol`, `golden_gate_assembly`)
- Golden Gate oligo design (`design_golden_gate_oligos`)
- Bacterial transformation protocol (`get_bacterial_transformation_protocol`)
- Primer design (`design_primer`)
- Sanger sequencing verification primer design (`design_verification_primers`)

### Genetics — 9 tools
- Genome coordinate liftover hg19/hg38 (`liftover_coordinates`)
- Bayesian fine-mapping with deep variational inference (`bayesian_finemapping_with_deep_vi`)
- Cas9 mutation outcome analysis (`analyze_cas9_mutation_outcomes`)
- CRISPR genome editing outcome analysis (`analyze_crispr_genome_editing`)
- Demographic history simulation (msprime) (`simulate_demographic_history`)
- Transcription factor binding site identification (`identify_transcription_factor_binding_sites`)
- Genomic prediction linear mixed model (`fit_genomic_prediction_model`)
- PCR amplification and gel electrophoresis simulation (`perform_pcr_and_gel_electrophoresis`)
- Protein phylogeny analysis (`analyze_protein_phylogeny`)

### Immunology — 10 tools
- ATAC-seq differential accessibility analysis (`analyze_atac_seq_differential_accessibility`)
- Bacterial growth curve analysis (`analyze_bacterial_growth_curve`)
- Immune cell isolation and purification simulation (`isolate_purify_immune_cells`)
- Cell cycle phase duration estimation (`estimate_cell_cycle_phase_durations`)
- Immune cell tracking under flow conditions (`track_immune_cells_under_flow`)
- CFSE cell proliferation analysis (`analyze_cfse_cell_proliferation`)
- CD4+ T cell cytokine production analysis (`analyze_cytokine_production_in_cd4_tcells`)
- EBV antibody titer ELISA analysis (`analyze_ebv_antibody_titers`)
- CNS lesion histology analysis (`analyze_cns_lesion_histology`)
- Immunohistochemistry image analysis (`analyze_immunohistochemistry_image`)

### Microbiology — 12 tools
- Anaerobic digestion process optimization (`optimize_anaerobic_digestion_process`)
- Arsenic speciation HPLC-ICP-MS analysis (`analyze_arsenic_speciation_hplc_icpms`)
- Bacterial colony counting (computer vision) (`count_bacterial_colonies`)
- Bacterial genome annotation (Prokka) (`annotate_bacterial_genome`)
- Serial dilution CFU enumeration (`enumerate_bacterial_cfu_by_serial_dilution`)
- Bacterial population dynamics modeling (ODE) (`model_bacterial_growth_dynamics`)
- Biofilm biomass quantification (crystal violet) (`quantify_biofilm_biomass_crystal_violet`)
- Microbial cell segmentation and morphology analysis (`segment_and_analyze_microbial_cells`)
- Deep learning cell segmentation (Cellpose/Omnipose) (`segment_cells_with_deep_learning`)
- Microbial community dynamics simulation (gLV model) (`simulate_generalized_lotka_volterra_dynamics`)
- RNA secondary structure prediction (ViennaRNA) (`predict_rna_secondary_structure`)
- Microbial population stochastic simulation (Gillespie algorithm) (`simulate_microbial_population_dynamics`)

### Pathology — 7 tools
- Aortic diameter and geometry analysis (`analyze_aortic_diameter_and_geometry`)
- ATP luminescence assay analysis (`analyze_atp_luminescence_assay`)
- Thrombus histology image analysis (`analyze_thrombus_histology`)
- Intracellular calcium analysis (Rhod-2) (`analyze_intracellular_calcium_with_rhod2`)
- Corneal nerve fiber quantification (`quantify_corneal_nerve_fibers`)
- Cell segmentation and protein quantification in multiplexed tissue images (`segment_and_quantify_cells_in_multiplexed_images`)
- Bone microstructure micro-CT morphometry (`analyze_bone_microct_morphometry`)

### Pharmacology — 25 tools
- DiffDock molecular docking (`run_diffdock_with_smiles`)
- AutoDock Vina molecular docking (`docking_autodock_vina`)
- AutoSite binding site identification (`run_autosite`)
- TxGNN drug repurposing prediction (`retrieve_topk_repurposing_drugs_from_disease_txgnn`)
- ADMET property prediction (`predict_admet_properties`)
- Protein-small molecule binding affinity prediction (`predict_binding_affinity_protein_1d_sequence`)
- Accelerated stability analysis of pharmaceutical formulations (`analyze_accelerated_stability_of_pharmaceutical_formulations`)
- 3D chondrogenic aggregate culture assay (`run_3d_chondrogenic_aggregate_assay`)
- VCOG-CTCAE adverse event grading (`grade_adverse_events_using_vcog_ctcae`)
- Radiolabeled antibody biodistribution analysis (`analyze_radiolabeled_antibody_biodistribution`)
- Alpha particle radiotherapy dosimetry estimation (`estimate_alpha_particle_radiotherapy_dosimetry`)
- Methylome-wide association study MWAS (`perform_mwas_cyp2c19_metabolizer_status`)
- Physicochemical property calculation (`calculate_physicochemical_properties`)
- Xenograft tumor growth inhibition analysis (`analyze_xenograft_tumor_growth_inhibition`)
- Western blot pixel distribution analysis (`analyze_pixel_distribution`)
- Western blot ROI detection (`find_roi_from_image`)
- Western blot densitometry analysis (`analyze_western_blot`)
- Drug-drug interaction query (DDInter) (`query_drug_interactions`)
- Drug combination safety check (`check_drug_combination_safety`)
- Drug interaction mechanism analysis (`analyze_interaction_mechanisms`)
- Alternative drug finding (`find_alternative_drugs_ddinter`)
- FDA adverse event query (`query_fda_adverse_events`)
- FDA drug label information retrieval (`get_fda_drug_label_info`)
- FDA drug recall check (`check_fda_drug_recalls`)
- FDA safety signal analysis (`analyze_fda_safety_signals`)

### Physiology — 11 tools
- 3D facial anatomy reconstruction from MRI (`reconstruct_3d_face_from_mri`)
- Auditory brainstem response (ABR) waveform analysis (`analyze_abr_waveform_p1_metrics`)
- Ciliary beat frequency analysis (FFT) (`analyze_ciliary_beat_frequency`)
- Protein colocalization analysis (`analyze_protein_colocalization`)
- Circadian rhythm cosinor analysis (`perform_cosinor_analysis`)
- Brain ADC map calculation (diffusion-weighted MRI) (`calculate_brain_adc_map`)
- Endolysosomal calcium dynamics analysis (`analyze_endolysosomal_calcium_dynamics`)
- Fatty acid composition analysis by GC (`analyze_fatty_acid_composition_by_gc`)
- Hemodynamic parameter analysis (`analyze_hemodynamic_data`)
- Thyroid hormone pharmacokinetics simulation (`simulate_thyroid_hormone_pharmacokinetics`)
- Amyloid beta plaque quantification (`quantify_amyloid_beta_plaques`)

### Synthetic Biology — 8 tools
- Bacterial genome engineering for therapeutic delivery (`engineer_bacterial_genome_for_therapeutic_delivery`)
- Bacterial growth rate analysis (`analyze_bacterial_growth_rate`)
- Barcode sequencing data analysis (`analyze_barcode_sequencing_data`)
- Bifurcation diagram analysis (`analyze_bifurcation_diagram`)
- SBML biochemical network model generation (`create_biochemical_network_sbml_model`)
- Codon optimization for heterologous expression (`optimize_codons_for_heterologous_expression`)
- Gene circuit dynamics simulation with growth feedback (`simulate_gene_circuit_with_growth_feedback`)
- Fatty acid synthase functional domain identification (`identify_fas_functional_domains`)

### Systems Biology — 7 tools
- Flux balance analysis FBA (`perform_flux_balance_analysis`)
- Protein dimerization network modeling (`model_protein_dimerization_network`)
- Metabolic network perturbation simulation (`simulate_metabolic_network_perturbation`)
- Protein signaling network dynamics simulation (`simulate_protein_signaling_network`)
- Protein structure comparison (`compare_protein_structures`)
- Renin-angiotensin system dynamics simulation (`simulate_renin_angiotensin_system_dynamics`)
- DNA sequence functional Q&A (ChatNT) (`query_chatnt`)

### Support Tools — 3 tools
- Python REPL execution (`run_python_repl`)
- Function source code reading (`read_function_source_code`)
- Synapse data download (`download_synapse_data`)

### Lab Automation — 3 tools
- PyLabRobot script testing (`test_pylabrobot_script`)
- PyLabRobot liquid handling documentation (`get_pylabrobot_documentation_liquid`)
- PyLabRobot material handling documentation (`get_pylabrobot_documentation_material`)

---

## Getting Started

### 1. Environment Setup

```bash
# Navigate to the project directory
cd /OpenBioMed/open_biomed_mcp

# Create and activate a conda environment (Python 3.11+ recommended)
conda create -n biomed_mcp python=3.11
conda activate biomed_mcp

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Edit the `.env` file and set the required API keys:

```env
tavily_api_key = "your_tavily_api_key"
jina_api_key = "your_jina_api_key"
```

### 3. Start the Service

```bash
# Start with uvicorn (development mode)
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Or start with fastapi CLI
fastapi dev main.py --host 0.0.0.0 --port 8000
```

Once running, you can access:
- API docs: `http://localhost:8000/docs` (Swagger UI)
- Health check: `http://localhost:8000/healthz`
- Tools summary: `http://localhost:8000/tools/summary`

---

## How to Use the MCP Service

This project supports **three access methods**:

### Method 1: REST API

All tools are registered as FastAPI endpoints and can be called via HTTP POST requests.

```bash
# Example: query gene metadata by gene name
curl -X POST "http://localhost:8000/tools/ncbi/get_gene_metadata_by_gene_name" \
  -H "Content-Type: application/json" \
  -d '{"name": "BRCA1", "species": "human"}'

# Example: search for a compound
curl -X POST "http://localhost:8000/tools/pubchem/search_pubchem_by_name" \
  -H "Content-Type: application/json" \
  -d '{"name": "aspirin"}'

# Example: query protein interaction network
curl -X POST "http://localhost:8000/tools/string/get_string_network_interaction" \
  -H "Content-Type: application/json" \
  -d '{"identifiers": ["TP53", "BRCA1"], "species": 9606, "required_score": 700, "add_nodes": 5, "network_type": "physical", "show_query_node_labels": 1}'
```

Full API documentation is available at `http://localhost:8000/docs`.

### Method 2: MCP SSE Protocol

The project also exposes MCP SSE endpoints, supporting direct connection from MCP clients (e.g., Kiro, Claude Desktop).

**Global MCP endpoint** (all tools):
```
http://localhost:8000/mcp
```

**Per-module MCP endpoints** (each module independent):
```
http://localhost:8000/chembl/mcp
http://localhost:8000/ncbi/mcp
http://localhost:8000/pubchem/mcp
http://localhost:8000/uniprot/mcp
http://localhost:8000/kegg/mcp
http://localhost:8000/string/mcp
http://localhost:8000/search_tools/mcp
http://localhost:8000/tcga/mcp
http://localhost:8000/ensembl/mcp
http://localhost:8000/ucsc/mcp
http://localhost:8000/clinicaltrials/mcp
http://localhost:8000/pdb/mcp
http://localhost:8000/dbsearch/mcp
http://localhost:8000/literature/mcp
http://localhost:8000/biochemistry/mcp
http://localhost:8000/bioimaging/mcp
http://localhost:8000/bioengineering/mcp
http://localhost:8000/biophysics/mcp
http://localhost:8000/glycoengineering/mcp
http://localhost:8000/cancer_biology/mcp
http://localhost:8000/cell_biology/mcp
http://localhost:8000/molecular_biology/mcp
http://localhost:8000/genetics/mcp
http://localhost:8000/immunology/mcp
http://localhost:8000/microbiology/mcp
http://localhost:8000/pathology/mcp
http://localhost:8000/pharmacology/mcp
http://localhost:8000/physiology/mcp
http://localhost:8000/synthetic_biology/mcp
http://localhost:8000/systems_biology/mcp
http://localhost:8000/support_tools/mcp
http://localhost:8000/lab_automation/mcp
```

### Method 3: Configure MCP in AI IDE / Agent

Configure the MCP server in any MCP-compatible AI tool (e.g., Kiro, Claude Desktop, Cursor).

**Kiro configuration example** (`.kiro/settings/mcp.json`):

```json
{
  "mcpServers": {
    "biomed-all": {
      "url": "http://localhost:8000/mcp",
      "disabled": false
    }
  }
}
```

To use only specific modules, configure them individually, for example:

```json
{
  "mcpServers": {
    "biomed-ncbi": {
      "url": "http://localhost:8000/ncbi/mcp",
      "disabled": false
    },
    "biomed-pubchem": {
      "url": "http://localhost:8000/pubchem/mcp",
      "disabled": false
    }
  }
}
```

**Claude Desktop configuration example** (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "biomed": {
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

---

## Project Structure

```
open_biomed_mcp/
├── main.py                    # FastAPI application entry point
├── registry.py                # MCP tool registry
├── mcp_to_fastapi.py          # MCP → FastAPI adapter
├── .env                       # Environment variable configuration
├── requirements.txt           # Python dependencies
└── tools/                     # Tool module directory
    ├── biodb/                 # External database API services
    │   ├── chembl/            # ChEMBL database
    │   ├── ncbi/              # NCBI database
    │   ├── pubchem/           # PubChem database
    │   ├── uniprot/           # UniProt database
    │   ├── kegg/              # KEGG database
    │   ├── STRING/            # STRING database
    │   ├── search/            # Search engines (Tavily/Jina)
    │   ├── tcga/              # TCGA cancer genome
    │   ├── ensembl/           # Ensembl genome annotation
    │   ├── ucsc/              # UCSC genome browser
    │   ├── clinicaltrials/    # ClinicalTrials.gov
    │   ├── pdb/               # PDB protein structure
    │   └── dbsearch/          # Multi-database search
    └── biocomputing/          # Biocomputing biomedical computing toolset
        ├── mcp_to_fastapi.py  # Biocomputing MCP adapter
        ├── tool_registry.py   # Tool registry
        ├── tool_description/  # Tool description definitions
        ├── literature.py      # Literature retrieval
        ├── biochemistry.py    # Biochemistry
        ├── bioimaging.py      # Bioimaging
        ├── bioengineering.py  # Bioengineering
        ├── biophysics.py      # Biophysics
        ├── glycoengineering.py # Glycoengineering
        ├── cancer_biology.py  # Cancer biology
        ├── cell_biology.py    # Cell biology
        ├── molecular_biology.py # Molecular biology
        ├── genetics.py        # Genetics
        ├── immunology.py      # Immunology
        ├── microbiology.py    # Microbiology
        ├── pathology.py       # Pathology
        ├── pharmacology.py    # Pharmacology
        ├── physiology.py      # Physiology
        ├── synthetic_biology.py # Synthetic biology
        ├── systems_biology.py # Systems biology
        ├── support_tools.py   # Support tools
        └── lab_automation.py  # Lab automation
```

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                      Client                          │
│  (AI Agent / Browser / curl / MCP Client)            │
└──────────┬──────────────────┬───────────────────────┘
           │ REST API         │ MCP SSE
           ▼                  ▼
┌──────────────────────────────────────────────────────┐
│                  FastAPI Application                  │
│                                                      │
│  /tools/*          → REST API endpoints              │
│  /mcp              → Global MCP SSE endpoint         │
│  /{module}/mcp     → Module-level MCP SSE endpoint   │
│  /docs             → Swagger API documentation       │
│  /healthz          → Health check                    │
│  /tools/summary    → Tools summary                   │
└──────────┬───────────────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────────────┐
│              MCPToolsRegistry                         │
│                                                      │
│  ┌─────────┐ ┌──────┐ ┌─────────┐ ┌──────────────┐  │
│  │ ChEMBL  │ │ NCBI │ │ PubChem │ │ ... more     │  │
│  │ FastMCP │ │FastMCP│ │ FastMCP │ │   FastMCP    │  │
│  └─────────┘ └──────┘ └─────────┘ └──────────────┘  │
│                                                      │
│  ┌──────────────────────────────────────────────┐    │
│  │    Biocomputing Toolset (19 sub-modules)      │    │
│  │    Each sub-module has its own FastMCP server │    │
│  └──────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────┘
```

Each tool module is an independent `FastMCP` server instance, uniformly registered to the FastAPI application via `MCPToolsRegistry`, generating both REST API endpoints and MCP SSE endpoints simultaneously.
