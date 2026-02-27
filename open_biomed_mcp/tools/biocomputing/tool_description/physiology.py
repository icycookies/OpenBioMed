description = [
    {
        "description": "从头颈部MRI扫描生成面部解剖结构的3D模型",
        "name": "reconstruct_3d_face_from_mri",
        "optional_parameters": [
            {
                "default": "./output",
                "description": "输出文件保存的目录",
                "name": "output_dir",
                "type": "str",
            },
            {
                "default": "subject",
                "description": "受试者标识符，用于输出文件名",
                "name": "subject_id",
                "type": "str",
            },
            {
                "default": 300,
                "description": "面部组织初始分割的阈值",
                "name": "threshold_value",
                "type": "int",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "MRI扫描文件的路径（NIfTI格式：.nii或.nii.gz）",
                "name": "mri_file_path",
                "type": "str",
            }
        ],
    },
    {
        "description": "从听觉脑干反应（ABR）波形数据中提取P1波幅和潜伏期",
        "name": "analyze_abr_waveform_p1_metrics",
        "optional_parameters": [],
        "required_parameters": [
            {
                "default": None,
                "description": "ABR记录的时间点，单位为毫秒",
                "name": "time_ms",
                "type": "array-like",
            },
            {
                "default": None,
                "description": "ABR记录的振幅值，单位为微伏",
                "name": "amplitude_uv",
                "type": "array-like",
            },
        ],
    },
    {
        "description": "使用FFT分析从高速视频显微镜数据中分析纤毛摆动频率",
        "name": "analyze_ciliary_beat_frequency",
        "optional_parameters": [
            {
                "default": 5,
                "description": "要分析的感兴趣区域数量",
                "name": "roi_count",
                "type": "int",
            },
            {
                "default": 0,
                "description": "考虑的最小频率，单位为Hz",
                "name": "min_freq",
                "type": "float",
            },
            {
                "default": 30,
                "description": "考虑的最大频率，单位为Hz",
                "name": "max_freq",
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
                "description": "纤毛摆动的高速视频显微镜文件路径",
                "name": "video_path",
                "type": "str",
            }
        ],
    },
    {
        "description": "分析显微镜图像中两个荧光标记蛋白之间的共定位",
        "name": "analyze_protein_colocalization",
        "optional_parameters": [
            {
                "default": "./output",
                "description": "保存输出文件的目录",
                "name": "output_dir",
                "type": "str",
            },
            {
                "default": "otsu",
                "description": "图像阈值分割方法（'otsu'、'li'或'yen'）",
                "name": "threshold_method",
                "type": "str",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "第一通道图像文件的路径（荧光蛋白1）",
                "name": "channel1_path",
                "type": "str",
            },
            {
                "default": None,
                "description": "第二通道图像文件的路径（荧光蛋白2）",
                "name": "channel2_path",
                "type": "str",
            },
        ],
    },
    {
        "description": "对生理时间序列数据执行余弦分析以表征昼夜节律",
        "name": "perform_cosinor_analysis",
        "optional_parameters": [
            {
                "default": 24.0,
                "description": "节律周期（小时），昼夜节律默认为24小时",
                "name": "period",
                "type": "float",
            }
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "测量的时间点，单位为小时",
                "name": "time_data",
                "type": "array-like",
            },
            {
                "default": None,
                "description": "对应每个时间点的生理测量值",
                "name": "physiological_data",
                "type": "array-like",
            },
        ],
    },
    {
        "description": "使用单指数扩散模型从扩散加权MRI数据计算表观扩散系数（ADC）图",
        "name": "calculate_brain_adc_map",
        "optional_parameters": [
            {
                "default": "adc_map.nii.gz",
                "description": "输出ADC图的保存路径",
                "name": "output_path",
                "type": "str",
            },
            {
                "default": None,
                "description": "二值掩膜文件的路径，用于将ADC计算限制在脑区域",
                "name": "mask_file_path",
                "type": "str",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "包含扩散加权MRI数据的4D NIfTI文件路径",
                "name": "dwi_file_path",
                "type": "str",
            },
            {
                "default": None,
                "description": "对应4D DWI数据中每个体积的b值列表",
                "name": "b_values",
                "type": "List[float]",
            },
        ],
    },
    {
        "description": "使用ELGA/ELGA1探针数据分析内溶酶体区室中的钙动力学",
        "name": "analyze_endolysosomal_calcium_dynamics",
        "optional_parameters": [
            {
                "default": None,
                "description": "施加处理/刺激的时间点（秒）",
                "name": "treatment_time",
                "type": "float",
            },
            {
                "default": "",
                "description": "实验中使用的细胞类型",
                "name": "cell_type",
                "type": "str",
            },
            {
                "default": "",
                "description": "施加的处理或刺激的名称",
                "name": "treatment_name",
                "type": "str",
            },
            {
                "default": "calcium_analysis_results.txt",
                "description": "保存详细分析结果的文件名",
                "name": "output_file",
                "type": "str",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "测量的时间点，单位为秒",
                "name": "time_points",
                "type": "numpy.ndarray or list",
            },
            {
                "default": None,
                "description": "来自ELGA/ELGA1探针的发光强度值，对应Ca2+水平",
                "name": "luminescence_values",
                "type": "numpy.ndarray or list",
            },
        ],
    },
    {
        "description": "使用气相色谱数据分析组织样本中的脂肪酸组成",
        "name": "analyze_fatty_acid_composition_by_gc",
        "optional_parameters": [
            {
                "default": "./results",
                "description": "结果文件保存的目录",
                "name": "output_directory",
                "type": "str",
            }
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "包含气相色谱数据的CSV文件路径，需包含'retention_time'和'peak_area'列",
                "name": "gc_data_file",
                "type": "str",
            },
            {
                "default": None,
                "description": "组织样本类型（例如：liver、kidney、heart、muscle、adipose）",
                "name": "tissue_type",
                "type": "str",
            },
            {
                "default": None,
                "description": "正在分析的样本标识符",
                "name": "sample_id",
                "type": "str",
            },
        ],
    },
    {
        "description": "分析原始血压数据以计算关键血流动力学参数",
        "name": "analyze_hemodynamic_data",
        "optional_parameters": [
            {
                "default": "hemodynamic_results.csv",
                "description": "保存计算参数的文件名",
                "name": "output_file",
                "type": "str",
            }
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "原始血压测量值，单位为mmHg",
                "name": "pressure_data",
                "type": "numpy.ndarray",
            },
            {
                "default": None,
                "description": "数据采集率，单位为Hz（每秒采样数）",
                "name": "sampling_rate",
                "type": "float",
            },
        ],
    },
    {
        "description": "使用基于ODE的药代动力学模型模拟甲状腺激素在不同组织区室间的转运和结合",
        "name": "simulate_thyroid_hormone_pharmacokinetics",
        "optional_parameters": [
            {
                "default": "(0, 24)",
                "description": "模拟的起始和结束时间，单位为小时",
                "name": "time_span",
                "type": "tuple",
            },
            {
                "default": 100,
                "description": "输出的时间点数量",
                "name": "time_points",
                "type": "int",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "包含模型参数的字典，包括transport_rates、binding_constants、metabolism_rates和volumes",
                "name": "parameters",
                "type": "dict",
            },
            {
                "default": None,
                "description": "每个区室中所有分子种类的初始浓度字典",
                "name": "initial_conditions",
                "type": "dict",
            },
        ],
    },
    {
        "description": "分析图像以检测和量化β-淀粉样蛋白斑块，返回详细的分析日志",
        "name": "quantify_amyloid_beta_plaques",
        "optional_parameters": [
            {
                "default": "./results",
                "description": "结果保存的目录",
                "name": "output_dir",
                "type": "str",
            },
            {
                "default": "otsu",
                "description": "图像阈值分割方法（otsu、adaptive或manual）",
                "name": "threshold_method",
                "type": "str",
            },
            {
                "default": 50,
                "description": "区域被视为斑块的最小尺寸，单位为像素²",
                "name": "min_plaque_size",
                "type": "int",
            },
            {
                "default": 127,
                "description": "当threshold_method为manual时使用的阈值",
                "name": "manual_threshold",
                "type": "int",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "要分析β-淀粉样蛋白斑块的图像文件路径",
                "name": "image_path",
                "type": "str",
            }
        ],
    },
]
