---
name: biodb-disease-drug-intelligence
description: A "Disease-to-Innovative-Drug Comprehensive Analysis" skill for biomedical Q&A scenarios. Used to answer questions such as "What innovative/cutting-edge/pipeline/novel-mechanism drugs exist for a given disease?" and outputs an integrated evidence report covering disease–target–pathway–drug–clinical progress–mechanism trends. Applicable to tasks requiring multi-database queries, deduplication/normalization, innovation filtering, and structured report generation using BioDB MCP (ChEMBL, ClinicalTrials, KEGG, UniProt, STRING, PubChem, Ensembl, PDB, Search).
---

# BioDB Disease Innovative Drug Intelligence Integration

## Overview

Converts natural language questions (e.g., "What noteworthy new drugs have emerged recently for Alzheimer's disease?") into executable multi-database query plans.
Generates decision-oriented comprehensive reports rather than simply returning a list of drug names.

## Quick Start

1. Identify whether the query belongs to the `disease_to_drug` scenario.
2. Normalize the disease entity and decompose the "innovative drug" intent.
3. Execute multi-database queries following a fixed subtask chain.
4. Perform entity normalization, evidence integration, innovation filtering, and tiered output.
5. Generate the report and annotate evidence boundaries.

For detailed data structures, routing tables, scoring rules, database role assignments, and the innovative drug intelligence template, see [disease_to_drug_playbook.md](references/disease_to_drug_playbook.md).

## Trigger and Detection

This skill is triggered when the user's question simultaneously contains:
- A disease entity: e.g., diabetes, lung cancer, Alzheimer's disease, obesity, NASH, RA.
- A drug innovation intent: e.g., innovative drug, novel-mechanism drug, pipeline drug, cutting-edge drug, noteworthy new drug.

If the question is too broad (e.g., "innovative drugs for cancer"), suggest narrowing the disease type first. If the user declines, default to a Top cancer types and Top mechanisms overview.

## Workflow (Fixed Skeleton)

### Step 0 — Question Structuring
Construct a task object (example):
```json
{
  "task_type": "disease_to_drug",
  "focus": "innovative_drugs",
  "disease_raw": "diabetes",
  "time_constraint": null,
  "region_constraint": null,
  "stage_constraint": null
}
```

### Step 1 — Disease Normalization
Output `canonical_disease`, `subtypes`, `aliases`, `preferred_query_terms`.
If the user has not specified a subtype, perform a general disease analysis first, then highlight more active R&D subtypes (e.g., prioritize T2DM under diabetes).

### Step 2 — Innovative Drug Definition Mapping
Map "innovative drug" to actionable criteria:
- New mechanism / new target (including first-in-class tendency)
- Representative recently approved drugs
- Mid-to-late stage pipeline candidates (Phase II/III preferred)
- Frontier directions (dual/multi-target, next-generation optimized molecules)

### Step 3 — Subtask Decomposition
Execute 6 fixed subtasks:
- `identify_targets_and_mechanisms`
- `enrich_pathway_and_target_evidence`
- `retrieve_representative_drugs`
- `build_drug_profiles`
- `validate_clinical_progress`
- `summarize_trends`

### Step 4 — Database Execution Order
Default order:
1. Disease normalization and alias enrichment: internal rules + `Search` (only when disease name is ambiguous or subtypes are missing)
2. Mechanism, pathway, and target skeleton: `KEGG` + `UniProt` + `STRING` + `Ensembl`
3. Target-to-drug mapping: `ChEMBL(target/mechanism)` + `ChEMBL(molecule/drug/indication)`
4. Clinical progress validation: `ClinicalTrials`
5. Structure, chemistry, and molecular supplement: `PubChem` + `PDB` (optional)
6. Web fallback: `Search` (only when databases are insufficient or latest regulatory/announcement verification is needed)

