# Disease-to-Innovative-Drug Playbook（中文）

## 1. 任务对象

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

## 2. 疾病标准化输出结构

```json
{
  "canonical_disease": "diabetes mellitus",
  "subtypes": ["type 1 diabetes mellitus", "type 2 diabetes mellitus"],
  "aliases": ["diabetes", "DM", "T1DM", "T2DM"],
  "preferred_query_terms": ["diabetes mellitus", "type 2 diabetes", "type 1 diabetes"]
}
```

## 3. 创新药内部定义

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

## 4. 固定子任务链

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

## 5. 数据库路由表（按当前 BioDB 工具集）

| 子任务 | 目标 | 主数据库 | 辅数据库 | 输出重点 |
|---|---|---|---|---|
| 疾病标准化 | 标准名称、别名、亚型 | 内部规则 | Search | 标准疾病实体 |
| identify_targets_and_mechanisms | 找关键靶点与机制方向 | KEGG, UniProt | STRING, Ensembl, ChEMBL | 通路、靶点、蛋白功能骨架 |
| enrich_pathway_and_target_evidence | 补充分子证据与网络支持 | UniProt, STRING, Ensembl | KEGG | 蛋白功能、互作网络、基因注释 |
| retrieve_representative_drugs | 拉取代表性药物与候选药 | ChEMBL | PubChem | 药物实体、机制、适应症 |
| build_drug_profiles | 构建药物画像 | ChEMBL, PubChem | UniProt, Ensembl, PDB | 药物-靶点-结构-分子证据 |
| validate_clinical_progress | 验证临床推进 | ClinicalTrials | Search | phase、status、NCT、地区 |
| summarize_trends | 趋势归纳 | ClinicalTrials, ChEMBL | KEGG, STRING, UniProt, Ensembl | 热门方向、研发格局、机制成熟度 |

说明：你原方案中的 OpenTargets 在当前 BioDB 工具目录中未发现对应 server，故本技能使用 `KEGG + UniProt + STRING + Ensembl + ChEMBL` 作为疾病到机制/靶点/药物主链路替代。

## 6. 查询优先级与粒度

优先级：
1. 疾病标准化与亚型拆分（内部规则 + Search）
2. 机制/通路/靶点骨架（KEGG + UniProt + STRING + Ensembl）
3. 药物候选池与机制映射（ChEMBL）
4. 临床验证（ClinicalTrials）
5. 化学与结构补强（PubChem/PDB）
6. 网页核验兜底（Search）

粒度策略：
- 宽泛问题（如“糖尿病创新药”）：先总体，再聚焦高活跃亚型。
- 机制限定（如“GLP-1 创新药”）：先机制锁定，再扩药物。
- 时间限定（如“近五年”）：提高近期临床与近年获批权重。
- 地域限定（如“中国”）：ClinicalTrials + Search 做地域过滤增强。

## 6.1 MCP 参数规范表

以下为当前 BioDB MCP 常用工具的最小可用请求体示例。调用时必须优先遵守接口 schema，不要按语义自行改字段名。

| 工具 | 用途 | 正确 body 示例 | 常见 422 原因 |
|---|---|---|---|
| `kegg_find` | 疾病/通路/基因检索 | `{"db":"disease","query":"lung cancer"}` | 把 `db` 写成 `database` |
| `get_general_info_by_protein_or_gene_name` | 蛋白/基因功能信息 | `{"query":"EGFR"}` | 把 `query` 写成 `protein_or_gene_name` |
| `get_lookup_symbol` | Ensembl 基因标准化 | `{"species":"homo_sapiens","symbol":"EGFR"}` | `species` 或 `symbol` 缺失 |
| `get_functional_annotation` | STRING 功能注释 | `{"identifiers":["EGFR","ERBB2"],"species":9606,"allow_pubmed":false,"only_pubmed":false}` | 漏掉 `allow_pubmed` / `only_pubmed` |
| `get_functional_enrichment` | STRING 富集分析 | `{"identifiers":["EGFR","ERBB2"],"species":9606,"background_string_identifiers":[]}` | 漏掉 `background_string_identifiers` |
| `search_target` | ChEMBL 靶点检索 | `{"query_str":"EGFR"}` | 字段名错误 |
| `search_molecule` | ChEMBL 药物检索 | `{"query_str":"osimertinib"}` | 字段名错误 |
| `get_drug_by_id` | ChEMBL 药物详情 | `{"chembl_id":"CHEMBL3545063"}` | 字段名错误 |
| `tavily_search` | 最新网页检索 | `{"query":"2025 2026 lung cancer FDA approvals EGFR MET DLL3"}` | 空 query 或字段名错误 |
| `jina_search` | 备选网页检索 | `{"query":"lung cancer innovative drugs 2025"}` | 空 query 或字段名错误 |

