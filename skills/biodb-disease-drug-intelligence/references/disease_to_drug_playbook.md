# Disease-to-Innovative-Drug Playbook

## 1. Task Object

```json
{
  "task_type": "disease_to_drug",
  "focus": "innovative_drugs",
  "disease_raw": "diabetes mellitus",
  "time_constraint": null,
  "region_constraint": null,
  "stage_constraint": null
}
```

## 2. Disease Standardization Output Structure

```json
{
  "canonical_disease": "diabetes mellitus",
  "subtypes": ["type 1 diabetes mellitus", "type 2 diabetes mellitus"],
  "aliases": ["diabetes", "DM", "T1DM", "T2DM"],
  "preferred_query_terms": ["diabetes mellitus", "type 2 diabetes", "type 1 diabetes"]
}
```

## 3. Internal Definition of Innovative Drugs

```json
{
  "innovation_definition": {
    "include_new_mechanism": true,
    "include_recent_approved": true,
    "include_late_stage_pipeline": true,
    "include_frontier_candidates": true
  }
}
```

## 4. Fixed Subtask Chain

```json
{
  "subtasks": [
    "identify_targets_and_mechanisms",
    "enrich_pathway_and_target_evidence",
    "retrieve_representative_drugs",
    "build_drug_profiles",
    "validate_clinical_progress",
    "summarize_trends"
  ]
}
```

## 5. Database Routing Table (Based on Current BioDB Toolset)

| Subtask | Goal | Primary DB | Secondary DB | Output Focus |
|---|---|---|---|---|
| Disease standardization | Canonical name, aliases, subtypes | Internal rules | Search | Standardized disease entity |
| identify_targets_and_mechanisms | Find key targets and mechanism directions | KEGG, UniProt | STRING, Ensembl, ChEMBL | Pathways, targets, protein function backbone |
| enrich_pathway_and_target_evidence | Supplement molecular evidence and network support | UniProt, STRING, Ensembl | KEGG | Protein function, interaction network, gene annotation |
| retrieve_representative_drugs | Retrieve representative drugs and candidates | ChEMBL | PubChem | Drug entities, mechanisms, indications |
| build_drug_profiles | Build drug profiles | ChEMBL, PubChem | UniProt, Ensembl, PDB | Drug-target-structure-molecular evidence |
| validate_clinical_progress | Validate clinical advancement | ClinicalTrials | Search | Phase, status, NCT, region |
| summarize_trends | Trend summarization | ClinicalTrials, ChEMBL | KEGG, STRING, UniProt, Ensembl | Hot directions, R&D landscape, mechanism maturity |

Note: OpenTargets from the original plan was not found in the current BioDB tool catalog. This skill uses `KEGG + UniProt + STRING + Ensembl + ChEMBL` as the primary chain for disease-to-mechanism/target/drug mapping.

## 6. Query Priority and Granularity

Priority order:
1. Disease standardization and subtype decomposition (internal rules + Search)
2. Mechanism/pathway/target backbone (KEGG + UniProt + STRING + Ensembl)
3. Drug candidate pool and mechanism mapping (ChEMBL)
4. Clinical validation (ClinicalTrials)
5. Chemical and structural enrichment (PubChem/PDB)
6. Web fallback (Search)

Granularity strategy:
- Broad queries (e.g., "diabetes innovative drugs"): Start with an overview, then focus on high-activity subtypes.
- Mechanism-specific (e.g., "GLP-1 innovative drugs"): Lock in the mechanism first, then expand to drugs.
- Time-constrained (e.g., "last five years"): Increase weight for recent clinical trials and recent approvals.
- Region-constrained (e.g., "China"): Enhance ClinicalTrials + Search with regional filtering.

## 6.1 MCP Parameter Reference Table

The following are minimal viable request body examples for commonly used BioDB MCP tools. Always follow the interface schema strictly — do not rename fields based on semantics.

