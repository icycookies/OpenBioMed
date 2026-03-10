# OpenBioMed MCP 服务文档

## 项目简介

`open_biomed_mcp` 是一个基于 FastAPI + MCP（Model Context Protocol）的生物医学工具服务平台。该平台针对当前生物医学工具碎片化的问题，通过对 OrigeneMCP 和 Biomni 等主流开源项目的整合、去重与规范化处理，实现了多源异构生物医学工具的统一封装。它原生支持 MCP（Model Context Protocol） 标准，并同步暴露 FastAPI 驱动的 RESTful 接口，为大模型（LLM）调用、智能 Agent 开发及传统科研流提供了“开箱即用”的多模态接入能力。

项目版本：`0.2.0`

---

## 服务总览

本项目共集成 **32 个工具模块**，分为两大类：

### 一、生物数据库 API 服务（13 个模块）

| 模块 | 路径前缀 | 说明 |
|------|----------|------|
| **ChEMBL** | `/chembl` | 生物活性数据库，提供化合物活性、检测、药物、靶点等查询 |
| **NCBI** | `/ncbi` | 美国国家生物技术信息中心，提供基因、基因组、分类学、病毒等数据查询 |
| **PubChem** | `/pubchem` | 化合物信息数据库，支持按名称/SMILES/CID/分子式搜索化合物及其性质 |
| **UniProt** | `/uniprot` | 蛋白质知识库，提供 UniProtKB、UniRef、UniParc、蛋白质组等查询 |
| **KEGG** | `/kegg` | 通路与基因组数据库，支持通路、基因、化合物的检索与转换 |
| **STRING** | `/string` | 蛋白质相互作用网络数据库，提供网络交互、功能富集、PPI 分析 |
| **TCGA** | `/tcga` | 癌症基因组图谱，分析基因在不同癌症类型中的表达模式 |
| **Ensembl** | `/ensembl` | 基因组注释数据库，提供基因查找、变异效应预测（VEP）、同源性分析、序列检索等 |
| **UCSC** | `/ucsc` | UCSC 基因组浏览器 API，提供基因组序列、轨道数据、染色体信息查询 |
| **ClinicalTrials** | `/clinicaltrials` | ClinicalTrials.gov 临床试验数据库，支持临床试验搜索与详情查询 |
| **PDB** | `/pdb` | 蛋白质数据库，提供蛋白质结构、实体、组装、化学组分等查询 |
| **DBSearch** | `/dbsearch` | 综合数据库搜索工具，集成 ClinVar、Ensembl、GSEA、GTRD、miRDB、MouseMine、PHIPSTER 等 |
| **Search** | `/search_tools` | 搜索引擎工具，集成 Tavily 搜索和 Jina DeepSearch |

### 二、生物医学计算工具集（19 个模块）

| 模块 | 路径前缀 | 说明 |
|------|----------|------|
| **文献检索** | `/literature` | 论文补充信息获取、文献搜索 |
| **生物化学** | `/biochemistry` | 圆二色谱分析、蛋白质结构分析等 |
| **生物成像** | `/bioimaging` | 图像分割、显微镜图像分析 |
| **生物工程** | `/bioengineering` | 细胞迁移分析、组织工程相关工具 |
| **生物物理** | `/biophysics` | 蛋白质无序区域预测（IUPred2A）等 |
| **糖工程** | `/glycoengineering` | N-糖基化位点查找等 |
| **癌症生物学** | `/cancer_biology` | DNA 损伤响应网络分析等 |
| **细胞生物学** | `/cell_biology` | 细胞周期分析、细胞计数等 |
| **分子生物学** | `/molecular_biology` | ORF 注释、质粒注释、PCR 模拟、限制性酶切、引物比对等 |
| **遗传学** | `/genetics` | 基因组坐标转换（hg19/hg38）等 |
| **免疫学** | `/immunology` | ATAC-seq 峰值检测、差异可及性分析等 |
| **微生物学** | `/microbiology` | 厌氧消化过程优化等 |
| **病理学** | `/pathology` | 心血管成像分析、主动脉几何参数计算等 |
| **药理学** | `/pharmacology` | 分子对接（DiffDock）等 |
| **生理学** | `/physiology` | MRI 面部解剖 3D 建模等 |
| **合成生物学** | `/synthetic_biology` | 细菌基因组改造、治疗递送设计等 |
| **系统生物学** | `/systems_biology` | 通量平衡分析（FBA）等 |
| **辅助工具** | `/support_tools` | Python REPL 执行、源码读取、Synapse 数据下载 |
| **实验室自动化** | `/lab_automation` | PyLabRobot 脚本测试等 |

