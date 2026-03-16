---
name: biodb-disease-drug-intelligence
description: 面向生物医药问答场景的“疾病到创新药综合分析”技能。用于回答“某疾病有哪些创新药/前沿药/在研药/新机制药”等问题，输出疾病-靶点-通路-药物-临床进展-机制趋势的一体化证据报告。适用于需要联合 BioDB MCP（ChEMBL、ClinicalTrials、KEGG、UniProt、STRING、PubChem、Ensembl、PDB、Search）进行多数据库查询、去重归一、创新性筛选与结构化报告生成的任务。
---

# BioDB 疾病创新药情报整合

## 概述

将自然语言问题（如“阿尔茨海默病最近有哪些值得关注的新药？”）转换为可执行的多库查询计划。  
生成面向决策的中文综合报告，而非仅返回药名列表。

## 快速开始

1. 识别是否属于 `disease_to_drug` 场景。
2. 标准化疾病实体并拆解“创新药”意图。
3. 按固定子任务链执行多数据库查询。
4. 做实体归一、证据整合、创新性筛选与分层输出。
5. 生成中文报告并标注证据边界。

详细的数据结构、路由表、评分规则、数据库角色分工和创新药情报模板见 [disease_to_drug_playbook.md](references/disease_to_drug_playbook.md)。

## 触发与判定

当用户问题同时包含以下信息时，触发本技能：
- 疾病实体：如糖尿病、肺癌、阿尔茨海默病、肥胖症、NASH、RA。
- 药物创新意图：如创新药、新机制药、在研药、前沿药、值得关注的新药。

若只提“癌症创新药”等过宽问题，先建议缩小病种；若用户不愿缩小，默认给 Top 癌种与 Top 机制概览。

## 工作流（固定骨架）

### Step 0 问题结构化
构造任务对象（示例）：
```json
{
  "task_type": "disease_to_drug",
  "focus": "innovative_drugs",
  "disease_raw": "糖尿病",
  "time_constraint": null,
  "region_constraint": null,
  "stage_constraint": null
}
```

### Step 1 疾病标准化
输出 `canonical_disease`、`subtypes`、`aliases`、`preferred_query_terms`。  
若用户未指定亚型，先做总疾病分析，再强调研发更活跃亚型（例如 diabetes 下优先覆盖 T2DM）。

### Step 2 创新药定义映射
将“创新药”映射为可执行准则：
- 新机制/新靶点（含 first-in-class 倾向）
- 近年代表性获批药
- 中后期在研候选（II/III 期优先）
- 前沿方向（双/多靶点、新一代优化分子）

### Step 3 子任务拆分
固定执行 6 个子任务：
- `identify_targets_and_mechanisms`
- `enrich_pathway_and_target_evidence`
- `retrieve_representative_drugs`
- `build_drug_profiles`
- `validate_clinical_progress`
- `summarize_trends`

### Step 4 数据库执行顺序
默认顺序：
1. 疾病标准化与别名补充：内部规则 + `Search`（仅疾病名歧义或亚型缺失时）
2. 机制、通路与靶点骨架：`KEGG` + `UniProt` + `STRING` + `Ensembl`
3. 靶点到药物映射：`ChEMBL(target/mechanism)` + `ChEMBL(molecule/drug/indication)`
4. 临床推进验证：`ClinicalTrials`
5. 结构、化学与分子补充：`PubChem` + `PDB`（可选）
6. 网页兜底：`Search`（仅数据库不足或最新监管/公告核验需要时）

说明：
- 当前 BioDB 工具集中未包含 OpenTargets 服务，本技能使用 `KEGG + UniProt + STRING + Ensembl + ChEMBL` 组合作为“疾病到机制/靶点/药物”主链路替代。
- `Ensembl` 的主要职责是基因符号归一、转录本/家族/同源信息补充，不替代 `UniProt` 的蛋白功能信息。

### Step 5 证据整合与去重
优先主键：
- 药物：`ChEMBL ID > 标准药名 > PubChem CID > ClinicalTrials intervention`
- 靶点：`UniProt accession / Ensembl gene / 基因符号 > 标准靶点名 > 别名`

必须保留别名、剂型、基因/蛋白 ID 映射信息，避免错误合并（如 semaglutide 不同制剂、同基因不同转录本或蛋白别名）。

### Step 6 创新性筛选与排序
按 0-5 分打分并综合排序：
- `disease_relevance`
- `innovation`
- `clinical_maturity`
- `evidence_strength`
- `representativeness`

输出必须分层：
- 已上市/已验证代表性创新药
- 中后期在研候选药
- 前沿探索机制方向

### Step 7 报告生成
默认必须先读取 `references/disease_to_drug_playbook.md` 中的 `## 10. 中文报告模板（标准版）`，并严格按照该模板的章节顺序与字段骨架输出最终报告。

仅当用户明确要求以下情况之一时，才允许偏离标准模板：
- 简版/摘要版/口语版
- 表格版/清单版
- 特定章节裁剪
- 用户指定的其他明确格式

若用户未明确要求改格式，则不得使用自由发挥的报告结构；即使回答较短，也要保持标准模板的主章节骨架。

使用中文分析体裁输出，至少包含：
- 结论先行
- 关键靶点/机制
- 代表性药物分层清单
- 临床试验进展概览
- 研发趋势判断
- 结果局限与证据边界

### Step 8 异常兜底
- 结果过多：按代表性+创新性取 Top N（默认 10）。
- 结果过少：优先输出靶点方向与邻近机制，不强行凑药物列表。
- 证据冲突：明确写出“分子证据存在/临床证据有限”。
- 约束缺失：默认 `time_constraint=null, region_constraint=global`，并在报告中显式声明。

## 工具调用约束

