description = [
    {
        "description": "在 hg19 和 hg38 格式之间执行基因组坐标的转换，并提供详细的中间步骤。",
        "name": "liftover_coordinates",
        "optional_parameters": [],
        "required_parameters": [
            {
                "default": None,
                "description": "染色体编号（例如 '1'、'X'）",
                "name": "chromosome",
                "type": "str",
            },
            {
                "default": None,
                "description": "基因组位置",
                "name": "position",
                "type": "int",
            },
            {
                "default": None,
                "description": "输入基因组构建版本（'hg19' 或 'hg38'）",
                "name": "input_format",
                "type": "str",
            },
            {
                "default": None,
                "description": "输出基因组构建版本（'hg19' 或 'hg38'）",
                "name": "output_format",
                "type": "str",
            },
            {
                "default": None,
                "description": "liftover chain 文件的路径",
                "name": "data_path",
                "type": "str",
            },
        ],
    },
    {
        "description": "使用深度变分推断从 GWAS 汇总统计数据执行贝叶斯精细定位，计算假定因果变异的后验包含概率和可信集。",
        "name": "bayesian_finemapping_with_deep_vi",
        "optional_parameters": [
            {
                "default": 5000,
                "description": "变分推断算法的训练迭代次数",
                "name": "n_iterations",
                "type": "int",
            },
            {
                "default": 0.01,
                "description": "优化算法的学习率",
                "name": "learning_rate",
                "type": "float",
            },
            {
                "default": 64,
                "description": "神经网络的隐藏维度大小",
                "name": "hidden_dim",
                "type": "int",
            },
            {
                "default": 0.95,
                "description": "定义可信集的阈值（例如 0.95 表示 95% 可信集）",
                "name": "credible_threshold",
                "type": "float",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "包含 GWAS 汇总统计数据的 CSV 或 TSV 文件路径，包含 variant_id、effect_size、pvalue 和可选的 se 列",
                "name": "gwas_summary_path",
                "type": "str",
            },
            {
                "default": None,
                "description": "连锁不平衡矩阵，包含变异之间的成对相关性",
                "name": "ld_matrix",
                "type": "numpy.ndarray",
            },
        ],
    },
    {
        "description": "分析并分类 Cas9 在靶位点诱导的突变。",
        "name": "analyze_cas9_mutation_outcomes",
        "optional_parameters": [
            {
                "default": None,
                "description": "将序列 ID 映射到细胞系信息的字典（例如野生型、敲除基因）",
                "name": "cell_line_info",
                "type": "dict",
            },
            {
                "default": "cas9_mutation_analysis",
                "description": "输出文件的前缀",
                "name": "output_prefix",
                "type": "str",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "将序列 ID 映射到参考 DNA 序列（字符串）的字典",
                "name": "reference_sequences",
                "type": "dict",
            },
            {
                "default": None,
                "description": "嵌套字典：{sequence_id: {read_id: sequence}}，包含每个参考的编辑/突变序列",
                "name": "edited_sequences",
                "type": "dict",
            },
        ],
    },
    {
        "description": "通过比较原始序列和编辑序列来分析 CRISPR-Cas9 基因组编辑结果。",
        "name": "analyze_crispr_genome_editing",
        "optional_parameters": [
            {
                "default": None,
                "description": "同源定向修复模板序列（如果使用）",
                "name": "repair_template",
                "type": "str",
            }
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "CRISPR-Cas9 编辑前的原始 DNA 序列",
                "name": "original_sequence",
                "type": "str",
            },
            {
                "default": None,
                "description": "CRISPR-Cas9 编辑后的 DNA 序列",
                "name": "edited_sequence",
                "type": "str",
            },
            {
                "default": None,
                "description": "用于靶向的 CRISPR 向导 RNA (crRNA) 序列",
                "name": "guide_rna",
                "type": "str",
            },
        ],
    },
    {
        "description": "使用 msprime 模拟具有指定人口统计和溯祖历史的 DNA 序列。",
        "name": "simulate_demographic_history",
        "optional_parameters": [
            {
                "default": 10,
                "description": "要模拟的样本序列数量",
                "name": "num_samples",
                "type": "int",
            },
            {
                "default": 100000,
                "description": "模拟序列的长度（单位：碱基对）",
                "name": "sequence_length",
                "type": "int",
            },
            {
                "default": 1e-08,
                "description": "每碱基重组率",
                "name": "recombination_rate",
                "type": "float",
            },
            {
                "default": 1e-08,
                "description": "每碱基突变率",
                "name": "mutation_rate",
                "type": "float",
            },
            {
                "default": "constant",
                "description": "要模拟的人口统计模型类型（constant、bottleneck、expansion、contraction、sawtooth）",
                "name": "demographic_model",
                "type": "str",
            },
            {
                "default": None,
                "description": "所选人口统计模型的特定参数",
                "name": "demographic_params",
                "type": "dict",
            },
            {
                "default": "kingman",
                "description": "要使用的溯祖模型类型（kingman、beta）",
                "name": "coalescent_model",
                "type": "str",
            },
            {
                "default": None,
                "description": "beta 溯祖模型的参数",
                "name": "beta_coalescent_param",
                "type": "float",
            },
            {
                "default": None,
                "description": "随机数生成器的种子",
                "name": "random_seed",
                "type": "int",
            },
            {
                "default": "simulated_sequences.vcf",
                "description": "以 VCF 格式保存模拟序列的文件名",
                "name": "output_file",
                "type": "str",
            },
        ],
        "required_parameters": [],
    },
    {
        "description": "识别基因组序列中特定转录因子的结合位点。",
        "name": "identify_transcription_factor_binding_sites",
        "optional_parameters": [
            {
                "default": 0.8,
                "description": "报告结合位点的最小评分阈值（0.0-1.0）",
                "name": "threshold",
                "type": "float",
            },
            {
                "default": None,
                "description": "保存结果的路径",
                "name": "output_file",
                "type": "str",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "要分析的基因组 DNA 序列",
                "name": "sequence",
                "type": "str",
            },
            {
                "default": None,
                "description": "要搜索的转录因子名称（例如 'Hsf1'、'GATA1'）",
                "name": "tf_name",
                "type": "str",
            },
        ],
    },
    {
        "description": "使用基因型和表型数据拟合用于基因组预测的线性混合模型。",
        "name": "fit_genomic_prediction_model",
        "optional_parameters": [
            {
                "default": None,
                "description": "固定效应矩阵（例如环境、管理），个体为行，效应为列。",
                "name": "fixed_effects",
                "type": "numpy.ndarray",
            },
            {
                "default": "additive",
                "description": '要拟合的遗传模型类型："additive" 或 "additive_dominance"。',
                "name": "model_type",
                "type": "str",
            },
            {
                "default": "genomic_prediction_results.csv",
                "description": "保存结果的文件名。",
                "name": "output_file",
                "type": "str",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "基因型数据矩阵，个体为行，标记为列。对于加性模型，值通常编码为 0、1、2，或对于显性效应使用特定编码。",
                "name": "genotypes",
                "type": "numpy.ndarray",
            },
            {
                "default": None,
                "description": "表型数据向量或矩阵，个体为行，性状为列。",
                "name": "phenotypes",
                "type": "numpy.ndarray",
            },
        ],
    },
    {
        "description": "执行目标转基因的 PCR 扩增，并使用琼脂糖凝胶电泳可视化结果。",
        "name": "perform_pcr_and_gel_electrophoresis",
        "optional_parameters": [
            {
                "default": None,
                "description": "正向引物序列。如果未提供，将根据 target_region 设计",
                "name": "forward_primer",
                "type": "str",
            },
            {
                "default": None,
                "description": "反向引物序列。如果未提供，将根据 target_region 设计",
                "name": "reverse_primer",
                "type": "str",
            },
            {
                "default": None,
                "description": "基因组 DNA 中目标区域的 (start, end) 位置元组",
                "name": "target_region",
                "type": "tuple",
            },
            {
                "default": 58,
                "description": "PCR 退火温度（单位：°C）",
                "name": "annealing_temp",
                "type": "float",
            },
            {
                "default": 30,
                "description": "延伸时间（单位：秒）",
                "name": "extension_time",
                "type": "int",
            },
            {
                "default": 35,
                "description": "PCR 循环次数",
                "name": "cycles",
                "type": "int",
            },
            {
                "default": 2.0,
                "description": "琼脂糖凝胶的百分比",
                "name": "gel_percentage",
                "type": "float",
            },
            {
                "default": "pcr_result",
                "description": "输出文件的前缀",
                "name": "output_prefix",
                "type": "str",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "包含 FASTA 格式基因组 DNA 序列的文件路径或序列本身",
                "name": "genomic_dna",
                "type": "str",
            }
        ],
    },
    {
        "description": "对一组蛋白质序列执行系统发育分析。此函数比对序列、构建系统发育树并可视化进化关系。",
        "name": "analyze_protein_phylogeny",
        "optional_parameters": [
            {
                "default": "./",
                "description": "保存输出文件的目录",
                "name": "output_dir",
                "type": "str",
            },
            {
                "default": "clustalw",
                "description": '序列比对方法："clustalw"、"muscle" 或 "pre-aligned"',
                "name": "alignment_method",
                "type": "str",
            },
            {
                "default": "fasttree",
                "description": '树构建方法："iqtree" 或回退到邻接法',
                "name": "tree_method",
                "type": "str",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "包含蛋白质序列的 FASTA 文件路径或 FASTA 格式的序列字符串",
                "name": "fasta_sequences",
                "type": "str",
            }
        ],
    },
]
