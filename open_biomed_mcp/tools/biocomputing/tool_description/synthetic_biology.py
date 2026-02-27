description = [
    {
        "description": "通过整合治疗性遗传元件来改造细菌基因组以实现治疗递送",
        "name": "engineer_bacterial_genome_for_therapeutic_delivery",
        "optional_parameters": [],
        "required_parameters": [
            {
                "default": None,
                "description": "包含FASTA格式细菌基因组序列的文件路径",
                "name": "bacterial_genome_file",
                "type": "str",
            },
            {
                "default": None,
                "description": "包含要整合的遗传元件的字典（启动子、基因、终止子、载体）",
                "name": "genetic_parts",
                "type": "dict",
            },
        ],
    },
    {
        "description": "分析细菌生长数据并从OD600测量值中提取生长参数",
        "name": "analyze_bacterial_growth_rate",
        "optional_parameters": [
            {
                "default": "Unknown strain",
                "description": "正在分析的细菌菌株名称",
                "name": "strain_name",
                "type": "str",
            },
            {
                "default": "./",
                "description": "保存输出文件的目录",
                "name": "output_dir",
                "type": "str",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "进行OD600测量的时间点（小时）",
                "name": "time_points",
                "type": "List or numpy.ndarray",
            },
            {
                "default": None,
                "description": "对应每个时间点的光密度（OD600）测量值",
                "name": "od_measurements",
                "type": "List or numpy.ndarray",
            },
        ],
    },
    {
        "description": "分析测序数据以提取、量化和确定条形码的谱系关系",
        "name": "analyze_barcode_sequencing_data",
        "optional_parameters": [
            {
                "default": None,
                "description": "用于识别条形码的正则表达式模式。如果为None，将使用侧翼序列",
                "name": "barcode_pattern",
                "type": "str",
            },
            {
                "default": None,
                "description": "条形码区域的5'侧翼序列",
                "name": "flanking_seq_5prime",
                "type": "str",
            },
            {
                "default": None,
                "description": "条形码区域的3'侧翼序列",
                "name": "flanking_seq_3prime",
                "type": "str",
            },
            {
                "default": 5,
                "description": "考虑条形码的最小计数阈值",
                "name": "min_count",
                "type": "int",
            },
            {
                "default": "./results",
                "description": "保存输出文件的目录",
                "name": "output_dir",
                "type": "str",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "FASTQ或FASTA格式的输入测序文件路径",
                "name": "input_file",
                "type": "str",
            }
        ],
    },
    {
        "description": "对动力系统执行分岔分析并生成分岔图",
        "name": "analyze_bifurcation_diagram",
        "optional_parameters": [
            {
                "default": "Dynamical System",
                "description": "正在分析的动力系统名称，用于图表标题",
                "name": "system_name",
                "type": "str",
            },
            {
                "default": "./",
                "description": "保存输出文件的目录",
                "name": "output_dir",
                "type": "str",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "二维数组，其中每行表示特定参数值的时间序列。形状应为(n_parameter_values, n_time_points)",
                "name": "time_series_data",
                "type": "numpy.ndarray",
            },
            {
                "default": None,
                "description": "对应每个时间序列的参数值的一维数组。形状应为(n_parameter_values,)",
                "name": "parameter_values",
                "type": "numpy.ndarray",
            },
        ],
    },
    {
        "description": "生成SBML格式的生化网络数学模型",
        "name": "create_biochemical_network_sbml_model",
        "optional_parameters": [
            {
                "default": "biochemical_model.xml",
                "description": "保存SBML模型的文件路径",
                "name": "output_file",
                "type": "str",
            }
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "表示反应的字典列表，包含id、name、reactants、products和reversible属性",
                "name": "reaction_network",
                "type": "List[dict]",
            },
            {
                "default": None,
                "description": "将反应ID映射到动力学定律参数的字典，包含law_type和parameters",
                "name": "kinetic_parameters",
                "type": "dict",
            },
        ],
    },
    {
        "description": "分析和优化DNA/RNA序列以改善在异源宿主生物中的表达",
        "name": "optimize_codons_for_heterologous_expression",
        "optional_parameters": [],
        "required_parameters": [
            {
                "default": None,
                "description": "要优化的目标基因的DNA或RNA序列。应包含完整的密码子（长度可被3整除）",
                "name": "target_sequence",
                "type": "str",
            },
            {
                "default": None,
                "description": "将密码子映射到其在宿主生物中使用频率的字典。格式：{'AUG': 0.8, 'GCC': 0.6, ...}或{'ATG': 0.8, 'GCC': 0.6, ...}",
                "name": "host_codon_usage",
                "type": "dict",
            },
        ],
    },
    {
        "description": "模拟具有生长反馈的基因调控回路动力学",
        "name": "simulate_gene_circuit_with_growth_feedback",
        "optional_parameters": [
            {
                "default": 100,
                "description": "总模拟时间",
                "name": "simulation_time",
                "type": "float",
            },
            {
                "default": 1000,
                "description": "要采样的时间点数量",
                "name": "time_points",
                "type": "int",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "表示基因回路拓扑的邻接矩阵。正值表示激活，负值表示抑制。形状应为(n_genes, n_genes)，其中n_genes是回路中的基因数量",
                "name": "circuit_topology",
                "type": "numpy.ndarray",
            },
            {
                "default": None,
                "description": "包含动力学参数的字典：基因回路的'basal_rates'、'degradation_rates'、'hill_coefficients'和'threshold_constants'",
                "name": "kinetic_params",
                "type": "dict",
            },
            {
                "default": None,
                "description": "包含生长相关参数的字典：'max_growth_rate'、'growth_inhibition'和'gene_growth_weights'",
                "name": "growth_params",
                "type": "dict",
            },
        ],
    },
    {
        "description": "识别脂肪酸合酶（FAS）序列中的功能域并预测其作用",
        "name": "identify_fas_functional_domains",
        "optional_parameters": [
            {
                "default": "protein",
                "description": '提供的序列类型 - "protein"或"nucleotide"',
                "name": "sequence_type",
                "type": "str",
            },
            {
                "default": "fas_domains_report.txt",
                "description": "保存详细域报告的输出文件名",
                "name": "output_file",
                "type": "str",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "FAS基因的核苷酸或蛋白质序列",
                "name": "sequence",
                "type": "str",
            }
        ],
    },
]