---

## 各模块核心功能详解

### ChEMBL（生物活性数据）共101个工具
- 活性数据查询与搜索（`get_activity`、`search_activity`）
- 检测信息查询（`get_assay_by_id`、`search_assay`）
- ATC 分类查询（`get_atc_class`）
- 结合位点查询（`get_binding_site`）
- 药物信息查询（`get_drug`、`get_drug_indication`、`get_drug_warning`）
- 化合物记录与结构警报（`get_compound_record`、`get_compound_structural_alert`）
- 文献查询与相似度分析（`get_document`、`get_document_similarity`）
- ChEMBL ID 查找（`get_chembl_id_lookup`）

### NCBI（基因与基因组）共56个工具
- 基因元数据查询（`get_gene_metadata_by_gene_name`）
- 基因 ID/登录号/符号/分类单元查询
- 基因组注释报告、序列报告、修订历史
- 病毒注释与基因组数据
- 分类学信息查询与建议
- 生物样本报告、细胞器数据
- 基因直系同源物查询

### PubChem（化合物信息）共39个工具
- 按名称/SMILES/CID/分子式搜索化合物
- 化合物详细信息（性质、同义词、描述、3D 结构）
- 物质信息查询（SID）
- 生物测定摘要
- 基因/蛋白质/分类学摘要
- 构象异构体查询
- 子结构 CAS 号查询

### UniProt（蛋白质知识库）共22个工具
- UniProtKB 条目查询与搜索
- UniRef 簇查询与成员检索
- UniParc 条目与交叉引用
- GeneCentric 基因中心查询
- 蛋白质组查询

### KEGG（通路与基因组）共6个工具
- 数据库信息查询（`kegg_info`）
- 数据搜索（`kegg_find`）
- 条目列表（`kegg_list`）
- 条目详情获取（`kegg_get`）
- ID 转换（`kegg_conv`）
- 交叉引用链接（`kegg_link`）

### STRING（蛋白质网络）共8个工具
- 标识符映射（`mapping_identifiers`）
- 网络交互查询（`get_string_network_interaction`）
- 全部交互伙伴查询
- 蛋白质相似性评分
- 跨物种最佳相似性匹配
- 功能富集分析
- 功能注释
- PPI 富集分析

### Ensembl（基因组注释）共104个工具
- 基因符号查找（`get_lookup_symbol`）
- 同源性分析（`get_homology_symbol`、`get_homology_id`）
- 基因组序列检索（`get_sequence_region`）
- 变异效应预测 VEP（`get_vep_hgvs`、`get_vep_id`、`get_vep_region`）
- 基因树与 CAFE 分析
- 组装信息与区域信息
- 交叉引用查询
- 坐标映射（cDNA/CDS/蛋白质 → 基因组）
- 本体查询
- 表型关联查询
- 变异信息与重编码

### UCSC（基因组浏览器）共9个工具
- 基因组列表与染色体列表
- 轨道数据查询
- DNA 序列获取
- 细胞带信息
- 公共轨道中心

### ClinicalTrials（临床试验）共8个工具
- 临床试验搜索（支持复杂查询、过滤、分页）
- 单个试验详情查询
- 元数据、搜索区域、枚举值查询
- 字段统计信息

### PDB（蛋白质结构）共20个工具
- 结构信息查询
- PubMed/UniProt/DrugBank 注释
- 聚合物/分支/非聚合物实体及实例查询
- 结构组装信息
- 聚合物界面分析
- 化学组分查询
- 残基链信息
- 实体组查询

### TCGA（癌症基因组图谱）共1个工具
- 基因在不同癌症类型中的表达模式分析（`get_gene_specific_expression_in_cancer_type`）：基于 Firebrowse API（TCGA mRNASeq），计算指定基因在各癌症队列中的平均表达量及 z 分数，返回高表达（z > 1）和低表达（z < -1）的癌症类型

