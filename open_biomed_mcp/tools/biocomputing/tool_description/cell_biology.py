description = [
    {
        "description": "使用 Calcofluor white 染色的显微镜图像量化每个细胞周期阶段的细胞百分比。",
        "name": "quantify_cell_cycle_phases_from_microscopy",
        "optional_parameters": [
            {
                "default": "./results",
                "description": "保存结果的目录",
                "name": "output_dir",
                "type": "str",
            }
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "用 Calcofluor white 染色的细胞显微镜图像文件路径列表",
                "name": "image_paths",
                "type": "List[str]",
            }
        ],
    },
    {
        "description": "从延时显微镜图像量化细胞运动特征，并根据运动模式对细胞进行聚类。",
        "name": "quantify_and_cluster_cell_motility",
        "optional_parameters": [
            {
                "default": "./results",
                "description": "保存输出文件的目录",
                "name": "output_dir",
                "type": "str",
            },
            {
                "default": 3,
                "description": "要识别的运动模式簇数量",
                "name": "num_clusters",
                "type": "int",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "包含按顺序排列的延时显微镜图像的目录路径",
                "name": "image_sequence_path",
                "type": "str",
            }
        ],
    },
    {
        "description": "执行荧光激活细胞分选 (FACS)，根据荧光特性富集细胞群体。",
        "name": "perform_facs_cell_sorting",
        "optional_parameters": [
            {
                "default": None,
                "description": "荧光参数的最小阈值。低于此值的细胞将被排除",
                "name": "threshold_min",
                "type": "float",
            },
            {
                "default": None,
                "description": "荧光参数的最大阈值。高于此值的细胞将被排除",
                "name": "threshold_max",
                "type": "float",
            },
            {
                "default": "sorted_cells.csv",
                "description": "保存分选细胞群体数据的文件名",
                "name": "output_file",
                "type": "str",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "包含流式细胞术数据的 FCS 文件路径",
                "name": "cell_suspension_data",
                "type": "str",
            },
            {
                "default": None,
                "description": "用于分选的荧光参数（例如 'GFP'、'FITC'、'PE'）",
                "name": "fluorescence_parameter",
                "type": "str",
            },
        ],
    },
    {
        "description": "分析流式细胞术数据，根据表面标记物识别和量化特定细胞群体。",
        "name": "analyze_flow_cytometry_immunophenotyping",
        "optional_parameters": [
            {
                "default": None,
                "description": "用于校正荧光重叠的溢出/补偿矩阵",
                "name": "compensation_matrix",
                "type": "numpy.ndarray",
            },
            {
                "default": "./results",
                "description": "保存结果的目录",
                "name": "output_dir",
                "type": "str",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "包含流式细胞术数据的 FCS 文件路径",
                "name": "fcs_file_path",
                "type": "str",
            },
            {
                "default": None,
                "description": "定义门控策略的字典。每个键是群体名称，每个值是元组列表 (marker, operator, threshold)",
                "name": "gating_strategy",
                "type": "dict",
            },
        ],
    },
    {
        "description": "从荧光显微镜图像量化线粒体形态和膜电位的指标。",
        "name": "analyze_mitochondrial_morphology_and_potential",
        "optional_parameters": [
            {
                "default": "./output",
                "description": "保存输出文件的目录",
                "name": "output_dir",
                "type": "str",
            }
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "显示线粒体形态的荧光显微镜图像路径（例如 MTS-GFP）",
                "name": "morphology_image_path",
                "type": "str",
            },
            {
                "default": None,
                "description": "显示线粒体膜电位的荧光显微镜图像路径（例如 TMRE 染色）",
                "name": "potential_image_path",
                "type": "str",
            },
        ],
    },
]
