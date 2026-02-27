description = [
    {
        "description": "使用MACS2执行ATAC-seq峰值检测和差异可及性分析。",
        "name": "analyze_atac_seq_differential_accessibility",
        "optional_parameters": [
            {
                "default": "./atac_results",
                "description": "保存输出文件的目录",
                "name": "output_dir",
                "type": "str",
            },
            {
                "default": "hs",
                "description": "MACS2的基因组大小参数",
                "name": "genome_size",
                "type": "str",
            },
            {
                "default": 0.05,
                "description": "峰值检测的q值截断值",
                "name": "q_value",
                "type": "float",
            },
            {
                "default": "atac",
                "description": "输出文件名的前缀",
                "name": "name_prefix",
                "type": "str",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "包含比对ATAC-seq读段的处理条件BAM文件路径",
                "name": "treatment_bam",
                "type": "str",
            },
            {
                "default": None,
                "description": "包含比对ATAC-seq读段的对照条件BAM文件路径",
                "name": "control_bam",
                "type": "str",
            },
        ],
    },
    {
        "description": "分析细菌生长曲线数据以确定生长参数，如倍增时间、生长速率和延滞期。",
        "name": "analyze_bacterial_growth_curve",
        "optional_parameters": [
            {
                "default": ".",
                "description": "保存输出文件的目录",
                "name": "output_dir",
                "type": "str",
            }
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "测量的时间点（小时）",
                "name": "time_points",
                "type": "List or numpy.ndarray",
            },
            {
                "default": None,
                "description": "对应每个时间点的光密度测量值",
                "name": "od_values",
                "type": "List or numpy.ndarray",
            },
            {
                "default": None,
                "description": "正在分析的细菌菌株名称",
                "name": "strain_name",
                "type": "str",
            },
        ],
    },
    {
        "description": "模拟从组织样本中分离和纯化免疫细胞的过程。",
        "name": "isolate_purify_immune_cells",
        "optional_parameters": [
            {
                "default": "collagenase",
                "description": "用于组织消化的酶",
                "name": "enzyme_type",
                "type": "str",
            },
            {
                "default": None,
                "description": "用于磁性辅助细胞分选的特异性抗体",
                "name": "macs_antibody",
                "type": "str",
            },
            {
                "default": 45,
                "description": "消化时间（分钟）",
                "name": "digestion_time_min",
                "type": "int",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "组织样本类型（例如：'adipose'、'kidney'、'liver'、'lung'、'spleen'）",
                "name": "tissue_type",
                "type": "str",
            },
            {
                "default": None,
                "description": "要分离的免疫细胞群（例如：'macrophages'、'leukocytes'、'T cells'）",
                "name": "target_cell_type",
                "type": "str",
            },
        ],
    },
    {
        "description": "使用双核苷脉冲标记数据和数学建模估算细胞周期各阶段的持续时间。",
        "name": "estimate_cell_cycle_phase_durations",
        "optional_parameters": [],
        "required_parameters": [
            {
                "default": None,
                "description": "包含EdU和BrdU标记流式细胞术实验数据的字典，包括时间点和标记细胞的百分比",
                "name": "flow_cytometry_data",
                "type": "dict",
            },
            {
                "default": None,
                "description": "细胞周期各阶段持续时间和死亡率的初始估计值",
                "name": "initial_estimates",
                "type": "dict",
            },
        ],
    },
    {
        "description": "在流动条件下追踪免疫细胞并对其行为进行分类。",
        "name": "track_immune_cells_under_flow",
        "optional_parameters": [
            {
                "default": "./output",
                "description": "保存输出文件的目录",
                "name": "output_dir",
                "type": "str",
            },
            {
                "default": 1.0,
                "description": "像素大小（微米）",
                "name": "pixel_size_um",
                "type": "float",
            },
            {
                "default": 1.0,
                "description": "帧间时间间隔（秒）",
                "name": "time_interval_sec",
                "type": "float",
            },
            {
                "default": "right",
                "description": "流动方向（'right'、'left'、'up'、'down'）",
                "name": "flow_direction",
                "type": "str",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "图像序列目录或视频文件的路径",
                "name": "image_sequence_path",
                "type": "str",
            }
        ],
    },
    {
        "description": "分析CFSE标记的细胞样本以量化细胞分裂和增殖。",
        "name": "analyze_cfse_cell_proliferation",
        "optional_parameters": [
            {
                "default": "FL1-A",
                "description": "包含CFSE荧光数据的通道名称",
                "name": "cfse_channel",
                "type": "str",
            },
            {
                "default": None,
                "description": "用于淋巴细胞门控的元组（min_fsc, max_fsc, min_ssc, max_ssc）",
                "name": "lymphocyte_gate",
                "type": "tuple or None",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "包含CFSE标记细胞流式细胞术数据的FCS文件路径",
                "name": "fcs_file_path",
                "type": "str",
            }
        ],
    },
    {
        "description": "分析抗原刺激后CD4+ T细胞中的细胞因子产生（IFN-γ、IL-17）。",
        "name": "analyze_cytokine_production_in_cd4_tcells",
        "optional_parameters": [
            {
                "default": "./results",
                "description": "保存结果文件的目录",
                "name": "output_dir",
                "type": "str",
            }
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "将刺激条件映射到FCS文件路径的字典。预期键：'unstimulated'、'Mtb300'、'CMV'、'SEB'",
                "name": "fcs_files_dict",
                "type": "dict",
            }
        ],
    },
    {
        "description": "分析ELISA数据以量化血浆/血清样本中的EBV抗体滴度。",
        "name": "analyze_ebv_antibody_titers",
        "optional_parameters": [
            {
                "default": "./",
                "description": "保存输出文件的目录。",
                "name": "output_dir",
                "type": "str",
            }
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "包含每个样本光密度（OD）读数的字典。格式：{sample_id: {'VCA_IgG': float, 'VCA_IgM': float, 'EA_IgG': float, 'EA_IgM': float, 'EBNA1_IgG': float, 'EBNA1_IgM': float}}",
                "name": "raw_od_data",
                "type": "dict",
            },
            {
                "default": None,
                "description": "包含每种抗体类型标准曲线数据的字典。格式：{antibody_type: [(concentration, OD), ...]}",
                "name": "standard_curve_data",
                "type": "dict",
            },
            {
                "default": None,
                "description": "包含每个样本元数据的字典。格式：{sample_id: {'group': str, 'collection_date': str}}",
                "name": "sample_metadata",
                "type": "dict",
            },
        ],
    },
    {
        "description": "分析CNS病变的组织学图像以量化免疫细胞浸润、脱髓鞘和组织损伤。",
        "name": "analyze_cns_lesion_histology",
        "optional_parameters": [
            {
                "default": "./output",
                "description": "保存输出文件的目录",
                "name": "output_dir",
                "type": "str",
            },
            {
                "default": "H&E",
                "description": "使用的组织学染色类型（选项：'H&E'、'LFB'、'IHC'）",
                "name": "stain_type",
                "type": "str",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "脑或脊髓组织切片显微镜图像文件的路径",
                "name": "image_path",
                "type": "str",
            }
        ],
    },
    {
        "description": "分析免疫组织化学图像以量化蛋白质表达和空间分布。",
        "name": "analyze_immunohistochemistry_image",
        "optional_parameters": [
            {
                "default": "Unknown",
                "description": "正在分析的蛋白质名称",
                "name": "protein_name",
                "type": "str",
            },
            {
                "default": "./ihc_results/",
                "description": "保存输出文件的目录",
                "name": "output_dir",
                "type": "str",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "用抗体染色的组织切片显微镜图像的路径",
                "name": "image_path",
                "type": "str",
            }
        ],
    },
]