### Search（搜索引擎工具）共2个工具
- Tavily 搜索（`tavily_search`）：使用 Tavily 搜索引擎检索并过滤网络结果
- Jina DeepSearch（`jina_search`）：使用 Jina DeepSearch 引擎进行深度检索

### DBSearch（综合数据库搜索）共14个工具
- ClinVar 变异显著性查询
- 蛋白质序列 BLAST 匹配
- 基因组区域基因查询
- 细胞遗传学带区域基因提取
- GSEA 基因集检索
- GTRD 转录因子靶基因查询
- miRDB miRNA 靶基因预测
- MouseMine 表型基因查询
- PHIPSTER 病毒-人类蛋白质相互作用查询

### 文献检索（Literature）共8个工具
- 通过 DOI 获取论文补充信息（`fetch_supplementary_info_from_doi`）
- arXiv 论文搜索（`query_arxiv`）
- Google Scholar 学术搜索（`query_scholar`）
- PubMed 文献搜索（`query_pubmed`）
- Google 搜索（`search_google`）
- URL 内容提取（`extract_url_content`）
- PDF 内容提取（`extract_pdf_content`）
- 基于 Claude 的高级网络搜索（`advanced_web_search_claude`）

### 生物化学（Biochemistry）共6个工具
- 圆二色谱（CD）光谱分析（`analyze_circular_dichroism_spectra`）
- RNA 二级结构特征分析（`analyze_rna_secondary_structure_features`）
- 蛋白酶动力学分析（`analyze_protease_kinetics`）
- 酶动力学测定分析（`analyze_enzyme_kinetics_assay`）
- ITC 结合热力学分析（`analyze_itc_binding_thermodynamics`）
- 蛋白质保守性分析（`analyze_protein_conservation`）

### 生物成像（Bioimaging）共9个工具
- 多模态图像拆分（`split_modalities`）
- nnU-Net 输入准备（`prepare_input_for_nnunet`）
- nnU-Net 图像分割（`segment_with_nn_unet`）
- 分割结果可视化（`create_segmentation_visualization`）
- 快速刚性配准（`quick_rigid_registration`）
- 快速仿射配准（`quick_affine_registration`）
- 快速可变形配准（`quick_deformable_registration`）
- 批量图像配准（`batch_register_images`）
- 相似度指标计算（`calculate_similarity_metrics`）
- 配准结果可视化（`create_registration_visualization`）

### 生物工程（Bioengineering）共7个工具
- 细胞迁移指标分析（`analyze_cell_migration_metrics`）
- CRISPR-Cas9 基因组编辑模拟（`perform_crispr_cas9_genome_editing`）
- 钙成像数据分析（`analyze_calcium_imaging_data`）
- 体外药物释放动力学分析（`analyze_in_vitro_drug_release_kinetics`）
- 肌纤维形态学分析（`analyze_myofiber_morphology`）
- 神经轨迹行为解码（`decode_behavior_from_neural_trajectories`）
- 全细胞 ODE 模型模拟（`simulate_whole_cell_ode_model`）

### 生物物理（Biophysics）共3个工具
- 蛋白质无序区域预测（`predict_protein_disorder_regions`）
- 细胞形态与细胞骨架分析（`analyze_cell_morphology_and_cytoskeleton`）
- 组织变形流分析（`analyze_tissue_deformation_flow`）

### 糖工程（Glycoengineering）共3个工具
- N-糖基化位点查找（`find_n_glycosylation_motifs`）
- O-糖基化热点预测（`predict_o_glycosylation_hotspots`）
- 糖工程资源列表（`list_glycoengineering_resources`）

### 癌症生物学（Cancer Biology）共6个工具
- DNA 损伤响应网络分析（`analyze_ddr_network_in_cancer`）
- 细胞衰老与凋亡分析（`analyze_cell_senescence_and_apoptosis`）
- 体细胞突变检测与注释（`detect_and_annotate_somatic_mutations`）
- 结构变异检测与表征（`detect_and_characterize_structural_variations`）
- 基因表达 NMF 分析（`perform_gene_expression_nmf_analysis`）
- 拷贝数/纯度/倍性及局灶事件分析（`analyze_copy_number_purity_ploidy_and_focal_events`）

