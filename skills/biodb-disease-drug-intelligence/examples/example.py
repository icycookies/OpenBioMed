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
    "帮我分析一下结直肠癌的创新药研究现状",
    "阿尔茨海默病最近有哪些值得关注的新药？",
    "想看NASH领域的前沿在研药和关键靶点",
]


# ============================================================
# STEP 1: STRUCTURE THE REQUEST
# ============================================================

TASK_OBJECT = {
    "task_type": "disease_to_drug",
    "focus": "innovative_drugs",
    "disease_raw": "结直肠癌",
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
       - Example: "结直肠癌" -> "Colorectal cancer"
       - Capture aliases, subtypes, and preferred search terms

    2. Map "创新药" into an actionable scope
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
        "aliases": ["CRC", "结直肠癌", "colorectal neoplasms"],
        "subtypes": ["MSI-H/dMMR", "BRAF V600E", "HER2阳性", "KRAS G12C"],
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
            "layer": "已上市/已验证",
            "mechanism": "BRAF inhibitor",
            "population": "BRAF V600E mCRC",
        },
        {
            "name": "adagrasib",
            "layer": "已上市/分子分层",
            "mechanism": "KRAS G12C inhibitor",
            "population": "KRAS G12C CRC, often combined with EGFR blockade",
        },
        {
            "name": "tucatinib",
            "layer": "已上市/精准治疗",
            "mechanism": "HER2 TKI",
            "population": "HER2-positive mCRC",
        },
        {
            "name": "trastuzumab deruxtecan",
            "layer": "中后期在研/重点跟踪",
            "mechanism": "HER2 ADC",
            "population": "HER2-positive mCRC",
        },
        {
            "name": "pelareorep",
            "layer": "前沿探索",
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
    《结直肠癌 创新药情报整合报告》

    0. 执行摘要
    - 当前结直肠癌创新药研发已进入分子分层时代。
    - 最成熟方向集中在 BRAF V600E、HER2阳性、KRAS G12C、MSI-H/dMMR。
    - 最大未满足需求仍在 MSS/pMMR 人群。

    4. 疾病机制、通路与分子证据分析
    - KEGG 支持 CRC 的核心病理轴包括 MAPK、PI3K-AKT、TGF-beta 等。
    - UniProt/STRING 支持 EGFR、ERBB2、BRAF、KRAS、PDCD1 是关键节点。

    6. 在研药物与研发格局
    - 已上市/已验证代表性创新药：encorafenib, tucatinib, pembrolizumab
    - 中后期重点品种：adagrasib + cetuximab, trastuzumab deruxtecan
    - 前沿探索方向：病毒治疗、双抗、免疫微环境重塑

    10. 总结与机会判断
    - 真正的增量机会不在传统 EGFR/VEGF 拓展，而在 MSS 免疫增敏、
      新型 ADC、耐药后序贯策略。
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