Notes:
- The current BioDB toolset does not include an OpenTargets service. This skill uses the `KEGG + UniProt + STRING + Ensembl + ChEMBL` combination as the primary "disease-to-mechanism/target/drug" pipeline substitute.
- `Ensembl`'s primary role is gene symbol normalization and transcript/family/homolog information supplementation; it does not replace `UniProt`'s protein function information.

### Step 5 — Evidence Integration and Deduplication
Primary keys (priority order):
- Drug: `ChEMBL ID > standard drug name > PubChem CID > ClinicalTrials intervention`
- Target: `UniProt accession / Ensembl gene / gene symbol > standard target name > alias`

Aliases, dosage forms, and gene/protein ID mappings must be retained to avoid incorrect merges (e.g., different formulations of semaglutide, different transcripts of the same gene, or protein aliases).

### Step 6 — Innovation Filtering and Ranking
Score 0–5 and rank comprehensively:
- `disease_relevance`
- `innovation`
- `clinical_maturity`
- `evidence_strength`
- `representativeness`

Output must be tiered:
- Approved / validated representative innovative drugs
- Mid-to-late stage pipeline candidates
- Frontier exploratory mechanism directions

### Step 7 — Report Generation
By default, first read `## 10. Report Template (Standard Version)` from `references/disease_to_drug_playbook.md` and strictly follow that template's section order and field skeleton for the final report.

Deviation from the standard template is only permitted when the user explicitly requests one of the following:
- Abbreviated / summary / conversational version
- Table / checklist version
- Specific section trimming
- Another explicitly specified format

If the user has not explicitly requested a format change, free-form report structures are not permitted. Even for shorter responses, the main section skeleton of the standard template must be maintained.

Output using an analytical writing style, including at minimum:
- Conclusion first
- Key targets / mechanisms
- Tiered list of representative drugs
- Clinical trial progress overview
- R&D trend assessment
- Result limitations and evidence boundaries

### Step 8 — Exception Fallback
- Too many results: select Top N by representativeness + innovation (default 10).
- Too few results: prioritize outputting target directions and adjacent mechanisms; do not force-fill a drug list.
- Conflicting evidence: explicitly state "molecular evidence exists / clinical evidence is limited."
- Missing constraints: default to `time_constraint=null, region_constraint=global` and explicitly declare this in the report.

## Tool Call Constraints

- Run the main pipeline first (`KEGG + UniProt + STRING + Ensembl -> ChEMBL -> ClinicalTrials`), then supplement with `PubChem/PDB/Search`. Do not reverse this order.
- `KEGG` handles disease–pathway skeleton; `UniProt` handles protein function and entry normalization; `STRING` handles network/interaction support; `Ensembl` handles gene naming, transcripts, and homolog supplementation; `ChEMBL` handles drug–target–mechanism mapping; `ClinicalTrials` handles clinical stage verification; `PubChem/PDB` handles chemistry and structure supplementation.
- When web supplementation, latest progress verification, regulatory announcement validation, or insufficient database results are needed, the `Search` capability within BioDB MCP must be used first.
- "Prioritize `Search`" means: multiple rounds of retrieval, query rewriting, splitting by disease subtype, separate searches by drug/trial/company/regulatory source, and cross-referencing multiple results are all permitted and encouraged.
- "`Search` insufficient" does not mean "first retrieval returned no hits." Only after reasonable multi-round `Search` retrieval still fails to yield sufficiently relevant, current, or credible primary sources should it be considered insufficient.
- External web search is only permitted as a last resort when the `Search` tool is unavailable, multi-round retrieval results remain clearly insufficient, or timeliness and source verification requirements still cannot be met.
- If external web search is ultimately used, the result notes or limitations section must explicitly state: which `Search` queries were performed, what information is still missing, and why external search was triggered. Bypassing BioDB MCP `Search` by default is not permitted.
- If key fields are missing (phase/status/target/pathway/gene_id/protein_id/structure), a supplementary query must be triggered.
- Every key conclusion in the report must have at least one traceable piece of evidence (database name + entity primary key or standard entry ID).
- Do not treat "innovative drug" as a regulatory definition; it is an information-integration definition and must be declared as such in the result notes.