| Tool | Purpose | Correct body example | Common 422 cause |
|---|---|---|---|
| `kegg_find` | Disease/pathway/gene search | `{"db":"disease","query":"lung cancer"}` | Writing `db` as `database` |
| `get_general_info_by_protein_or_gene_name` | Protein/gene function info | `{"query":"EGFR"}` | Writing `query` as `protein_or_gene_name` |
| `get_lookup_symbol` | Ensembl gene normalization | `{"species":"homo_sapiens","symbol":"EGFR"}` | Missing `species` or `symbol` |
| `get_functional_annotation` | STRING functional annotation | `{"identifiers":["EGFR","ERBB2"],"species":9606,"allow_pubmed":false,"only_pubmed":false}` | Missing `allow_pubmed` / `only_pubmed` |
| `get_functional_enrichment` | STRING enrichment analysis | `{"identifiers":["EGFR","ERBB2"],"species":9606,"background_string_identifiers":[]}` | Missing `background_string_identifiers` |
| `search_target` | ChEMBL target search | `{"query_str":"EGFR"}` | Wrong field name |
| `search_molecule` | ChEMBL drug search | `{"query_str":"osimertinib"}` | Wrong field name |
| `get_drug_by_id` | ChEMBL drug details | `{"chembl_id":"CHEMBL3545063"}` | Wrong field name |
| `tavily_search` | Latest web search | `{"query":"2025 2026 lung cancer FDA approvals EGFR MET DLL3"}` | Empty query or wrong field name |
| `jina_search` | Alternative web search | `{"query":"lung cancer innovative drugs 2025"}` | Empty query or wrong field name |

Additional notes:
- For `ClinicalTrials`, `PubChem`, and `PDB` interfaces where field names are uncertain, always refer to successful call examples or the interface schema first.
- On first call failure, do not immediately switch databases. First check whether the `422` is caused by wrong field names, wrong field types, or missing required fields.

## 6.2 422 Error Handling Protocol

- `422 Unprocessable Entity` should first be interpreted as "request body does not conform to the interface schema," not as database unavailability.
- Required troubleshooting order:
  1. Check `loc` in the error log
  2. Check whether `msg` is `Field required`
  3. Fix missing fields in the `body`
  4. Retry the same interface with the corrected body
- Only switch to an alternative database or use `Search` as a supplement when:
  - The tool is reachable but still fails after multiple schema corrections
  - The tool itself is unresponsive or times out
  - The result quality is clearly insufficient

## 7. Evidence Integration and Deduplication

Drug primary key priority:
1. ChEMBL ID
2. Standard drug name
3. PubChem CID
4. ClinicalTrials intervention name (after normalization)

Target primary key priority:
1. UniProt accession / Ensembl gene / gene symbol
2. Standard target name
3. Aliases

Unified drug candidate pool structure:

```json
[
  {
    "drug_name": "...",
    "aliases": ["..."],
    "target": ["..."],
    "mechanism": "...",
    "evidence": {
      "chembl": {},
      "clinicaltrials": {},
      "mechanism_support": {}
    }
  }
]
```

## 8. Innovation Scoring (Simplified)

```json
{
  "disease_relevance": 0,
  "innovation": 0,
  "clinical_maturity": 0,
  "evidence_strength": 0,
  "representativeness": 0
}
```

Output layers:
- Approved/validated representative innovative drugs
- Mid/late-stage pipeline candidates
- Frontier exploration mechanism directions

## 9. Exception Fallback

- Disease too broad (e.g., "cancer innovative drugs"): Suggest narrowing to a specific cancer type first; otherwise output Top cancer types + Top mechanisms.
- Inconsistent evidence across databases: Explicitly state "mechanism evidence present, clinical evidence weak/not found."
- Too many results: Default to Top N output (recommended: 10).
- Too few results: Switch to "target directions + adjacent mechanisms + trend assessment."

## 10. Report Template (Standard Version)

