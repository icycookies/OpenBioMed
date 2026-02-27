description = [
    {
        "description": "对基因组规模代谢网络模型执行通量平衡分析（FBA）并返回过程和结果的研究日志",
        "name": "perform_flux_balance_analysis",
        "optional_parameters": [
            {
                "default": None,
                "description": "反应约束字典，键为反应ID，值为(lower_bound, upper_bound)元组",
                "name": "constraints",
                "type": "dict",
            },
            {
                "default": None,
                "description": "用作目标函数的反应ID（例如生物量反应）",
                "name": "objective_reaction",
                "type": "str",
            },
            {
                "default": "fba_results.csv",
                "description": "保存通量分布结果的文件名",
                "name": "output_file",
                "type": "str",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "代谢模型文件的路径（SBML或JSON格式）",
                "name": "model_file",
                "type": "str",
            }
        ],
    },
    {
        "description": "建模蛋白质二聚化网络以找到二聚体的平衡浓度",
        "name": "model_protein_dimerization_network",
        "optional_parameters": [],
        "required_parameters": [
            {
                "default": None,
                "description": "将单体名称映射到其初始浓度的字典（任意单位）",
                "name": "monomer_concentrations",
                "type": "dict",
            },
            {
                "default": None,
                "description": "将二聚体名称（作为'A-B'字符串）映射到其结合常数（Ka）的字典",
                "name": "dimerization_affinities",
                "type": "dict",
            },
            {
                "default": None,
                "description": "可以形成二聚体的(monomer1, monomer2)对列表",
                "name": "network_topology",
                "type": "list",
            },
        ],
    },
    {
        "description": "构建和模拟代谢网络的动力学模型并分析其对扰动的响应",
        "name": "simulate_metabolic_network_perturbation",
        "optional_parameters": [
            {"default": 100, "description": "总模拟时间", "name": "simulation_time", "type": "float"},
            {"default": 1000, "description": "要模拟的时间点数量", "name": "time_points", "type": "int"},
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "COBRA模型文件的路径（SBML格式）",
                "name": "model_file",
                "type": "str",
            },
            {
                "default": None,
                "description": "将代谢物ID映射到其初始浓度的字典",
                "name": "initial_concentrations",
                "type": "dict",
            },
            {
                "default": None,
                "description": "包含键'time'（float）、'metabolite'（str）和'factor'（float）的扰动详情字典",
                "name": "perturbation_params",
                "type": "dict",
            },
        ],
    },
    {
        "description": "使用基于ODE的逻辑建模和归一化Hill函数模拟蛋白质信号网络动力学",
        "name": "simulate_protein_signaling_network",
        "optional_parameters": [
            {
                "default": 100,
                "description": "总模拟时间，任意时间单位",
                "name": "simulation_time",
                "type": "float",
            },
            {
                "default": 1000,
                "description": "模拟的时间点数量",
                "name": "time_points",
                "type": "int",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "定义网络拓扑的字典。每个键是目标蛋白质，其值是(regulator, regulation_type)元组列表，其中regulation_type为1表示激活，-1表示抑制",
                "name": "network_structure",
                "type": "dict",
            },
            {
                "default": None,
                "description": "反应参数字典。键为(regulator, target)元组，值为包含键'W'（权重）、'n'（Hill系数）和'EC50'（半最大有效浓度）的字典",
                "name": "reaction_params",
                "type": "dict",
            },
            {
                "default": None,
                "description": "物种参数字典。键为蛋白质名称，值为包含键'tau'（时间常数）、'y0'（初始浓度）和'ymax'（最大浓度）的字典",
                "name": "species_params",
                "type": "dict",
            },
        ],
    },
    {
        "description": "比较两个蛋白质结构以识别结构差异和构象变化",
        "name": "compare_protein_structures",
        "optional_parameters": [
            {
                "default": "A",
                "description": "第一个结构中要分析的链ID",
                "name": "chain_id1",
                "type": "str",
            },
            {
                "default": "A",
                "description": "第二个结构中要分析的链ID",
                "name": "chain_id2",
                "type": "str",
            },
            {
                "default": "protein_comparison",
                "description": "输出文件的前缀",
                "name": "output_prefix",
                "type": "str",
            },
        ],
        "required_parameters": [
            {"default": None, "description": "第一个PDB文件的路径", "name": "pdb_file1", "type": "str"},
            {"default": None, "description": "第二个PDB文件的路径", "name": "pdb_file2", "type": "str"},
        ],
    },
    {
        "description": "模拟肾素-血管紧张素系统（RAS）组分的时间依赖性浓度",
        "name": "simulate_renin_angiotensin_system_dynamics",
        "optional_parameters": [
            {
                "default": 48,
                "description": "总模拟时间，单位为小时",
                "name": "simulation_time",
                "type": "float",
            },
            {"default": 100, "description": "要评估的时间点数量", "name": "time_points", "type": "int"},
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "RAS组分的初始浓度，包含键：'renin'、'angiotensinogen'、'angiotensin_I'、'angiotensin_II'、'ACE2_angiotensin_II'、'angiotensin_1_7'",
                "name": "initial_concentrations",
                "type": "dict",
            },
            {
                "default": None,
                "description": "动力学速率常数，包含键：'k_ren'、'k_agt'、'k_ace'、'k_ace2'、'k_at1r'、'k_mas'",
                "name": "rate_constants",
                "type": "dict",
            },
            {
                "default": None,
                "description": "控制反馈机制的参数，包含键：'fb_ang_II'、'fb_ace2'",
                "name": "feedback_params",
                "type": "dict",
            },
        ],
    },
    {
        "description": "回答关于DNA序列的功能和属性问题",
        "name": "query_chatnt",
        "optional_parameters": [
            {
                "default": -1,
                "description": "用于ChatNT模型的设备。默认为-1（CPU）",
                "name": "device",
                "type": "int",
            }
        ],
        "required_parameters": [
            {"default": "A", "description": "关于DNA序列的问题", "name": "question", "type": "str"},
            {"default": "A", "description": "具有潜在功能的DNA序列", "name": "sequence", "type": "str"},
        ],
    },
]
