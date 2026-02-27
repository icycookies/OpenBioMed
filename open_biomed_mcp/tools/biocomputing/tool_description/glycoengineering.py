description = [
    {
        "name": "find_n_glycosylation_motifs",
        "description": "扫描蛋白质序列以查找典型的N-糖基化序列基序（N-X-[S/T]，X≠P）。返回位置和基序信息。",
        "required_parameters": [
            {
                "name": "sequence",
                "type": "str",
                "description": "蛋白质序列（单字母氨基酸代码）",
                "default": None,
            }
        ],
        "optional_parameters": [
            {
                "name": "allow_overlap",
                "type": "bool",
                "description": "允许检测重叠的基序",
                "default": False,
            }
        ],
    },
    {
        "name": "predict_o_glycosylation_hotspots",
        "description": "使用局部S/T密度进行启发式O-糖基化位点热点预测（轻量级基线方法；最先进方法请参考NetOGlyc 4.0）。",
        "required_parameters": [
            {
                "name": "sequence",
                "type": "str",
                "description": "蛋白质序列（单字母氨基酸代码）",
                "default": None,
            }
        ],
        "optional_parameters": [
            {"name": "window", "type": "int", "description": "用于局部密度计算的奇数大小窗口（>=3）", "default": 7},
            {
                "name": "min_st_fraction",
                "type": "float",
                "description": "窗口内标记位点所需的最小S/T比例",
                "default": 0.4,
            },
            {
                "name": "disallow_proline_next",
                "type": "bool",
                "description": "避免S/T后紧跟脯氨酸（Proline）的情况",
                "default": True,
            },
        ],
    },
    {
        "name": "list_glycoengineering_resources",
        "description": "精选的外部糖工程工具和资源列表（包含链接和注释），参考issue #198。",
        "required_parameters": [],
        "optional_parameters": [],
    },
]
