description = [
    {
        "description": "使用蛋白质PDB文件和配体的SMILES字符串运行DiffDock分子对接，在Docker容器中执行该过程。",
        "name": "run_diffdock_with_smiles",
        "optional_parameters": [
            {
                "default": 0,
                "description": "用于计算的GPU设备ID",
                "name": "gpu_device",
                "type": "int",
            },
            {
                "default": True,
                "description": "是否使用GPU加速进行对接",
                "name": "use_gpu",
                "type": "bool",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "用于对接的蛋白质PDB文件路径",
                "name": "pdb_path",
                "type": "str",
            },
            {
                "default": None,
                "description": "配体分子的SMILES字符串表示",
                "name": "smiles_string",
                "type": "str",
            },
            {
                "default": None,
                "description": "保存对接结果的本地目录路径",
                "name": "local_output_dir",
                "type": "str",
            },
        ],
    },
    {
        "description": "使用AutoDock Vina执行分子对接以预测小分子与受体蛋白之间的结合亲和力。",
        "name": "docking_autodock_vina",
        "optional_parameters": [
            {
                "default": 1,
                "description": "用于对接的CPU核心数",
                "name": "ncpu",
                "type": "int",
            }
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "表示要对接的小分子的SMILES字符串列表",
                "name": "smiles_list",
                "type": "List[str]",
            },
            {
                "default": None,
                "description": "受体蛋白结构PDB文件的路径",
                "name": "receptor_pdb_file",
                "type": "str",
            },
            {
                "default": None,
                "description": "对接盒中心的3D坐标[x, y, z]",
                "name": "box_center",
                "type": "List[float]",
            },
            {
                "default": None,
                "description": "对接盒的尺寸[x, y, z]",
                "name": "box_size",
                "type": "List[float]",
            },
        ],
    },
    {
        "description": "在PDB文件上运行AutoSite以识别潜在的结合位点并返回包含结果的研究日志。",
        "name": "run_autosite",
        "optional_parameters": [
            {
                "default": 1.0,
                "description": "AutoSite计算的网格间距参数",
                "name": "spacing",
                "type": "float",
            }
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "输入PDB文件的路径",
                "name": "pdb_file",
                "type": "str",
            },
            {
                "default": None,
                "description": "保存AutoSite结果的目录",
                "name": "output_dir",
                "type": "str",
            },
        ],
    },
    {
        "description": "计算TxGNN模型对药物重定位的预测，并返回给定疾病的得分最高的预测药物。",
        "name": "retrieve_topk_repurposing_drugs_from_disease_txgnn",
        "optional_parameters": [
            {
                "default": 5,
                "description": "要返回的顶级药物预测数量",
                "name": "k",
                "type": "int",
            }
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "要检索药物预测的疾病名称",
                "name": "disease_name",
                "type": "str",
            },
            {
                "default": None,
                "description": "数据湖的路径",
                "name": "data_lake_path",
                "type": "str",
            },
        ],
    },
    {
        "description": "使用预训练模型预测化合物列表的ADMET（吸收、分布、代谢、排泄、毒性）属性。",
        "name": "predict_admet_properties",
        "optional_parameters": [
            {
                "default": "MPNN",
                "description": "用于ADMET预测的模型类型（选项：'MPNN'、'CNN'、'Morgan'）",
                "name": "ADMET_model_type",
                "type": "str",
            }
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "表示要分析的化合物的SMILES字符串列表",
                "name": "smiles_list",
                "type": "List[str]",
            }
        ],
    },
    {
        "description": "使用预训练的深度学习模型预测小分子与蛋白质序列之间的结合亲和力。",
        "name": "predict_binding_affinity_protein_1d_sequence",
        "optional_parameters": [
            {
                "default": "MPNN-CNN",
                "description": "用于结合亲和力预测的深度学习模型架构（选项：CNN-CNN、MPNN-CNN、Morgan-CNN、Morgan-AAC、Daylight-AAC）",
                "name": "affinity_model_type",
                "type": "str",
            }
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "表示化合物的SMILES字符串列表",
                "name": "smiles_list",
                "type": "List[str]",
            },
            {
                "default": None,
                "description": "氨基酸格式的蛋白质序列",
                "name": "amino_acid_sequence",
                "type": "str",
            },
        ],
    },
    {
        "description": "分析加速储存条件下药物制剂的稳定性。",
        "name": "analyze_accelerated_stability_of_pharmaceutical_formulations",
        "optional_parameters": [],
        "required_parameters": [
            {
                "default": None,
                "description": "制剂字典列表，包含名称、活性成分、浓度和辅料",
                "name": "formulations",
                "type": "List[dict]",
            },
            {
                "default": None,
                "description": "储存条件字典列表，包含温度、湿度（可选）和描述",
                "name": "storage_conditions",
                "type": "List[dict]",
            },
            {
                "default": None,
                "description": "评估稳定性的时间点列表（天）",
                "name": "time_points",
                "type": "List[int]",
            },
        ],
    },
    {
        "description": "生成执行3D软骨聚集培养测定的详细方案，以评估化合物对软骨形成的影响。",
        "name": "run_3d_chondrogenic_aggregate_assay",
        "optional_parameters": [
            {
                "default": 21,
                "description": "培养期的总持续时间（天）",
                "name": "culture_duration_days",
                "type": "int",
            },
            {
                "default": 7,
                "description": "测量之间的间隔（天）",
                "name": "measurement_intervals",
                "type": "int",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "包含细胞信息的字典，包括'source'、'passage_number'和'cell_density'",
                "name": "chondrocyte_cells",
                "type": "dict",
            },
            {
                "default": None,
                "description": "要测试的化合物列表，每个包含'name'、'concentration'和'vehicle'键",
                "name": "test_compounds",
                "type": "list of dict",
            },
        ],
    },
    {
        "description": "使用VCOG-CTCAE标准对动物研究中的不良事件进行分级和监测。",
        "name": "grade_adverse_events_using_vcog_ctcae",
        "optional_parameters": [],
        "required_parameters": [
            {
                "default": None,
                "description": "包含临床评估数据的CSV文件路径，包含以下列：subject_id、time_point、symptom、severity、measurement（可选）",
                "name": "clinical_data_file",
                "type": "str",
            }
        ],
    },
    {
        "description": "分析放射性标记抗体的生物分布和药代动力学特征。",
        "name": "analyze_radiolabeled_antibody_biodistribution",
        "optional_parameters": [],
        "required_parameters": [
            {
                "default": None,
                "description": "进行测量的时间点（小时）",
                "name": "time_points",
                "type": "List[float] or numpy.ndarray",
            },
            {
                "default": None,
                "description": "字典，键为组织名称，值为与time_points对应的%IA/g测量值列表/数组。必须包含'tumor'作为键之一",
                "name": "tissue_data",
                "type": "dict",
            },
        ],
    },
    {
        "description": "使用医学内部辐射剂量（MIRD）模式估算α粒子放射治疗药物对肿瘤和正常器官的辐射吸收剂量。",
        "name": "estimate_alpha_particle_radiotherapy_dosimetry",
        "optional_parameters": [
            {
                "default": "dosimetry_results.csv",
                "description": "保存剂量学结果的文件名",
                "name": "output_file",
                "type": "str",
            }
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "包含器官/组织名称作为键、时间-活度测量列表作为值的字典。每个测量应为(time_hours, percent_injected_activity)元组。必须包含所有相关器官的条目，包括'tumor'",
                "name": "biodistribution_data",
                "type": "dict",
            },
            {
                "default": None,
                "description": "包含α发射放射性核素辐射参数的字典，包括'radionuclide'、'half_life_hours'、'energy_per_decay_MeV'、'radiation_weighting_factor'和'S_factors'",
                "name": "radiation_parameters",
                "type": "dict",
            },
        ],
    },
    {
        "description": "执行全甲基化组关联研究（MWAS）以识别与CYP2C19代谢者状态显著相关的CpG位点。",
        "name": "perform_mwas_cyp2c19_metabolizer_status",
        "optional_parameters": [
            {
                "default": None,
                "description": "包含回归模型中要调整的协变量的CSV或TSV文件路径（例如：年龄、性别、吸烟状态）",
                "name": "covariates_path",
                "type": "str",
            },
            {
                "default": 0.05,
                "description": "多重检验校正后的显著性P值阈值",
                "name": "pvalue_threshold",
                "type": "float",
            },
            {
                "default": "significant_cpg_sites.csv",
                "description": "保存显著CpG位点的文件名",
                "name": "output_file",
                "type": "str",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "包含DNA甲基化beta值的CSV或TSV文件路径。行应为样品，列应为CpG位点",
                "name": "methylation_data_path",
                "type": "str",
            },
            {
                "default": None,
                "description": "包含每个样品CYP2C19代谢者状态的CSV或TSV文件路径。应包含样品ID列和状态列",
                "name": "metabolizer_status_path",
                "type": "str",
            },
        ],
    },
    {
        "description": "计算候选药物分子的关键理化性质。",
        "name": "calculate_physicochemical_properties",
        "optional_parameters": [],
        "required_parameters": [
            {
                "default": None,
                "description": "SMILES格式的分子结构",
                "name": "smiles_string",
                "type": "str",
            }
        ],
    },
    {
        "description": "分析不同治疗组异种移植模型中的肿瘤生长抑制。",
        "name": "analyze_xenograft_tumor_growth_inhibition",
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
                "description": "包含肿瘤体积测量值的CSV或TSV文件路径",
                "name": "data_path",
                "type": "str",
            },
            {
                "default": None,
                "description": "包含时间点的列名",
                "name": "time_column",
                "type": "str",
            },
            {
                "default": None,
                "description": "包含肿瘤体积测量值的列名",
                "name": "volume_column",
                "type": "str",
            },
            {
                "default": None,
                "description": "包含治疗组标签的列名",
                "name": "group_column",
                "type": "str",
            },
            {
                "default": None,
                "description": "包含受试者/小鼠标识符的列名",
                "name": "subject_column",
                "type": "str",
            },
        ],
    },
    {
        "description": "分析Western blot或DNA电泳图像并返回像素分布统计信息，包括强度统计、百分位数和亮度分布。使用此工具为find_roi_from_image确定适当的阈值。",
        "name": "analyze_pixel_distribution",
        "optional_parameters": [],
        "required_parameters": [
            {
                "default": None,
                "description": "输入灰度图像的路径。如果未提供后缀，将自动添加.png",
                "name": "image_path",
                "type": "str",
            }
        ],
    },
    {
        "description": "使用基于阈值的斑点检测从Western blot或DNA电泳图像中查找蛋白质条带的ROI（感兴趣区域）。返回带注释的图像路径和ROI坐标列表。首先使用analyze_pixel_distribution确定适当的阈值。返回的ROI列表可以转换为analyze_western_blot的target_bands格式。",
        "name": "find_roi_from_image",
        "optional_parameters": [
            {
                "default": True,
                "description": "如果为True，绘制绿色轮廓（凸包）和蓝色关键点框以进行调试",
                "name": "debug",
                "type": "bool",
            }
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "输入图像的路径",
                "name": "image_path",
                "type": "str",
            },
            {
                "default": None,
                "description": "低于此值的像素强度用于生成二值图像。使用analyze_pixel_distribution确定适当的值",
                "name": "lower_threshold",
                "type": "int",
            },
            {
                "default": None,
                "description": "大于或等于此值的像素强度用于生成二值图像。使用analyze_pixel_distribution确定适当的值",
                "name": "upper_threshold",
                "type": "int",
            },
            {
                "default": None,
                "description": "图像中预期的实际条带数量",
                "name": "number_of_bands",
                "type": "int",
            },
        ],
    },
    {
        "description": "对Western blot图像执行密度测定分析以量化相对蛋白质表达。",
        "name": "analyze_western_blot",
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
                "description": "Western blot图像文件的路径",
                "name": "blot_image_path",
                "type": "str",
            },
            {
                "default": None,
                "description": "包含目标蛋白质条带信息的字典列表，每个包含'name'和'roi'（感兴趣区域为[x, y, width, height]）",
                "name": "target_bands",
                "type": "list of dict",
            },
            {
                "default": None,
                "description": "包含上样对照蛋白质的'name'和'roi'的字典（例如：β-actin、GAPDH）",
                "name": "loading_control_band",
                "type": "dict",
            },
            {
                "default": None,
                "description": "包含所用抗体信息的字典，包含'primary'和'secondary'键",
                "name": "antibody_info",
                "type": "dict",
            },
        ],
    },
    {
        "description": "从DDInter数据库查询药物-药物相互作用，以识别指定药物之间的潜在相互作用、机制和严重程度。",
        "name": "query_drug_interactions",
        "required_parameters": [
            {
                "default": None,
                "description": "要查询相互作用的药物名称列表",
                "name": "drug_names",
                "type": "List[str]",
            }
        ],
        "optional_parameters": [
            {
                "default": None,
                "description": "按特定相互作用类型过滤结果",
                "name": "interaction_types",
                "type": "List[str]",
            },
            {
                "default": None,
                "description": "按严重程度过滤结果（Major、Moderate、Minor）",
                "name": "severity_levels",
                "type": "List[str]",
            },
            {
                "default": None,
                "description": "包含DDInter数据的数据湖目录路径",
                "name": "data_lake_path",
                "type": "str",
            },
        ],
    },
    {
        "description": "使用DDInter数据库分析药物组合的安全性以识别潜在相互作用，提供全面的风险评估和临床建议。",
        "name": "check_drug_combination_safety",
        "required_parameters": [
            {
                "default": None,
                "description": "要分析组合安全性的药物列表",
                "name": "drug_list",
                "type": "List[str]",
            }
        ],
        "optional_parameters": [
            {
                "default": True,
                "description": "在结果中包含相互作用机制描述",
                "name": "include_mechanisms",
                "type": "bool",
            },
            {
                "default": True,
                "description": "在结果中包含管理建议",
                "name": "include_management",
                "type": "bool",
            },
            {
                "default": None,
                "description": "包含DDInter数据的数据湖目录路径",
                "name": "data_lake_path",
                "type": "str",
            },
        ],
    },
    {
        "description": "分析两种特定药物之间的相互作用机制，提供详细的机制见解和临床意义评估。",
        "name": "analyze_interaction_mechanisms",
        "required_parameters": [
            {
                "default": None,
                "description": "要分析的药物对（drug1, drug2）",
                "name": "drug_pair",
                "type": "Tuple[str, str]",
            }
        ],
        "optional_parameters": [
            {
                "default": True,
                "description": "在分析中包含详细的机制信息",
                "name": "detailed_analysis",
                "type": "bool",
            },
            {
                "default": None,
                "description": "包含DDInter数据的数据湖目录路径",
                "name": "data_lake_path",
                "type": "str",
            },
        ],
    },
    {
        "description": "使用DDInter数据库查找不与禁忌药物相互作用的替代药物，以实现更安全的治疗替代。",
        "name": "find_alternative_drugs_ddinter",
        "required_parameters": [
            {
                "default": None,
                "description": "要查找替代品的药物",
                "name": "target_drug",
                "type": "str",
            },
            {
                "default": None,
                "description": "要避免相互作用的药物列表",
                "name": "contraindicated_drugs",
                "type": "List[str]",
            },
        ],
        "optional_parameters": [
            {
                "default": None,
                "description": "将搜索限制在特定治疗类别",
                "name": "therapeutic_class",
                "type": "str",
            },
            {
                "default": None,
                "description": "包含DDInter数据的数据湖目录路径",
                "name": "data_lake_path",
                "type": "str",
            },
        ],
    },
    {
        "description": "从OpenFDA数据库查询特定药物的FDA不良事件报告，以识别潜在的安全信号、反应模式和监管情报。",
        "name": "query_fda_adverse_events",
        "required_parameters": [
            {
                "default": None,
                "description": "要查询不良事件的药物名称",
                "name": "drug_name",
                "type": "str",
            },
        ],
        "optional_parameters": [
            {
                "default": None,
                "description": "可选的日期范围，格式为(start_date, end_date)，使用YYYY-MM-DD格式",
                "name": "date_range",
                "type": "Tuple[str, str]",
            },
            {
                "default": None,
                "description": "可选的按严重程度过滤['serious', 'non_serious']",
                "name": "severity_filter",
                "type": "List[str]",
            },
            {
                "default": None,
                "description": "可选的按结果过滤['life_threatening', 'hospitalization', 'death']",
                "name": "outcome_filter",
                "type": "List[str]",
            },
            {
                "default": 100,
                "description": "要返回的最大结果数",
                "name": "limit",
                "type": "int",
            },
        ],
    },
    {
        "description": "从OpenFDA数据库检索FDA药物标签信息，包括适应症、禁忌症、警告和剂量信息。",
        "name": "get_fda_drug_label_info",
        "required_parameters": [
            {
                "default": None,
                "description": "要查询标签信息的药物名称",
                "name": "drug_name",
                "type": "str",
            },
        ],
        "optional_parameters": [
            {
                "default": None,
                "description": "可选的要检索的特定部分列表['indications_and_usage', 'contraindications', 'warnings', 'dosage_and_administration']",
                "name": "sections",
                "type": "List[str]",
            },
        ],
    },
    {
        "description": "从OpenFDA数据库检查FDA药物召回和执法行动，以识别安全问题和监管行动。",
        "name": "check_fda_drug_recalls",
        "required_parameters": [
            {
                "default": None,
                "description": "要检查召回的药物名称",
                "name": "drug_name",
                "type": "str",
            },
        ],
        "optional_parameters": [
            {
                "default": None,
                "description": "可选的按召回类别过滤['Class I', 'Class II', 'Class III']",
                "name": "classification",
                "type": "List[str]",
            },
            {
                "default": None,
                "description": "可选的召回日期范围，格式为(start_date, end_date)",
                "name": "date_range",
                "type": "Tuple[str, str]",
            },
        ],
    },
    {
        "description": "使用OpenFDA不良事件数据分析多种药物的安全信号，以识别模式和比较风险特征。",
        "name": "analyze_fda_safety_signals",
        "required_parameters": [
            {
                "default": None,
                "description": "要分析安全信号的药物名称列表",
                "name": "drug_list",
                "type": "List[str]",
            },
        ],
        "optional_parameters": [
            {
                "default": None,
                "description": "可选的比较时间段，格式为(start_date, end_date)",
                "name": "comparison_period",
                "type": "Tuple[str, str]",
            },
            {
                "default": 2.0,
                "description": "信号检测阈值",
                "name": "signal_threshold",
                "type": "float",
            },
        ],
    },
]