### 细胞生物学（Cell Biology）共5个工具
- 显微镜图像细胞周期相位量化（`quantify_cell_cycle_phases_from_microscopy`）
- 细胞运动性量化与聚类（`quantify_and_cluster_cell_motility`）
- 荧光激活细胞分选 FACS（`perform_facs_cell_sorting`）
- 流式细胞术免疫表型分析（`analyze_flow_cytometry_immunophenotyping`）
- 线粒体形态与膜电位分析（`analyze_mitochondrial_morphology_and_potential`）

### 分子生物学（Molecular Biology）共18个工具
- 开放阅读框（ORF）注释（`annotate_open_reading_frames`）
- 质粒注释（`annotate_plasmid`）
- 基因编码序列检索（`get_gene_coding_sequence`）
- 质粒序列检索（Addgene/NCBI）（`get_plasmid_sequence`）
- 引物比对（`align_sequences`）
- PCR 扩增模拟（`pcr_simple`）
- 限制性酶切模拟（`digest_sequence`）
- 限制性酶切位点查找（`find_restriction_sites`、`find_restriction_enzymes`）
- 序列突变查找（`find_sequence_mutations`）
- CRISPR sgRNA 设计（`design_knockout_sgrna`）
- 寡核苷酸退火方案（`get_oligo_annealing_protocol`）
- Golden Gate 组装方案与模拟（`get_golden_gate_assembly_protocol`、`golden_gate_assembly`）
- Golden Gate 寡核苷酸设计（`design_golden_gate_oligos`）
- 细菌转化方案（`get_bacterial_transformation_protocol`）
- 引物设计（`design_primer`）
- Sanger 测序验证引物设计（`design_verification_primers`）

### 遗传学（Genetics）共9个工具
- 基因组坐标转换 hg19/hg38（`liftover_coordinates`）
- 贝叶斯精细定位（深度变分推断）（`bayesian_finemapping_with_deep_vi`）
- Cas9 突变结果分析（`analyze_cas9_mutation_outcomes`）
- CRISPR 基因组编辑结果分析（`analyze_crispr_genome_editing`）
- 人口统计历史模拟（msprime）（`simulate_demographic_history`）
- 转录因子结合位点识别（`identify_transcription_factor_binding_sites`）
- 基因组预测线性混合模型（`fit_genomic_prediction_model`）
- PCR 扩增与凝胶电泳模拟（`perform_pcr_and_gel_electrophoresis`）
- 蛋白质系统发育分析（`analyze_protein_phylogeny`）

### 免疫学（Immunology）共10个工具
- ATAC-seq 差异可及性分析（`analyze_atac_seq_differential_accessibility`）
- 细菌生长曲线分析（`analyze_bacterial_growth_curve`）
- 免疫细胞分离与纯化模拟（`isolate_purify_immune_cells`）
- 细胞周期相位持续时间估算（`estimate_cell_cycle_phase_durations`）
- 流动条件下免疫细胞追踪（`track_immune_cells_under_flow`）
- CFSE 细胞增殖分析（`analyze_cfse_cell_proliferation`）
- CD4+ T 细胞细胞因子产生分析（`analyze_cytokine_production_in_cd4_tcells`）
- EBV 抗体滴度 ELISA 分析（`analyze_ebv_antibody_titers`）
- CNS 病变组织学分析（`analyze_cns_lesion_histology`）
- 免疫组织化学图像分析（`analyze_immunohistochemistry_image`）

### 微生物学（Microbiology）共12个工具
- 厌氧消化过程优化（`optimize_anaerobic_digestion_process`）
- 砷形态 HPLC-ICP-MS 分析（`analyze_arsenic_speciation_hplc_icpms`）
- 细菌菌落计数（计算机视觉）（`count_bacterial_colonies`）
- 细菌基因组注释（Prokka）（`annotate_bacterial_genome`）
- 系列稀释 CFU 计数（`enumerate_bacterial_cfu_by_serial_dilution`）
- 细菌种群动态建模（ODE）（`model_bacterial_growth_dynamics`）
- 生物膜生物量量化（结晶紫）（`quantify_biofilm_biomass_crystal_violet`）
- 微生物细胞分割与形态分析（`segment_and_analyze_microbial_cells`）
- 深度学习细胞分割（Cellpose/Omnipose）（`segment_cells_with_deep_learning`）
- 微生物群落动态模拟（gLV 模型）（`simulate_generalized_lotka_volterra_dynamics`）
- RNA 二级结构预测（ViennaRNA）（`predict_rna_secondary_structure`）
- 微生物种群随机模拟（Gillespie 算法）（`simulate_microbial_population_dynamics`）

