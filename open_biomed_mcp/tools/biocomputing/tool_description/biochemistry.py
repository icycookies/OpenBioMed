description = [
    {
        "description": "分析圆二色谱 (CD) 光谱数据以确定二级结构和热稳定性。",
        "name": "analyze_circular_dichroism_spectra",
        "optional_parameters": [
            {
                "default": None,
                "description": "热变性实验的温度值（°C）",
                "name": "temperature_data",
                "type": "list or numpy.ndarray",
            },
            {
                "default": None,
                "description": "不同温度下特定波长的 CD 信号值",
                "name": "thermal_cd_data",
                "type": "list or numpy.ndarray",
            },
            {
                "default": "./",
                "description": "保存结果文件的目录",
                "name": "output_dir",
                "type": "str",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": '生物分子样品的名称（例如 "Znf706"、"G-quadruplex"）',
                "name": "sample_name",
                "type": "str",
            },
            {
                "default": None,
                "description": '生物分子的类型（"protein" 或 "nucleic_acid"）',
                "name": "sample_type",
                "type": "str",
            },
            {
                "default": None,
                "description": "CD 光谱的波长值（单位：nm）",
                "name": "wavelength_data",
                "type": "list or numpy.ndarray",
            },
            {
                "default": None,
                "description": "CD 信号强度值（通常以 mdeg 或 Δε 为单位）",
                "name": "cd_signal_data",
                "type": "list or numpy.ndarray",
            },
        ],
    },
    {
        "description": "计算 RNA 二级结构各种结构特征的数值。",
        "name": "analyze_rna_secondary_structure_features",
        "optional_parameters": [
            {
                "default": None,
                "description": "与结构对应的 RNA 序列。如果提供，将执行序列依赖的能量计算。",
                "name": "sequence",
                "type": "str",
            }
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "点括号表示法的 RNA 二级结构（例如 \"(((...)))\")。括号表示碱基配对，点表示未配对的碱基。",
                "name": "dot_bracket_structure",
                "type": "str",
            }
        ],
    },
    {
        "description": "分析来自荧光肽切割测定的蛋白酶动力学数据，将数据拟合到 Michaelis-Menten 动力学，并确定关键动力学参数。",
        "name": "analyze_protease_kinetics",
        "optional_parameters": [
            {
                "default": "protease_kinetics",
                "description": "输出文件的前缀",
                "name": "output_prefix",
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
                "description": "进行测量的时间点数组（单位：秒）",
                "name": "time_points",
                "type": "numpy.ndarray",
            },
            {
                "default": None,
                "description": "荧光测量的二维数组，其中每行对应不同的底物浓度，每列对应一个时间点",
                "name": "fluorescence_data",
                "type": "numpy.ndarray",
            },
            {
                "default": None,
                "description": "与 fluorescence_data 中每行对应的底物浓度数组（单位：μM）",
                "name": "substrate_concentrations",
                "type": "numpy.ndarray",
            },
            {
                "default": None,
                "description": "蛋白酶的浓度（单位：μM）",
                "name": "enzyme_concentration",
                "type": "float",
            },
        ],
    },
    {
        "description": "执行体外酶动力学测定并分析调节剂的剂量依赖性效应。",
        "name": "analyze_enzyme_kinetics_assay",
        "optional_parameters": [
            {
                "default": None,
                "description": "调节剂字典，其中键为调节剂名称，值为浓度列表（单位：μM）",
                "name": "modulators",
                "type": "dict",
            },
            {
                "default": None,
                "description": "时间进程测量的时间点（单位：分钟）",
                "name": "time_points",
                "type": "list or numpy.ndarray",
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
                "description": "正在测试的纯化酶的名称",
                "name": "enzyme_name",
                "type": "str",
            },
            {
                "default": None,
                "description": "用于动力学分析的底物浓度列表（单位：μM）",
                "name": "substrate_concentrations",
                "type": "list or numpy.ndarray",
            },
            {
                "default": None,
                "description": "酶的浓度（单位：nM）",
                "name": "enzyme_concentration",
                "type": "float",
            },
        ],
    },
    {
        "description": "分析等温滴定量热法 (ITC) 数据以确定结合亲和力和热力学参数。",
        "name": "analyze_itc_binding_thermodynamics",
        "optional_parameters": [
            {
                "default": None,
                "description": "包含 ITC 热谱图数据的 CSV 或 TSV 文件路径，包含注射次数、注射体积和释放/吸收热量的列。",
                "name": "itc_data_path",
                "type": "str",
            },
            {
                "default": None,
                "description": "原始 ITC 热谱图数据，作为形状为 (n_injections, 3) 的 numpy 数组，包含注射次数、注射体积和热量。",
                "name": "itc_data",
                "type": "numpy.ndarray",
            },
            {
                "default": 298.15,
                "description": "进行实验的温度（单位：开尔文）。",
                "name": "temperature",
                "type": "float",
            },
            {
                "default": None,
                "description": "样品池中蛋白质的初始浓度（单位：摩尔 M）。",
                "name": "protein_concentration",
                "type": "float",
            },
            {
                "default": None,
                "description": "注射器中配体的浓度（单位：摩尔 M）。",
                "name": "ligand_concentration",
                "type": "float",
            },
        ],
        "required_parameters": [],
    },
    {
        "description": "执行多序列比对和系统发育分析以识别保守的蛋白质区域。",
        "name": "analyze_protein_conservation",
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
                "description": "来自多个生物体的 FASTA 格式蛋白质序列列表。",
                "name": "protein_sequences",
                "type": "list of str",
            }
        ],
    },
]
