description = [
    {
        "description": "分析癌症样本中的 DNA 损伤响应 (DDR) 网络改变和依赖性。",
        "name": "analyze_ddr_network_in_cancer",
        "optional_parameters": [
            {
                "default": "./results",
                "description": "保存输出文件的目录",
                "name": "output_dir",
                "type": "str",
            }
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "基因表达数据文件的路径（CSV 格式，基因为行，样本为列）",
                "name": "expression_data_path",
                "type": "str",
            },
            {
                "default": None,
                "description": "突变数据文件的路径（CSV 格式，基因为行，样本为列，值表示突变状态）",
                "name": "mutation_data_path",
                "type": "str",
            },
        ],
    },
    {
        "description": "分析流式细胞术数据以量化衰老和凋亡细胞群体。",
        "name": "analyze_cell_senescence_and_apoptosis",
        "optional_parameters": [],
        "required_parameters": [
            {
                "default": None,
                "description": "包含流式细胞术数据的 FCS 文件路径，包含衰老相关 β-半乳糖苷酶 (SA-β-Gal) 和 Annexin V/7-AAD 染色的测量数据",
                "name": "fcs_file_path",
                "type": "str",
            }
        ],
    },
    {
        "description": "使用 GATK Mutect2 进行变异调用、GATK FilterMutectCalls 进行过滤以及 SnpEff 进行功能注释，检测并注释肿瘤样本相对于匹配正常样本的体细胞突变。",
        "name": "detect_and_annotate_somatic_mutations",
        "optional_parameters": [
            {
                "default": "GRCh38.105",
                "description": "用于注释的 SnpEff 数据库",
                "name": "snpeff_database",
                "type": "str",
            }
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "肿瘤样本 BAM 文件的路径",
                "name": "tumor_bam",
                "type": "str",
            },
            {
                "default": None,
                "description": "匹配正常样本 BAM 文件的路径",
                "name": "normal_bam",
                "type": "str",
            },
            {
                "default": None,
                "description": "参考基因组 FASTA 文件的路径",
                "name": "reference_genome",
                "type": "str",
            },
            {
                "default": None,
                "description": "输出文件的前缀",
                "name": "output_prefix",
                "type": "str",
            },
        ],
    },
    {
        "description": "使用 LUMPY 进行结构变异检测，然后使用 COSMIC 和/或 ClinVar 数据库进行注释，检测并表征基因组测序数据中的结构变异 (SV)。",
        "name": "detect_and_characterize_structural_variations",
        "optional_parameters": [
            {
                "default": None,
                "description": "用于癌症注释的 COSMIC 数据库路径",
                "name": "cosmic_db_path",
                "type": "str",
            },
            {
                "default": None,
                "description": "用于临床注释的 ClinVar 数据库路径",
                "name": "clinvar_db_path",
                "type": "str",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "BAM 格式的比对测序数据路径",
                "name": "bam_file_path",
                "type": "str",
            },
            {
                "default": None,
                "description": "FASTA 格式的参考基因组路径",
                "name": "reference_genome_path",
                "type": "str",
            },
            {
                "default": None,
                "description": "保存结果的目录",
                "name": "output_dir",
                "type": "str",
            },
        ],
    },
    {
        "description": "对基因表达数据执行非负矩阵分解 (NMF)，以提取元基因及其相关的样本权重，用于肿瘤亚型识别。",
        "name": "perform_gene_expression_nmf_analysis",
        "optional_parameters": [
            {
                "default": 10,
                "description": "要提取的元基因（组分）数量。",
                "name": "n_components",
                "type": "int",
            },
            {
                "default": True,
                "description": "在应用 NMF 之前是否归一化表达数据。",
                "name": "normalize",
                "type": "bool",
            },
            {
                "default": "nmf_results",
                "description": "保存输出文件的目录。",
                "name": "output_dir",
                "type": "str",
            },
            {
                "default": 42,
                "description": "用于可重复性的随机种子。",
                "name": "random_state",
                "type": "int",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "包含基因表达数据的 CSV 或 TSV 文件路径，基因为行，样本为列。值应为非负数。",
                "name": "expression_data_path",
                "type": "str",
            }
        ],
    },
    {
        "description": "基于 CNVkit 的拷贝数工作流，执行 CNV 分段、纯度和倍性近似、简化的 HRD 风格指标，以及选定基因中的局灶性扩增/缺失检测。",
        "name": "analyze_copy_number_purity_ploidy_and_focal_events",
        "optional_parameters": [
            {
                "name": "normal_bam",
                "type": "str",
                "default": None,
                "description": "匹配正常样本 BAM 的路径（推荐用于 CNVkit）",
            },
            {
                "name": "output_dir",
                "type": "str",
                "default": "cn_analysis_results",
                "description": "存储 CNVkit 工作流输出的目录",
            },
            {
                "name": "targets_bed",
                "type": "str",
                "default": None,
                "description": "CNVkit 目标区域的 BED 文件（panel/exome）",
            },
            {
                "name": "antitargets_bed",
                "type": "str",
                "default": None,
                "description": "CNVkit 反目标区域的 BED 文件",
            },
            {
                "name": "gene_bed",
                "type": "str",
                "default": None,
                "description": "用于局灶性事件注释的基因 BED（chrom, start, end, gene）",
            },
            {
                "name": "focal_genes",
                "type": "list[str]",
                "default": None,
                "description": "要突出显示局灶性事件的基因（默认：MYC、ERBB2、CDKN2A）",
            },
            {
                "name": "log2_amp_threshold",
                "type": "float",
                "default": 1.0,
                "description": "局灶性扩增调用的 Log2 比率阈值",
            },
            {
                "name": "log2_del_threshold",
                "type": "float",
                "default": -1.0,
                "description": "局灶性深度缺失调用的 Log2 比率阈值",
            },
        ],
        "required_parameters": [
            {
                "name": "tumor_bam",
                "type": "str",
                "default": None,
                "description": "肿瘤 BAM 的路径（已索引）",
            },
            {
                "name": "reference_genome",
                "type": "str",
                "default": None,
                "description": "参考基因组 FASTA 的路径",
            },
        ],
    },
]