### 病理学（Pathology）共7个工具
- 主动脉直径与几何形状分析（`analyze_aortic_diameter_and_geometry`）
- ATP 发光测定分析（`analyze_atp_luminescence_assay`）
- 血栓组织学图像分析（`analyze_thrombus_histology`）
- 细胞内钙浓度分析（Rhod-2）（`analyze_intracellular_calcium_with_rhod2`）
- 角膜神经纤维量化（`quantify_corneal_nerve_fibers`）
- 多通道组织图像细胞分割与蛋白质量化（`segment_and_quantify_cells_in_multiplexed_images`）
- 骨微结构 micro-CT 分析（`analyze_bone_microct_morphometry`）

### 药理学（Pharmacology）共25个工具
- DiffDock 分子对接（`run_diffdock_with_smiles`）
- AutoDock Vina 分子对接（`docking_autodock_vina`）
- AutoSite 结合位点识别（`run_autosite`）
- TxGNN 药物重定位预测（`retrieve_topk_repurposing_drugs_from_disease_txgnn`）
- ADMET 属性预测（`predict_admet_properties`）
- 蛋白质-小分子结合亲和力预测（`predict_binding_affinity_protein_1d_sequence`）
- 药物制剂加速稳定性分析（`analyze_accelerated_stability_of_pharmaceutical_formulations`）
- 3D 软骨聚集培养测定方案（`run_3d_chondrogenic_aggregate_assay`）
- VCOG-CTCAE 不良事件分级（`grade_adverse_events_using_vcog_ctcae`）
- 放射性标记抗体生物分布分析（`analyze_radiolabeled_antibody_biodistribution`）
- α 粒子放射治疗剂量估算（`estimate_alpha_particle_radiotherapy_dosimetry`）
- 全甲基化组关联研究 MWAS（`perform_mwas_cyp2c19_metabolizer_status`）
- 理化性质计算（`calculate_physicochemical_properties`）
- 异种移植肿瘤生长抑制分析（`analyze_xenograft_tumor_growth_inhibition`）
- Western blot 像素分布分析（`analyze_pixel_distribution`）
- Western blot ROI 检测（`find_roi_from_image`）
- Western blot 密度测定分析（`analyze_western_blot`）
- 药物-药物相互作用查询（DDInter）（`query_drug_interactions`）
- 药物组合安全性检查（`check_drug_combination_safety`）
- 药物相互作用机制分析（`analyze_interaction_mechanisms`）
- 替代药物查找（`find_alternative_drugs_ddinter`）
- FDA 不良事件查询（`query_fda_adverse_events`）
- FDA 药物标签信息检索（`get_fda_drug_label_info`）
- FDA 药物召回检查（`check_fda_drug_recalls`）
- FDA 安全信号分析（`analyze_fda_safety_signals`）

### 生理学（Physiology）共11个工具
- MRI 面部解剖 3D 重建（`reconstruct_3d_face_from_mri`）
- 听觉脑干反应 ABR 波形分析（`analyze_abr_waveform_p1_metrics`）
- 纤毛摆动频率分析（FFT）（`analyze_ciliary_beat_frequency`）
- 蛋白质共定位分析（`analyze_protein_colocalization`）
- 昼夜节律余弦分析（`perform_cosinor_analysis`）
- 脑 ADC 图计算（扩散加权 MRI）（`calculate_brain_adc_map`）
- 内溶酶体钙动力学分析（`analyze_endolysosomal_calcium_dynamics`）
- 脂肪酸组成气相色谱分析（`analyze_fatty_acid_composition_by_gc`）
- 血流动力学参数分析（`analyze_hemodynamic_data`）
- 甲状腺激素药代动力学模拟（`simulate_thyroid_hormone_pharmacokinetics`）
- β-淀粉样蛋白斑块量化（`quantify_amyloid_beta_plaques`）