补充说明：
- `ClinicalTrials`、`PubChem`、`PDB` 相关接口若字段名存在不确定性，应优先参考成功调用样例或接口 schema。
- 第一次调用失败时，不要立刻切换数据库；优先检查是否是字段名、字段类型或必填字段缺失导致的 `422`。

## 6.2 422 报错处理规范

- `422 Unprocessable Entity` 优先解释为“请求体不符合接口 schema”，而不是数据库不可用。
- 必做排查顺序：
  1. 查看日志中的 `loc`
  2. 查看 `msg` 是否为 `Field required`
  3. 修正 `body` 中缺失字段
  4. 使用修正后的 body 重新请求同一接口
- 只有在：
  - 工具可达但多次 schema 修正后仍失败
  - 或工具本身无响应/超时
  - 或结果质量明显不足
  时，才允许切换同类数据库或使用 `Search` 补充。

## 7. 证据整合与去重

药物主键优先级：
1. ChEMBL ID
2. 标准药名
3. PubChem CID
4. ClinicalTrials intervention name（归并后）

靶点主键优先级：
1. UniProt accession / Ensembl gene / gene symbol
2. 标准 target name
3. 别名

统一药物候选池结构：

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

## 8. 创新性评分（简化版）

```json
{
  "disease_relevance": 0,
  "innovation": 0,
  "clinical_maturity": 0,
  "evidence_strength": 0,
  "representativeness": 0
}
```

输出分层：
- 已上市/已验证代表性创新药
- 中后期在研候选药
- 前沿探索机制方向

## 9. 异常兜底

- 疾病过宽（如“癌症创新药”）：先建议缩小癌种；否则输出 Top 癌种 + Top 机制。
- 库间证据不一致：明确写“机制证据有、临床证据弱/未检出”。
- 结果过多：默认输出 Top N（建议 10）。
- 结果过少：转为“靶点方向 + 邻近机制 + 趋势判断”。

## 10. 中文报告模板（标准版）

