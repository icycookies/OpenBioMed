description = [
    {
        "description": "优化厌氧消化过程条件以最大化VFA产量或甲烷产量。",
        "name": "optimize_anaerobic_digestion_process",
        "optional_parameters": [
            {
                "default": "methane_yield",
                "description": "要最大化的目标输出，可选'vfa_production'或'methane_yield'",
                "name": "target_output",
                "type": "str",
            },
            {
                "default": "rsm",
                "description": "用于优化的方法，可选'rsm'（响应面法）或'genetic'（遗传算法）",
                "name": "optimization_method",
                "type": "str",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "包含废物特性的字典，如total_solids、volatile_solids和cod",
                "name": "waste_characteristics",
                "type": "dict",
            },
            {
                "default": None,
                "description": "包含操作参数及其范围的字典，包括hrt、olr、if_ratio、temperature和ph",
                "name": "operational_parameters",
                "type": "dict",
            },
        ],
    },
    {
        "description": "使用HPLC-ICP-MS技术分析液体样品中的砷形态。返回总结分析步骤和结果的研究日志。",
        "name": "analyze_arsenic_speciation_hplc_icpms",
        "optional_parameters": [
            {
                "default": "Unknown Sample",
                "description": "正在分析的样品名称",
                "name": "sample_name",
                "type": "str",
            },
            {
                "default": None,
                "description": "包含校准标准数据的字典，包含每种砷形态的已知浓度",
                "name": "calibration_data",
                "type": "dict",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "包含样品数据的字典，键为样品ID，值为字典，其中保留时间（分钟）为键，信号强度为值",
                "name": "sample_data",
                "type": "dict",
            }
        ],
    },
    {
        "description": "使用计算机视觉技术从琼脂平板图像中计数细菌菌落。",
        "name": "count_bacterial_colonies",
        "optional_parameters": [
            {
                "default": 1,
                "description": "平板样品的稀释因子",
                "name": "dilution_factor",
                "type": "float",
            },
            {
                "default": 65.0,
                "description": "琼脂平板的面积（平方厘米）",
                "name": "plate_area_cm2",
                "type": "float",
            },
            {
                "default": "./output",
                "description": "保存输出图像和结果的目录",
                "name": "output_dir",
                "type": "str",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "包含琼脂平板上细菌菌落的图像文件路径",
                "name": "image_path",
                "type": "str",
            }
        ],
    },
    {
        "description": "使用Prokka注释细菌基因组以识别基因、蛋白质和功能特征。",
        "name": "annotate_bacterial_genome",
        "optional_parameters": [
            {
                "default": "annotation_results",
                "description": "保存注释结果的目录",
                "name": "output_dir",
                "type": "str",
            },
            {
                "default": "",
                "description": "生物体的属名",
                "name": "genus",
                "type": "str",
            },
            {
                "default": "",
                "description": "生物体的种名",
                "name": "species",
                "type": "str",
            },
            {
                "default": "",
                "description": "菌株标识符",
                "name": "strain",
                "type": "str",
            },
            {
                "default": "",
                "description": "输出文件的前缀",
                "name": "prefix",
                "type": "str",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "FASTA格式的组装基因组序列文件路径",
                "name": "genome_file_path",
                "type": "str",
            }
        ],
    },
    {
        "description": "使用系列稀释和点样平板法量化细菌浓度（CFU/mL）。",
        "name": "enumerate_bacterial_cfu_by_serial_dilution",
        "optional_parameters": [
            {
                "default": 1.0,
                "description": "初始细菌样品的体积（毫升）",
                "name": "initial_sample_volume_ml",
                "type": "float",
            },
            {
                "default": 100000000.0,
                "description": "初始样品中细菌的估计浓度（CFU/mL）",
                "name": "estimated_concentration",
                "type": "float",
            },
            {
                "default": 10,
                "description": "每次稀释降低浓度的因子",
                "name": "dilution_factor",
                "type": "int",
            },
            {
                "default": 8,
                "description": "要执行的系列稀释次数",
                "name": "num_dilutions",
                "type": "int",
            },
            {
                "default": 3,
                "description": "每个稀释度要平板的重复点样数",
                "name": "spots_per_dilution",
                "type": "int",
            },
            {
                "default": "cfu_enumeration_results.csv",
                "description": "保存CFU计数结果的文件名",
                "name": "output_file",
                "type": "str",
            },
        ],
        "required_parameters": [],
    },
    {
        "description": "使用常微分方程对细菌种群随时间的动态进行建模。",
        "name": "model_bacterial_growth_dynamics",
        "optional_parameters": [
            {
                "default": 24,
                "description": "总模拟时间（小时）",
                "name": "simulation_time",
                "type": "float",
            },
            {
                "default": 0.1,
                "description": "模拟输出的时间步长",
                "name": "time_step",
                "type": "float",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "初始细菌种群大小（CFU/ml或细胞数）",
                "name": "initial_population",
                "type": "float",
            },
            {
                "default": None,
                "description": "细菌生长速率（每小时）",
                "name": "growth_rate",
                "type": "float",
            },
            {
                "default": None,
                "description": "细菌从系统中清除的速率（每小时）",
                "name": "clearance_rate",
                "type": "float",
            },
            {
                "default": None,
                "description": "环境的最大承载能力（CFU/ml或细胞数）",
                "name": "niche_size",
                "type": "float",
            },
        ],
    },
    {
        "description": "使用结晶紫染色测定数据量化生物膜生物量并返回详细的研究日志。",
        "name": "quantify_biofilm_biomass_crystal_violet",
        "optional_parameters": [
            {
                "default": None,
                "description": "与od_values对应的生物膜样品名称",
                "name": "sample_names",
                "type": "List[str]",
            },
            {
                "default": 0,
                "description": "od_values中阴性对照样品的索引",
                "name": "control_index",
                "type": "int",
            },
            {
                "default": None,
                "description": "将结果保存为CSV文件的路径",
                "name": "save_path",
                "type": "str",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "结晶紫染色的光密度测量值，表示样品的吸光度读数",
                "name": "od_values",
                "type": "List[float] or numpy.ndarray",
            }
        ],
    },
    {
        "description": "对荧光显微镜图像执行自动细胞分割并量化形态学指标。",
        "name": "segment_and_analyze_microbial_cells",
        "optional_parameters": [
            {
                "default": "./output",
                "description": "保存输出文件的目录",
                "name": "output_dir",
                "type": "str",
            },
            {
                "default": 50,
                "description": "过滤噪声的最小细胞大小（像素）",
                "name": "min_cell_size",
                "type": "int",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "荧光显微镜图像文件的路径",
                "name": "image_path",
                "type": "str",
            }
        ],
    },
    {
        "description": "使用Cellpose/Omnipose库的预训练模型通过深度学习对荧光显微镜图像执行细胞分割。",
        "name": "segment_cells_with_deep_learning",
        "optional_parameters": [
            {
                "default": "bact_fluor_omni",
                "description": "要使用的预训练模型名称（选项包括：'bact_fluor_omni'、'cyto'、'nuclei'等）",
                "name": "model_type",
                "type": "str",
            },
            {
                "default": None,
                "description": "细胞的预期直径（像素）。如果为None，则自动估计直径",
                "name": "diameter",
                "type": "float",
            },
            {
                "default": "segmentation_results",
                "description": "保存分割结果的目录",
                "name": "save_dir",
                "type": "str",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "荧光显微镜图像文件的路径",
                "name": "image_path",
                "type": "str",
            }
        ],
    },
    {
        "description": "使用广义Lotka-Volterra（gLV）模型模拟微生物群落动态。",
        "name": "simulate_generalized_lotka_volterra_dynamics",
        "optional_parameters": [
            {
                "default": "glv_simulation_results.csv",
                "description": "保存模拟结果的文件名",
                "name": "output_file",
                "type": "str",
            }
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "每个微生物物种的初始丰度（一维数组）",
                "name": "initial_abundances",
                "type": "numpy.ndarray",
            },
            {
                "default": None,
                "description": "每个微生物物种的内在生长速率（一维数组）",
                "name": "growth_rates",
                "type": "numpy.ndarray",
            },
            {
                "default": None,
                "description": "相互作用系数矩阵，其中A[i,j]表示物种j对物种i的影响（二维数组）",
                "name": "interaction_matrix",
                "type": "numpy.ndarray",
            },
            {
                "default": None,
                "description": "评估模型的时间点",
                "name": "time_points",
                "type": "numpy.ndarray",
            },
        ],
    },
    {
        "description": "使用ViennaRNA预测RNA分子的二级结构。",
        "name": "predict_rna_secondary_structure",
        "optional_parameters": [
            {
                "default": "rna_structure",
                "description": "输出文件的前缀",
                "name": "output_prefix",
                "type": "str",
            }
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "RNA序列（由A、U、G、C核苷酸组成）",
                "name": "rna_sequence",
                "type": "str",
            }
        ],
    },
    {
        "description": "使用Gillespie算法执行微生物种群动态的随机模拟。",
        "name": "simulate_microbial_population_dynamics",
        "optional_parameters": [
            {
                "default": 100,
                "description": "最大模拟时间",
                "name": "max_time",
                "type": "float",
            },
            {
                "default": 100,
                "description": "要运行的随机模拟次数",
                "name": "num_simulations",
                "type": "int",
            },
            {
                "default": 100,
                "description": "要记录轨迹的时间点数量",
                "name": "time_points",
                "type": "int",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "每个微生物物种的初始种群大小",
                "name": "initial_populations",
                "type": "List[int]",
            },
            {
                "default": None,
                "description": "每个物种的人均生长速率",
                "name": "growth_rates",
                "type": "List[float]",
            },
            {
                "default": None,
                "description": "每个物种的人均死亡/清除速率",
                "name": "clearance_rates",
                "type": "List[float]",
            },
            {
                "default": None,
                "description": "每个物种的最大可持续种群数量",
                "name": "carrying_capacities",
                "type": "List[float]",
            },
        ],
    },
]