### 合成生物学（Synthetic Biology）共8个工具
- 细菌基因组治疗递送改造（`engineer_bacterial_genome_for_therapeutic_delivery`）
- 细菌生长速率分析（`analyze_bacterial_growth_rate`）
- 条形码测序数据分析（`analyze_barcode_sequencing_data`）
- 分岔图分析（`analyze_bifurcation_diagram`）
- SBML 生化网络模型生成（`create_biochemical_network_sbml_model`）
- 密码子优化（异源表达）（`optimize_codons_for_heterologous_expression`）
- 基因调控回路动力学模拟（含生长反馈）（`simulate_gene_circuit_with_growth_feedback`）
- 脂肪酸合酶功能域识别（`identify_fas_functional_domains`）

### 系统生物学（Systems Biology）共7个工具
- 通量平衡分析 FBA（`perform_flux_balance_analysis`）
- 蛋白质二聚化网络建模（`model_protein_dimerization_network`）
- 代谢网络扰动模拟（`simulate_metabolic_network_perturbation`）
- 蛋白质信号网络动力学模拟（`simulate_protein_signaling_network`）
- 蛋白质结构比较（`compare_protein_structures`）
- 肾素-血管紧张素系统动力学模拟（`simulate_renin_angiotensin_system_dynamics`）
- DNA 序列功能问答（ChatNT）（`query_chatnt`）

### 辅助工具（Support Tools）共3个工具
- Python REPL 执行（`run_python_repl`）
- 函数源码读取（`read_function_source_code`）
- Synapse 数据下载（`download_synapse_data`）

### 实验室自动化（Lab Automation）共3个工具
- PyLabRobot 脚本测试（`test_pylabrobot_script`）
- PyLabRobot 液体处理文档（`get_pylabrobot_documentation_liquid`）
- PyLabRobot 材料处理文档（`get_pylabrobot_documentation_material`）

---

## 如何启动项目

### 1. 环境准备

```bash
# 进入项目目录
cd /OpenBioMed/open_biomed_mcp

# 创建并激活 conda 环境（推荐 Python 3.11+）
conda create -n biomed_mcp python=3.11
conda activate biomed_mcp

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置环境变量

编辑 `.env` 文件，配置必要的 API Key：

```env
tavily_api_key = "your_tavily_api_key"
jina_api_key = "your_jina_api_key"
```

### 3. 启动服务

```bash
# 使用 uvicorn 启动（开发模式）
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 或使用 fastapi CLI 启动
fastapi dev main.py --host 0.0.0.0 --port 8000
```

启动后可访问：
- API 文档：`http://localhost:8000/docs`（Swagger UI）
- 健康检查：`http://localhost:8000/healthz`
- 工具摘要：`http://localhost:8000/tools/summary`

---

## 如何使用 MCP 服务

本项目支持 **三种接入方式**：

### 方式一：REST API 调用

所有工具都注册为 FastAPI 端点，可通过 HTTP POST 请求调用。

```bash
# 示例：通过基因名称查询基因元数据
curl -X POST "http://localhost:8000/tools/ncbi/get_gene_metadata_by_gene_name" \
  -H "Content-Type: application/json" \
  -d '{"name": "BRCA1", "species": "human"}'

# 示例：搜索化合物
curl -X POST "http://localhost:8000/tools/pubchem/search_pubchem_by_name" \
  -H "Content-Type: application/json" \
  -d '{"name": "aspirin"}'

# 示例：查询蛋白质交互网络
curl -X POST "http://localhost:8000/tools/string/get_string_network_interaction" \
  -H "Content-Type: application/json" \
  -d '{"identifiers": ["TP53", "BRCA1"], "species": 9606, "required_score": 700, "add_nodes": 5, "network_type": "physical", "show_query_node_labels": 1}'
```

完整的 API 文档可在 `http://localhost:8000/docs` 查看。

### 方式二：MCP SSE 协议接入

项目同时暴露了 MCP SSE 端点，支持 MCP 客户端（如 Kiro、Claude Desktop 等）直接连接。

**全局 MCP 端点**（包含所有工具）：
```
http://localhost:8000/mcp
```

**按模块拆分的 MCP 端点**（每个模块独立）：
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

### 方式三：在 AI IDE / Agent 中配置 MCP

在支持 MCP 的 AI 工具（如 Kiro、Claude Desktop、Cursor 等）中配置 MCP 服务器。

