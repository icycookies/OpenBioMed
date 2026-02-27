description = [
    {
        "description": "从延时显微镜图像分析细胞迁移指标。",
        "name": "analyze_cell_migration_metrics",
        "optional_parameters": [
            {
                "default": 1.0,
                "description": "从像素到微米的转换因子",
                "name": "pixel_size_um",
                "type": "float",
            },
            {
                "default": 1.0,
                "description": "连续帧之间的时间间隔（单位：分钟）",
                "name": "time_interval_min",
                "type": "float",
            },
            {
                "default": 10,
                "description": "细胞必须被追踪的最小帧数才能纳入分析",
                "name": "min_track_length",
                "type": "int",
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
                "description": "包含延时图像的目录路径或多帧 TIFF 文件的路径",
                "name": "image_sequence_path",
                "type": "str",
            }
        ],
    },
    {
        "description": "模拟 CRISPR-Cas9 基因组编辑过程，包括向导 RNA 设计、递送和分析。",
        "name": "perform_crispr_cas9_genome_editing",
        "optional_parameters": [],
        "required_parameters": [
            {
                "default": None,
                "description": "靶向感兴趣基因组区域的向导 RNA 序列列表（每个 20 个核苷酸）",
                "name": "guide_rna_sequences",
                "type": "List[str]",
            },
            {
                "default": None,
                "description": "要编辑的目标基因组序列（应长于向导 RNA 并包含目标位点）",
                "name": "target_genomic_loci",
                "type": "str",
            },
            {
                "default": None,
                "description": "正在编辑的细胞或组织类型（影响递送效率和编辑结果）",
                "name": "cell_tissue_type",
                "type": "str",
            },
        ],
    },
    {
        "description": "分析钙成像数据以量化神经元活动指标，包括细胞计数、事件率、衰减时间和信噪比。",
        "name": "analyze_calcium_imaging_data",
        "optional_parameters": [
            {
                "default": "./",
                "description": "保存输出文件的目录",
                "name": "output_dir",
                "type": "str",
            }
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "荧光显微镜图像的时间序列堆栈路径（TIFF 格式）",
                "name": "image_stack_path",
                "type": "str",
            }
        ],
    },
    {
        "description": "分析生物材料制剂的体外药物释放动力学。",
        "name": "analyze_in_vitro_drug_release_kinetics",
        "optional_parameters": [
            {
                "default": "Drug",
                "description": "正在分析的药物名称",
                "name": "drug_name",
                "type": "str",
            },
            {
                "default": None,
                "description": "制剂中最初装载的药物总量。如果为 None，则使用最大浓度作为 100%",
                "name": "total_drug_loaded",
                "type": "float",
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
                "description": "测量药物浓度的时间点（单位：小时）",
                "name": "time_points",
                "type": "List[float] or numpy.ndarray",
            },
            {
                "default": None,
                "description": "每个时间点测量的药物浓度",
                "name": "concentration_data",
                "type": "List[float] or numpy.ndarray",
            },
        ],
    },
    {
        "description": "量化组织切片显微镜图像中肌纤维的形态学特性。",
        "name": "analyze_myofiber_morphology",
        "optional_parameters": [
            {
                "default": 2,
                "description": "包含细胞核染色（DAPI、Hoechst 等）的通道索引",
                "name": "nuclei_channel",
                "type": "int",
            },
            {
                "default": 1,
                "description": "包含肌纤维染色（α-Actinin 等）的通道索引",
                "name": "myofiber_channel",
                "type": "int",
            },
            {
                "default": "otsu",
                "description": "阈值处理方法（'otsu'、'adaptive' 或 'manual'）",
                "name": "threshold_method",
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
                "description": "显微镜图像文件的路径（通常是包含细胞核和肌纤维染色的多通道图像）",
                "name": "image_path",
                "type": "str",
            }
        ],
    },
    {
        "description": "建模神经活动轨迹并解码行为变量。",
        "name": "decode_behavior_from_neural_trajectories",
        "optional_parameters": [
            {
                "default": 10,
                "description": "用于降维的主成分数量",
                "name": "n_components",
                "type": "int",
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
                "description": "神经元放电活动数据，形状为 (n_timepoints, n_neurons)",
                "name": "neural_data",
                "type": "numpy.ndarray",
            },
            {
                "default": None,
                "description": "行为数据，形状为 (n_timepoints, n_behavioral_variables)",
                "name": "behavioral_data",
                "type": "numpy.ndarray",
            },
        ],
    },
    {
        "description": "模拟表示为常微分方程 (ODE) 系统的全细胞模型。",
        "name": "simulate_whole_cell_ode_model",
        "optional_parameters": [
            {
                "default": None,
                "description": "定义 ODE 系统的函数。应接受参数 (t, y, *args)，其中 t 是时间，y 是状态向量，args 包含附加参数。如果为 None，将使用一个简单的示例全细胞模型。",
                "name": "ode_function",
                "type": "callable",
            },
            {
                "default": "(0, 100)",
                "description": "模拟的 (start_time, end_time) 元组。",
                "name": "time_span",
                "type": "tuple",
            },
            {
                "default": 1000,
                "description": "要评估的时间点数量。",
                "name": "time_points",
                "type": "int",
            },
            {
                "default": "'LSODA'",
                "description": "要使用的数值积分方法（例如 'RK45'、'LSODA'、'BDF'）。",
                "name": "method",
                "type": "str",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "模型中每个状态变量的初始值。如果是字典，键为变量名称，值为初始浓度/值。如果是类数组，顺序必须与 ODE 函数期望的顺序匹配。",
                "name": "initial_conditions",
                "type": "dict or array-like",
            },
            {
                "default": None,
                "description": "ODE 函数所需的模型参数。键为参数名称，值为参数值。",
                "name": "parameters",
                "type": "dict",
            },
        ],
    },
]