```markdown
《{疾病名称} 创新药情报整合报告》

0. 执行摘要
- 结论摘要：用 5-8 句话概括疾病创新药现状、最值得关注的机制/通路方向、代表性品种、临床推进和潜在机会。
- 核心判断：
  - 当前领域是否高度拥挤：{是/否 + 原因}
  - 当前最值得关注的机制：{机制1}、{机制2}、{机制3}
  - 当前最值得跟踪的品种：{品种1}、{品种2}、{品种3}
  - 当前最值得关注的风险：{风险1}、{风险2}

1. 项目目标
- 从 {疾病名称} 适应症出发，评估潜在未满足临床需求、创新药研发机会与差异化切入点。
- 梳理疾病机制、通路、重点靶点、在研品种、临床推进、竞争格局、监管要点和核心交易。
- 为新药立项、赛道判断、BD 评估和竞争调研提供结构化决策支持。

2. 疾病与适应症分析
2.1 疾病现状与市场分析
- 疾病定义、分型/分期、核心临床特征
- 流行病学：患病人数、发病率、死亡率、疾病负担
- 治疗费用与支付端：治疗成本、医保/可及性情况
- 市场概况：当前市场规模、增长驱动因素、未来预期
- 说明：
  - 如果没有可靠市场数据，不强行给出具体金额，可改为“市场成熟/快速增长/仍处早期”的定性判断

2.2 疾病人群特征
- 典型患者人群
- 关键亚型/分层人群
- 高风险人群或治疗需求差异明显的人群

2.3 疾病诊断与治疗现状
- 诊断标准与常用评估指标
- 当前标准治疗方案
- 现有治疗局限：疗效不足、安全性、耐药、依从性、给药便利性
- 主要合并症、并发症与预后影响

3. 未满足的临床需求
3.1 总体 unmet need
- 当前治疗仍未解决的核心问题
- 疗效不足的环节
- 安全性与耐受性问题
- 长期管理与依从性难点
- 可及性与支付限制

3.2 细分人群 unmet need
- 哪些亚型/阶段/伴随疾病人群缺乏更优方案
- 当前疗法在哪些人群中效果不佳
- 哪些问题可能对应新的研发切入点

4. 疾病机制、通路与分子证据分析
4.1 疾病机制
- 疾病发生发展的核心生物学机制
- 关键病理环节及其与临床表型的联系

4.2 关键信号通路
- 主要信号通路及其在疾病中的作用
- 哪些通路与当前药物开发最相关
- 建议显式区分：
  - `KEGG`：通路级证据
  - `UniProt`：蛋白功能级证据
  - `STRING`：网络/互作支持
  - `Ensembl`：基因命名、转录本、同源补充

4.3 机制到药物的映射
- 当前主要药物分别切入哪些机制环节
- 已被充分验证的机制与仍处探索阶段的机制分别是什么

5. 靶点分析
5.1 靶点筛选与优先级排序
- 候选靶点总览
- 按以下维度给出优先级判断：
  - 疾病相关性
  - 生物学合理性
  - 临床可转化性
  - 在研热度
  - 差异化潜力

建议用简表呈现：

| 靶点 | 作用机制 | 证据强度 | 主要证据来源 | 在研热度 | 最高阶段 | 优先级判断 |
|---|---|---|---|---|---|
| {target1} | {mechanism} | {高/中/低} | {KEGG/UniProt/STRING/Ensembl/ChEMBL} | {高/中/低} | {阶段} | {高/中/低} |

5.2 在研靶点种类、数量和阶段
- 靶点分布概况
- 不同靶点下在研品种数量
- 各靶点的最高开发阶段与拥挤程度

5.3 在研靶点的作用机制
- 各重点靶点的机制分类
- 哪些是成熟机制
- 哪些是新靶点/新机制

5.4 靶点可行性分析
- 文献、临床、专利和公开信息支持程度
- 重点回答以下问题：
  1. 该靶点药物在 {疾病名称} 中可能对应的细分人群是谁
  2. 该靶点未来是否可能成为一线或核心治疗方向
  3. 该靶点与现有疗法的关系更偏替代、联用还是补充
  4. 该靶点与同适应症其他在研靶点相比有何差异
  5. 该靶点是否可能改善当前药物的疗效或安全性短板
- 必须明确区分：
  - 直接证据
  - 综合推断
  - 建议性判断
- 对于每个重点靶点，优先说明：
  - `UniProt accession`
  - `Ensembl gene ID`（若有）
  - 关键 `STRING` 互作或网络支持

5.5 新靶点/新机制进展
- 近几年新增或升温的靶点/机制
- 其独特临床价值是什么
- 是否可能成为未来重点机会方向

5.6 SWOT 分析
- 对重点机制或靶点做 SWOT 对比
- 如果无法完整展开，可至少给出“优势/劣势/机会/威胁”四栏简表

6. 创新药与在研品种分析
6.1 全球已上市/在研品种概况
- 靶点分布
- 机制分布
- 药品类型分布：化学药 / 生物药 / 多肽 / 抗体 / 细胞基因治疗等
- 最高研发阶段分布
- 主要研发企业

建议用表格呈现：

| 药品名称 | 研发代码 | 公司 | 靶点/机制 | 适应症（分型/分期） | 药品类型 | 最高阶段 | 地区 | 关键证据来源 |
|---|---|---|---|---|---|---|---|
| {drug1} | {code1} | {company1} | {target/mechanism} | {indication} | {type} | {phase} | Global | {ChEMBL/ClinicalTrials/PubChem/...} |

6.2 中国已上市/在研品种概况
- 中国在研品种靶点分布
- 中国主要参与公司
- 中国本土差异化方向

建议用表格呈现：

| 药品名称 | 研发代码 | 公司 | 靶点/机制 | 适应症（分型/分期） | 药品类型 | 最高阶段 | 中国阶段 | 关键证据来源 |
|---|---|---|---|---|---|---|---|
| {drug_cn_1} | {code_cn_1} | {company_cn_1} | {target/mechanism} | {indication} | {type} | {phase} | {cn_phase} | {ChEMBL/ClinicalTrials/Search/...} |

6.3 重点品种分析
- 建议展开 3-8 个重点品种，每个品种单独成卡

【重点品种卡片模板】

6.3.x {品种名称}（{研发代码}）
- 公司：
- 靶点/机制：
- 药品类型：
- 当前最高阶段：
- 主要适应症：
- 关键数据库证据：
  - {ChEMBL ID / ClinicalTrials NCT / PubChem CID / UniProt / Ensembl / PDB（如有）}
- 关键试验：
  - {NCT / 试验名称 / 阶段 / 状态}
- 研发进展：
  - 临床阶段、试验设计、主要观察终点、公开初步结果
- 创新点：
  - 相比现有疗法或同类在研品种的差异化价值
- 市场前景：
  - 潜在商业价值、竞争位置、未来放量逻辑
- 专利与保护：
  - 若有信息，列明专利类型、重点国家/地区、到期时间、是否有 SPC 等
  - 若无可靠信息，明确写“公开专利信息未系统核实”
- 主要风险：
  - 疗效风险 / 安全性风险 / 同类竞争 / 商业化风险 / 监管风险

7. 疾病领域竞争公司分析
7.1 全球竞争公司分析
- 全球主要参与公司及其核心管线
- 各公司在该赛道的布局重点
- 已上市产品与在研品种之间的竞争关系

7.2 中国竞争公司分析
- 中国本土公司和中国区布局公司
- 哪些公司在重点机制上有布局
- 中国市场可能出现的差异化打法

建议用简表呈现：

| 公司 | 代表产品/管线 | 靶点/机制 | 最高阶段 | 区域 | 竞争定位 |
|---|---|---|---|---|---|
| {company1} | {asset1} | {mechanism1} | {phase1} | {global/cn} | {leader/challenger/niche} |

8. 监管要点
8.1 中国 NMPA
- 是否存在审评关注点、说明书风险、审批趋势

8.2 美国 FDA
- 是否有黑框警告、咨询委讨论、临床 hold、撤市原因、标签限制等

8.3 欧盟 EMA
- 是否有审评分歧、风险沟通或特殊要求

8.4 日本 PMDA / 厚生劳动省
- 若有公开要点，做补充

8.5 监管风险解读
- 不需要堆原文
- 重点解读：
  - 毒副作用意味着什么
  - 哪些风险可能反而构成差异化机会

9. 疾病领域核心交易
- 梳理该疾病领域的重要授权、合作、并购、资产交易和里程碑事件
- 交易金额、时间、双方、资产、机制方向
- 通过资金流向判断热点靶点、热点品种与赛道关注点

建议用简表呈现：

| 时间 | 交易类型 | 双方 | 资产/品种 | 靶点/机制 | 金额/里程碑 | 含义 |
|---|---|---|---|---|---|---|
| {date1} | {licensing/M&A/collab} | {party_a} / {party_b} | {asset1} | {mechanism1} | {deal_value} | {why_it_matters} |

10. 总结与机会判断
- 总结疾病领域现状
- 当前最值得关注的靶点/机制方向
- 哪些方向相对拥挤
- 哪些方向仍有差异化机会
- 哪些品种值得持续跟踪
- 如果要立项，建议优先考虑的切入逻辑是什么

11. 结果说明与局限
- 本报告为多数据库与公开信息整合结果
- 典型数据库覆盖包括：`KEGG`、`UniProt`、`STRING`、`Ensembl`、`ChEMBL`、`ClinicalTrials`、`PubChem`、`PDB`、`Search`
- “创新药”是信息整合口径，不等同于严格监管定义
- 市场规模、专利、交易金额等信息若未系统核验，必须标注“公开信息有限”
- 对于新靶点和早期项目，应明确区分事实、推断与建议
- 若触发网页兜底，需说明：已进行哪些 `Search` 检索、仍缺什么、为何触发外部来源
```