**Kiro 配置示例**（`.kiro/settings/mcp.json`）：

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

如果只需要特定模块，可以单独配置（用哪个直接配置对应的MCP）例如：

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

**Claude Desktop 配置示例**（`claude_desktop_config.json`）：

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

## 项目结构

```
open_biomed_mcp/
├── main.py                    # FastAPI 应用入口
├── registry.py                # MCP 工具注册中心
├── mcp_to_fastapi.py          # MCP → FastAPI 适配器
├── .env                       # 环境变量配置
├── requirements.txt           # Python 依赖
└── tools/                     # 工具模块目录
    ├── biodb/                 # 外部数据库 API 服务
    │   ├── chembl/            # ChEMBL 数据库
    │   ├── ncbi/              # NCBI 数据库
    │   ├── pubchem/           # PubChem 数据库
    │   ├── uniprot/           # UniProt 数据库
    │   ├── kegg/              # KEGG 数据库
    │   ├── STRING/            # STRING 数据库
    │   ├── search/            # 搜索引擎（Tavily/Jina）
    │   ├── tcga/              # TCGA 癌症基因组
    │   ├── ensembl/           # Ensembl 基因组注释
    │   ├── ucsc/              # UCSC 基因组浏览器
    │   ├── clinicaltrials/    # ClinicalTrials.gov
    │   ├── pdb/               # PDB 蛋白质结构
    │   └── dbsearch/          # 综合数据库搜索
    └── biocomputing/          # Biocomputing 生物医学计算工具集
        ├── mcp_to_fastapi.py  # Biocomputing MCP 适配器
        ├── tool_registry.py   # 工具注册器
        ├── tool_description/  # 工具描述定义
        ├── literature.py      # 文献检索
        ├── biochemistry.py    # 生物化学
        ├── bioimaging.py      # 生物成像
        ├── bioengineering.py  # 生物工程
        ├── biophysics.py      # 生物物理
        ├── glycoengineering.py # 糖工程
        ├── cancer_biology.py  # 癌症生物学
        ├── cell_biology.py    # 细胞生物学
        ├── molecular_biology.py # 分子生物学
        ├── genetics.py        # 遗传学
        ├── immunology.py      # 免疫学
        ├── microbiology.py    # 微生物学
        ├── pathology.py       # 病理学
        ├── pharmacology.py    # 药理学
        ├── physiology.py      # 生理学
        ├── synthetic_biology.py # 合成生物学
        ├── systems_biology.py # 系统生物学
        ├── support_tools.py   # 辅助工具
        └── lab_automation.py  # 实验室自动化
```

---

## 架构说明

```
┌─────────────────────────────────────────────────────┐
│                    客户端                             │
│  (AI Agent / 浏览器 / curl / MCP Client)             │
└──────────┬──────────────────┬───────────────────────┘
           │ REST API         │ MCP SSE
           ▼                  ▼
┌──────────────────────────────────────────────────────┐
│                  FastAPI Application                  │
│                                                      │
│  /tools/*          → REST API 端点                   │
│  /mcp              → 全局 MCP SSE 端点               │
│  /{module}/mcp     → 模块级 MCP SSE 端点             │
│  /docs             → Swagger API 文档                │
│  /healthz          → 健康检查                        │
│  /tools/summary    → 工具摘要                        │
└──────────┬───────────────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────────────┐
│              MCPToolsRegistry (注册中心)              │
│                                                      │
│  ┌─────────┐ ┌──────┐ ┌─────────┐ ┌──────────────┐  │
│  │ ChEMBL  │ │ NCBI │ │ PubChem │ │ ... 更多模块  │  │
│  │ FastMCP │ │FastMCP│ │ FastMCP │ │   FastMCP    │  │
│  └─────────┘ └──────┘ └─────────┘ └──────────────┘  │
│                                                      │
│  ┌──────────────────────────────────────────────┐    │
│  │         生物计算工具集 (19 个子模块)           │    │
│  │  每个子模块独立 FastMCP 服务器                 │    │
│  └──────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────┘
```

每个工具模块内部都是一个独立的 `FastMCP` 服务器实例，通过 `MCPToolsRegistry` 统一注册到 FastAPI 应用中，同时生成 REST API 端点和 MCP SSE 端点。
