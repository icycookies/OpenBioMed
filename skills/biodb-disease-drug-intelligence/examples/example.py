"""
Example: Using the biodb-disease-drug-intelligence skill

This file is a user-facing demonstration of how to invoke the skill and what
kind of workflow/output to expect. It is intentionally illustrative rather
than executable against a local SDK, because this skill is triggered by user
intent inside Codex/ChatGPT rather than by importing a Python package.
"""

from textwrap import dedent


# ============================================================
# SCENARIO: User wants an innovation landscape for a disease
# ============================================================

# Example user prompts that should trigger this skill:
EXAMPLE_PROMPTS = [
    "Help me analyze the current state of innovative drug research in colorectal cancer",
    "What are the noteworthy new drugs for Alzheimer's disease recently?",
    "I want to see the frontier pipeline drugs and key targets in the NASH field",
]


# ============================================================
# STEP 1: STRUCTURE THE REQUEST
# ============================================================

TASK_OBJECT = {
    "task_type": "disease_to_drug",
    "focus": "innovative_drugs",
    "disease_raw": "Colorectal cancer",
    "time_constraint": None,
    "region_constraint": "global",
    "stage_constraint": None,
}


# ============================================================
# STEP 2: EXPLAIN WHAT THE SKILL WILL DO
# ============================================================

WORKFLOW_OVERVIEW = dedent(
    """
    The skill will usually do the following:

    1. Standardize the disease name
       - Example: "Colorectal cancer" -> "Colorectal cancer"
       - Capture aliases, subtypes, and preferred search terms

    2. Map "innovative drugs" into an actionable scope
       - Approved representative innovative drugs
       - Mid/late-stage pipeline assets
       - Emerging mechanisms and future directions

    3. Build the evidence chain
       - KEGG: disease/pathway backbone
       - UniProt: protein function
       - STRING: network/pathway support
       - Ensembl: gene normalization
       - ChEMBL: target-drug mapping
       - ClinicalTrials: clinical status validation
       - Search: latest public updates when needed

    4. Produce a structured Chinese report
       - Executive summary
       - Key targets and mechanisms
       - Representative drugs by layer
       - Clinical progress
       - Trend judgment
       - Limitations and evidence boundaries
    """
).strip()


# ============================================================
# STEP 3: SHOW A CONCRETE EXAMPLE
# ============================================================

SIMULATED_RUN = {
    "disease_standardization": {
        "canonical_disease": "Colorectal cancer",
        "aliases": ["CRC", "colorectal cancer", "colorectal neoplasms"],
        "subtypes": ["MSI-H/dMMR", "BRAF V600E", "HER2-positive", "KRAS G12C"],
    },
    "key_mechanisms": [
        "EGFR-RAS-RAF-MEK-ERK",
        "PI3K-AKT",
        "PD-1/CTLA-4 immune checkpoint",
        "TGF-beta / tumor microenvironment remodeling",
    ],
    "representative_drugs": [
        {
            "name": "encorafenib",
            "layer": "Approved/Validated",
            "mechanism": "BRAF inhibitor",
            "population": "BRAF V600E mCRC",
        },
        {
            "name": "adagrasib",
            "layer": "Approved/Molecular stratification",
            "mechanism": "KRAS G12C inhibitor",
            "population": "KRAS G12C CRC, often combined with EGFR blockade",
        },
        {
            "name": "tucatinib",
            "layer": "Approved/Precision therapy",
            "mechanism": "HER2 TKI",
            "population": "HER2-positive mCRC",
        },
        {
            "name": "trastuzumab deruxtecan",
            "layer": "Mid/late-stage pipeline/Key tracking",
            "mechanism": "HER2 ADC",
            "population": "HER2-positive mCRC",
        },
        {
            "name": "pelareorep",
            "layer": "Frontier exploration",
            "mechanism": "oncolytic virus / immune activation",
            "population": "KRAS-mutant MSS mCRC",
        },
    ],
}


# ============================================================
# STEP 4: SHOW THE EXPECTED OUTPUT STYLE
# ============================================================

EXPECTED_OUTPUT = dedent(
    """
    [Colorectal Cancer Innovative Drug Intelligence Integration Report]

    0. Executive Summary
    - Innovative drug R&D for colorectal cancer has entered the era of molecular stratification.
    - The most mature directions focus on BRAF V600E, HER2-positive, KRAS G12C, and MSI-H/dMMR.
    - The largest unmet need remains in the MSS/pMMR population.

    4. Disease Mechanism, Pathway, and Molecular Evidence Analysis
    - KEGG supports that the core pathological axes of CRC include MAPK, PI3K-AKT, TGF-beta, etc.
    - UniProt/STRING support that EGFR, ERBB2, BRAF, KRAS, and PDCD1 are key nodes.

    6. Pipeline Drugs and R&D Landscape
    - Approved/validated representative innovative drugs: encorafenib, tucatinib, pembrolizumab
    - Mid/late-stage key assets: adagrasib + cetuximab, trastuzumab deruxtecan
    - Frontier exploration directions: oncolytic virus therapy, bispecific antibodies, immune microenvironment remodeling

    10. Summary and Opportunity Assessment
    - The real incremental opportunity lies not in extending traditional EGFR/VEGF approaches,
      but in MSS immune sensitization, novel ADCs, and post-resistance sequential strategies.
    """
).strip()


def demonstrate_skill_usage() -> None:
    print("=" * 72)
    print("BIODB DISEASE-DRUG INTELLIGENCE SKILL EXAMPLE")
    print("=" * 72)

    print("\n1. Example prompts")
    for idx, prompt in enumerate(EXAMPLE_PROMPTS, start=1):
        print(f"   {idx}. {prompt}")

    print("\n2. Structured task object")
    for key, value in TASK_OBJECT.items():
        print(f"   - {key}: {value}")

    print("\n3. Workflow overview")
    print(WORKFLOW_OVERVIEW)

    print("\n4. Simulated normalized disease")
    print(f"   - Canonical disease: {SIMULATED_RUN['disease_standardization']['canonical_disease']}")
    print(f"   - Aliases: {', '.join(SIMULATED_RUN['disease_standardization']['aliases'])}")
    print(f"   - Subtypes: {', '.join(SIMULATED_RUN['disease_standardization']['subtypes'])}")

    print("\n5. Key mechanisms")
    for item in SIMULATED_RUN["key_mechanisms"]:
        print(f"   - {item}")

    print("\n6. Representative drugs")
    for drug in SIMULATED_RUN["representative_drugs"]:
        print(f"   - {drug['name']} | {drug['layer']} | {drug['mechanism']} | {drug['population']}")

    print("\n7. Expected output style")
    print(EXPECTED_OUTPUT)

    print("\n" + "=" * 72)
    print("Notes")
    print("=" * 72)
    print("- This is a demonstration file, not a direct runtime entrypoint.")
    print("- The skill is normally triggered by a natural-language request.")
    print("- Use it when the user asks for innovative drugs, pipeline assets,")
    print("  frontier mechanisms, or a disease-to-drug landscape report.")


if __name__ == "__main__":
    demonstrate_skill_usage()