- 先跑主链路（`KEGG + UniProt + STRING + Ensembl -> ChEMBL -> ClinicalTrials`），再做 `PubChem/PDB/Search` 补强，不要反过来。
- `KEGG` 负责疾病-通路骨架，`UniProt` 负责蛋白功能与条目归一，`STRING` 负责网络/互作支持，`Ensembl` 负责基因命名、转录本与同源补充，`ChEMBL` 负责药物-靶点-机制映射，`ClinicalTrials` 负责临床阶段核验，`PubChem/PDB` 负责化学与结构补充。
- 当需要网页补充、最新进展核验、监管公告核实或数据库结果不足时，必须优先使用 BioDB MCP 中的 `Search` 能力。
- 优先使用 `Search` 的含义包括：允许并鼓励进行多轮检索、改写 query、按疾病亚型拆分检索、按药物/试验/公司/监管来源分别检索，以及交叉核对多个结果。
- `Search` 不足不等于“第一次检索未命中”；只有在经过合理的多轮 `Search` 检索后，仍无法获得足够相关、足够新、或足够可信的一手来源时，才视为不足。
- 只有在 `Search` 工具不可用、经过多轮检索后结果仍明显不足、或仍无法满足时效性与来源核验要求时，才允许使用外部网页搜索作为最后兜底。
- 若最终使用了外部网页搜索，必须在结果说明或局限部分明确说明：已经进行了哪些 `Search` 检索、仍缺失什么信息、因此才触发外部搜索；不得默认绕过 BioDB MCP `Search`。
- 若缺失关键字段（phase/status/target/pathway/gene_id/protein_id/structure），必须触发补查。
- 报告中的每个关键结论至少有一条可追溯证据（数据库名 + 实体主键或标准条目 ID）。
- 不把“创新药”当监管定义；它是信息整合定义，必须在结果说明中声明。

## MCP 参数规范表

以下字段名必须按 MCP 接口 schema 原样传递，不要按语义猜测字段名。若接口返回 `422 Unprocessable Entity`，优先根据报错中的 `missing` 字段修正请求体并重试，不要直接切换外部搜索。

### KEGG

- `kegg_find`
  - 用途：疾病、通路、基因等关键词查找
  - body 示例：
```json
{"db":"disease","query":"lung cancer"}
```
  - 常见错误：
    - 把 `db` 写成 `database`

### UniProt

- `get_general_info_by_protein_or_gene_name`
  - 用途：按蛋白名或基因名查询基础功能信息
  - body 示例：
```json
{"query":"EGFR"}
```
  - 常见错误：
    - 把 `query` 写成 `protein_or_gene_name`

### Ensembl

- `get_lookup_symbol`
  - 用途：基因符号标准化
  - body 示例：
```json
{"species":"homo_sapiens","symbol":"EGFR"}
```

### STRING

- `get_functional_annotation`
  - 用途：功能注释与网络支持
  - body 示例：
```json
{"identifiers":["EGFR","ERBB2"],"species":9606,"allow_pubmed":false,"only_pubmed":false}
```
  - 常见错误：
    - 漏掉 `allow_pubmed`
    - 漏掉 `only_pubmed`

- `get_functional_enrichment`
  - 用途：通路/功能富集
  - body 示例：
```json
{"identifiers":["EGFR","ERBB2"],"species":9606,"background_string_identifiers":[]}
```
  - 常见错误：
    - 漏掉 `background_string_identifiers`

### ChEMBL

- `search_target`
  - 用途：查靶点实体
  - body 示例：
```json
{"query_str":"EGFR"}
```

- `search_molecule`
  - 用途：查药物/分子
  - body 示例：
```json
{"query_str":"osimertinib"}
```

- `get_drug_by_id`
  - 用途：按 ChEMBL ID 拉药物详情
  - body 示例：
```json
{"chembl_id":"CHEMBL3545063"}
```

### ClinicalTrials

- `get_studies`
  - 用途：检索临床试验
  - body：以接口当前 schema 为准；至少先传疾病、药物或关键词约束，不要直接传空对象
  - 调用要求：
    - 优先用标准疾病名或药名
    - 返回过多时再按阶段、状态或地域细化

### Search

- `tavily_search`
  - 用途：最新公开进展、监管公告、公司新闻、试验网页补充
  - body 示例：
```json
{"query":"2025 2026 lung cancer FDA approvals EGFR MET DLL3"}
```

- `jina_search`
  - 用途：网页检索备选
  - body 示例：
```json
{"query":"lung cancer innovative drugs 2025"}
```

### PubChem / PDB

- 若需要化学实体或结构补充，按各自接口 schema 传标准实体名、CID、InChIKey、PDB ID 或靶点名。
- 若首次调用不确定字段名，先参考已有成功调用样例或工具 schema，不要自行发明字段。

## 422 处理规则

- 出现 `422` 时，先看日志中的 `loc` 和 `msg`：
  - `missing` 表示缺字段
  - 重点修正 `body` 下缺失字段
- 第一次 `422` 后必须：
  - 修正字段名
  - 补齐必填字段
  - 重新调用同一 MCP 工具
- 只有在工具可达但多次校正后仍失败，才允许改用同类数据库或网页兜底。

## 质量检查清单

- 是否完成疾病标准化（含别名/亚型）？
- 是否给出机制/通路-靶点-药物-临床四层证据链？
- 是否明确 KEGG/UniProt/STRING/Ensembl 在关键结论中的角色分工？
- 是否完成实体归一和别名去重？
- 是否分层输出（上市/中后期/前沿）？
- 是否明确局限、冲突与不确定性？

## 参考文件

- [disease_to_drug_playbook.md](references/disease_to_drug_playbook.md)：完整 SOP、路由策略、内部 JSON 结构、中文报告模板。