## MCP Parameter Reference Table

The following field names must be passed exactly as specified in the MCP interface schema. Do not guess field names based on semantics. If the interface returns `422 Unprocessable Entity`, first correct the request body based on the `missing` field in the error and retry; do not switch to external search directly.

### KEGG

- `kegg_find`
  - Purpose: Keyword lookup for diseases, pathways, genes, etc.
  - Body example:
```json
{"db":"disease","query":"lung cancer"}
```
  - Common errors:
    - Writing `db` as `database`

### UniProt

- `get_general_info_by_protein_or_gene_name`
  - Purpose: Query basic functional information by protein or gene name
  - Body example:
```json
{"query":"EGFR"}
```
  - Common errors:
    - Writing `query` as `protein_or_gene_name`

### Ensembl

- `get_lookup_symbol`
  - Purpose: Gene symbol normalization
  - Body example:
```json
{"species":"homo_sapiens","symbol":"EGFR"}
```

### STRING

- `get_functional_annotation`
  - Purpose: Functional annotation and network support
  - Body example:
```json
{"identifiers":["EGFR","ERBB2"],"species":9606,"allow_pubmed":false,"only_pubmed":false}
```
  - Common errors:
    - Missing `allow_pubmed`
    - Missing `only_pubmed`

- `get_functional_enrichment`
  - Purpose: Pathway / functional enrichment
  - Body example:
```json
{"identifiers":["EGFR","ERBB2"],"species":9606,"background_string_identifiers":[]}
```
  - Common errors:
    - Missing `background_string_identifiers`

### ChEMBL

- `search_target`
  - Purpose: Query target entities
  - Body example:
```json
{"query_str":"EGFR"}
```

- `search_molecule`
  - Purpose: Query drugs / molecules
  - Body example:
```json
{"query_str":"osimertinib"}
```

- `get_drug_by_id`
  - Purpose: Retrieve drug details by ChEMBL ID
  - Body example:
```json
{"chembl_id":"CHEMBL3545063"}
```

### ClinicalTrials

- `get_studies`
  - Purpose: Search clinical trials
  - Body: Follow the current interface schema; pass at least a disease, drug, or keyword constraint — do not pass an empty object
  - Call requirements:
    - Prefer standard disease names or drug names
    - If too many results are returned, refine by phase, status, or region

### Search

- `tavily_search`
  - Purpose: Latest public progress, regulatory announcements, company news, trial web supplementation
  - Body example:
```json
{"query":"2025 2026 lung cancer FDA approvals EGFR MET DLL3"}
```

- `jina_search`
  - Purpose: Alternative web search
  - Body example:
```json
{"query":"lung cancer innovative drugs 2025"}
```

### PubChem / PDB

- For chemical entity or structure supplementation, pass standard entity names, CIDs, InChIKeys, PDB IDs, or target names according to each interface's schema.
- If field names are uncertain on the first call, refer to existing successful call examples or the tool schema; do not invent field names.

## 422 Handling Rules

- When a `422` occurs, first check `loc` and `msg` in the log:
  - `missing` indicates a missing field
  - Focus on correcting missing fields under `body`
- After the first `422`, you must:
  - Correct field names
  - Fill in all required fields
  - Retry the same MCP tool
- Only if the tool is reachable but still fails after multiple corrections is it permitted to fall back to an equivalent database or web search.

## Quality Checklist

- Has disease normalization been completed (including aliases/subtypes)?
- Has a four-layer evidence chain of mechanism/pathway–target–drug–clinical been provided?
- Has the role of KEGG/UniProt/STRING/Ensembl in key conclusions been clearly stated?
- Has entity normalization and alias deduplication been completed?
- Has tiered output been provided (approved / mid-to-late stage / frontier)?
- Have limitations, conflicts, and uncertainties been clearly stated?

## Reference Files

- [disease_to_drug_playbook.md](references/disease_to_drug_playbook.md): Complete SOP, routing strategy, internal JSON structures, and report template.