```markdown
[{Disease Name} Innovative Drug Intelligence Integration Report]

0. Executive Summary
- Summary: Summarize the current state of innovative drug development for the disease in 5-8 sentences, covering the most noteworthy mechanism/pathway directions, representative assets, clinical progress, and potential opportunities.
- Core assessments:
  - Is the field currently highly crowded: {Yes/No + reason}
  - Most noteworthy mechanisms currently: {mechanism 1}, {mechanism 2}, {mechanism 3}
  - Most noteworthy assets to track: {asset 1}, {asset 2}, {asset 3}
  - Most noteworthy risks currently: {risk 1}, {risk 2}

1. Project Objectives
- Starting from the {disease name} indication, assess potential unmet clinical needs, innovative drug R&D opportunities, and differentiated entry points.
- Map disease mechanisms, pathways, key targets, pipeline assets, clinical progress, competitive landscape, regulatory highlights, and key deals.
- Provide structured decision support for new drug initiation, track assessment, BD evaluation, and competitive research.

2. Disease and Indication Analysis
2.1 Disease Overview and Market Analysis
- Disease definition, subtypes/staging, core clinical features
- Epidemiology: patient population, incidence, mortality, disease burden
- Treatment cost and payer landscape: treatment costs, insurance/accessibility
- Market overview: current market size, growth drivers, future outlook
- Note:
  - If reliable market data is unavailable, do not force specific figures; use qualitative assessments such as "mature market / fast-growing / still early stage"

2.2 Disease Population Characteristics
- Typical patient population
- Key subtypes/stratified populations
- High-risk populations or populations with significantly different treatment needs

2.3 Disease Diagnosis and Current Treatment
- Diagnostic criteria and commonly used assessment metrics
- Current standard-of-care regimens
- Limitations of existing treatments: insufficient efficacy, safety, resistance, adherence, dosing convenience
- Major comorbidities, complications, and prognostic factors

3. Unmet Clinical Needs
3.1 Overall Unmet Need
- Core problems not yet resolved by current treatments
- Gaps in efficacy
- Safety and tolerability issues
- Long-term management and adherence challenges
- Accessibility and payment barriers

3.2 Subpopulation Unmet Need
- Which subtypes/stages/comorbid populations lack better options
- Which populations respond poorly to current therapies
- Which problems may correspond to new R&D entry points

4. Disease Mechanism, Pathway, and Molecular Evidence Analysis
4.1 Disease Mechanisms
- Core biological mechanisms underlying disease onset and progression
- Key pathological steps and their links to clinical phenotypes

4.2 Key Signaling Pathways
- Major signaling pathways and their roles in the disease
- Which pathways are most relevant to current drug development
- Recommended explicit distinction:
  - `KEGG`: pathway-level evidence
  - `UniProt`: protein function-level evidence
  - `STRING`: network/interaction support
  - `Ensembl`: gene nomenclature, transcripts, homology supplement

4.3 Mechanism-to-Drug Mapping
- Which mechanism steps are targeted by current major drugs
- Which mechanisms are well-validated vs. still exploratory

5. Target Analysis
5.1 Target Screening and Prioritization
- Overview of candidate targets
- Priority assessment across the following dimensions:
  - Disease relevance
  - Biological rationale
  - Clinical translatability
  - Pipeline activity
  - Differentiation potential

Recommended summary table:

| Target | Mechanism | Evidence Strength | Key Evidence Sources | Pipeline Activity | Highest Stage | Priority |
|---|---|---|---|---|---|---|
| {target1} | {mechanism} | {High/Medium/Low} | {KEGG/UniProt/STRING/Ensembl/ChEMBL} | {High/Medium/Low} | {stage} | {High/Medium/Low} |

5.2 Pipeline Target Types, Counts, and Stages
- Overview of target distribution
- Number of pipeline assets per target
- Highest development stage and crowding level per target

5.3 Mechanisms of Action for Pipeline Targets
- Mechanism classification for each key target
- Which are mature mechanisms
- Which are novel targets/mechanisms

5.4 Target Feasibility Analysis
- Level of support from literature, clinical data, patents, and public information
- Key questions to address:
  1. Which patient subpopulation might correspond to drugs against this target in {disease name}
  2. Could this target become a first-line or core treatment direction in the future
  3. Is the relationship of this target to existing therapies more substitutive, combinatorial, or complementary
  4. How does this target differ from other pipeline targets in the same indication
  5. Could this target improve the efficacy or safety limitations of current drugs
- Must explicitly distinguish:
  - Direct evidence
  - Synthesized inference
  - Recommended judgment
- For each key target, prioritize stating:
  - `UniProt accession`
  - `Ensembl gene ID` (if available)
  - Key `STRING` interactions or network support

5.5 Novel Target/Mechanism Progress
- Targets/mechanisms that have emerged or gained momentum in recent years
- Their unique clinical value
- Whether they may become a key opportunity direction in the future

5.6 SWOT Analysis
- SWOT comparison for key mechanisms or targets
- If a full analysis is not feasible, at minimum provide a four-column summary table: Strengths / Weaknesses / Opportunities / Threats

6. Innovative Drug and Pipeline Asset Analysis
6.1 Global Approved/Pipeline Asset Overview
- Target distribution
- Mechanism distribution
- Drug type distribution: small molecule / biologic / peptide / antibody / cell & gene therapy, etc.
- Highest development stage distribution
- Major R&D companies

Recommended table format:

| Drug Name | Development Code | Company | Target/Mechanism | Indication (subtype/stage) | Drug Type | Highest Stage | Region | Key Evidence Sources |
|---|---|---|---|---|---|---|---|---|
| {drug1} | {code1} | {company1} | {target/mechanism} | {indication} | {type} | {phase} | Global | {ChEMBL/ClinicalTrials/PubChem/...} |

6.2 China Approved/Pipeline Asset Overview
- Target distribution of China pipeline assets
- Major companies in China
- Differentiated directions from Chinese companies

Recommended table format:

| Drug Name | Development Code | Company | Target/Mechanism | Indication (subtype/stage) | Drug Type | Highest Stage | China Stage | Key Evidence Sources |
|---|---|---|---|---|---|---|---|---|
| {drug_cn_1} | {code_cn_1} | {company_cn_1} | {target/mechanism} | {indication} | {type} | {phase} | {cn_phase} | {ChEMBL/ClinicalTrials/Search/...} |

6.3 Key Asset Deep Dives
- Recommend expanding on 3-8 key assets, each as a separate card

[Key Asset Card Template]

6.3.x {Asset Name} ({Development Code})
- Company:
- Target/Mechanism:
- Drug Type:
- Current Highest Stage:
- Primary Indications:
- Key Database Evidence:
  - {ChEMBL ID / ClinicalTrials NCT / PubChem CID / UniProt / Ensembl / PDB (if available)}
- Key Trials:
  - {NCT / trial name / phase / status}
- Development Progress:
  - Clinical stage, trial design, primary endpoints, publicly available preliminary results
- Innovation Points:
  - Differentiated value compared to existing therapies or similar pipeline assets
- Market Outlook:
  - Potential commercial value, competitive positioning, future uptake rationale
- Patents and Protection:
  - If information is available, list patent types, key countries/regions, expiry dates, SPC status, etc.
  - If no reliable information is available, explicitly state "public patent information not systematically verified"
- Key Risks:
  - Efficacy risk / safety risk / class competition / commercialization risk / regulatory risk

7. Competitive Company Analysis
7.1 Global Competitive Landscape
- Major global companies and their core pipelines
- Each company's strategic focus in this space
- Competitive relationships between approved products and pipeline assets

7.2 China Competitive Landscape
- Domestic Chinese companies and companies with China presence
- Which companies have positions in key mechanisms
- Potential differentiated strategies in the China market

Recommended summary table:

| Company | Representative Asset/Pipeline | Target/Mechanism | Highest Stage | Region | Competitive Position |
|---|---|---|---|---|---|
| {company1} | {asset1} | {mechanism1} | {phase1} | {global/cn} | {leader/challenger/niche} |

8. Regulatory Highlights
8.1 China NMPA
- Any review concerns, label risks, or approval trends

8.2 US FDA
- Any black box warnings, advisory committee discussions, clinical holds, withdrawal reasons, or label restrictions

8.3 EU EMA
- Any review divergences, risk communications, or special requirements

8.4 Japan PMDA / Ministry of Health, Labour and Welfare
- Supplement with key public information if available

8.5 Regulatory Risk Interpretation
- Do not simply reproduce original text
- Focus on interpreting:
  - What the adverse effects imply
  - Which risks may actually represent differentiation opportunities

9. Key Deals in the Disease Area
- Summarize important licensing deals, collaborations, M&A, asset transactions, and milestone events in the disease area
- Deal value, timing, parties, assets, mechanism directions
- Use capital flow to identify hot targets, hot assets, and track focus areas

Recommended summary table:

| Date | Deal Type | Parties | Asset | Target/Mechanism | Value/Milestones | Significance |
|---|---|---|---|---|---|---|
| {date1} | {licensing/M&A/collab} | {party_a} / {party_b} | {asset1} | {mechanism1} | {deal_value} | {why_it_matters} |

10. Summary and Opportunity Assessment
- Summarize the current state of the disease area
- Most noteworthy target/mechanism directions currently
- Which directions are relatively crowded
- Which directions still have differentiation opportunities
- Which assets are worth continued tracking
- If initiating a new project, what entry logic is recommended

11. Result Notes and Limitations
- This report is an integration of multi-database and public information
- Typical database coverage includes: `KEGG`, `UniProt`, `STRING`, `Ensembl`, `ChEMBL`, `ClinicalTrials`, `PubChem`, `PDB`, `Search`
- "Innovative drugs" is an information integration scope, not equivalent to a strict regulatory definition
- If market size, patents, deal values, and similar information have not been systematically verified, they must be labeled as "limited public information available"
- For novel targets and early-stage projects, clearly distinguish facts, inferences, and recommendations
- If a web fallback is triggered, state: which `Search` queries were performed, what is still missing, and why an external source was used
```
