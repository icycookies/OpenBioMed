description = [
    {
        "description": "使用Biopython在DNA序列中查找所有开放阅读框（ORF），搜索正向和反向互补链。",
        "name": "annotate_open_reading_frames",
        "optional_parameters": [
            {
                "default": False,
                "description": "是否搜索反向互补链",
                "name": "search_reverse",
                "type": "bool",
            },
            {
                "default": False,
                "description": "是否过滤掉具有相同终点但较晚起点的ORF",
                "name": "filter_subsets",
                "type": "bool",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "要分析的DNA序列",
                "name": "sequence",
                "type": "str",
            },
            {
                "default": None,
                "description": "ORF的最小长度（核苷酸数）",
                "name": "min_length",
                "type": "int",
            },
        ],
    },
    {
        "description": "使用pLannotate的命令行界面注释DNA序列。",
        "name": "annotate_plasmid",
        "optional_parameters": [
            {
                "default": True,
                "description": "序列是否为环状",
                "name": "is_circular",
                "type": "bool",
            }
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "要注释的DNA序列",
                "name": "sequence",
                "type": "str",
            }
        ],
    },
    {
        "description": "从NCBI Entrez检索指定基因的编码序列。",
        "name": "get_gene_coding_sequence",
        "optional_parameters": [
            {
                "default": None,
                "description": "用于NCBI Entrez的电子邮件地址（推荐）",
                "name": "email",
                "type": "str",
            }
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "基因名称",
                "name": "gene_name",
                "type": "str",
            },
            {
                "default": None,
                "description": "生物体名称",
                "name": "organism",
                "type": "str",
            },
        ],
    },
    {
        "description": "统一函数，用于从Addgene或NCBI检索质粒序列。如果is_addgene为True或标识符为数字，则使用Addgene。否则使用质粒名称搜索NCBI。",
        "name": "get_plasmid_sequence",
        "optional_parameters": [
            {
                "default": None,
                "description": "如果为True则强制使用Addgene查找，如果为False则强制使用NCBI。如果为None，则根据标识符格式尝试自动检测。",
                "name": "is_addgene",
                "type": "bool",
            }
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "Addgene ID或质粒名称",
                "name": "identifier",
                "type": "str",
            }
        ],
    },
    {
        "description": "将短序列（引物）比对到较长序列，允许一个错配。检查正向和反向互补链。",
        "name": "align_sequences",
        "optional_parameters": [],
        "required_parameters": [
            {
                "default": None,
                "description": "目标DNA序列",
                "name": "long_seq",
                "type": "str",
            },
            {
                "default": None,
                "description": "单个引物或引物列表",
                "name": "short_seqs",
                "type": "Union[str, List[str]]",
            },
        ],
    },
    {
        "description": "使用给定的引物和序列模拟PCR扩增。",
        "name": "pcr_simple",
        "optional_parameters": [
            {
                "default": False,
                "description": "序列是否为环状",
                "name": "circular",
                "type": "bool",
            }
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "序列字符串或质粒文件路径",
                "name": "sequence",
                "type": "str",
            },
            {
                "default": None,
                "description": "正向引物序列（5'到3'）",
                "name": "forward_primer",
                "type": "str",
            },
            {
                "default": None,
                "description": "反向引物序列（5'到3'）",
                "name": "reverse_primer",
                "type": "str",
            },
        ],
    },
    {
        "description": "模拟DNA序列的限制性内切酶消化并返回产生的片段及其属性。",
        "name": "digest_sequence",
        "optional_parameters": [
            {
                "default": True,
                "description": "DNA序列是环状（True）还是线性（False）",
                "name": "is_circular",
                "type": "bool",
            }
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "要消化的输入DNA序列",
                "name": "dna_sequence",
                "type": "str",
            },
            {
                "default": None,
                "description": "用于消化的限制性内切酶名称",
                "name": "enzyme_names",
                "type": "List[str]",
            },
        ],
    },
    {
        "description": "在给定的DNA序列中识别指定酶的限制性内切酶位点。",
        "name": "find_restriction_sites",
        "optional_parameters": [
            {
                "default": True,
                "description": "DNA序列是环状（True）还是线性（False）",
                "name": "is_circular",
                "type": "bool",
            }
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "完整的输入DNA序列",
                "name": "dna_sequence",
                "type": "str",
            },
            {
                "default": None,
                "description": "要检查的限制性内切酶名称列表",
                "name": "enzymes",
                "type": "List[str]",
            },
        ],
    },
    {
        "description": "在DNA序列中查找常见的限制性内切酶位点并返回其切割位置。",
        "name": "find_restriction_enzymes",
        "optional_parameters": [
            {
                "default": False,
                "description": "序列是否为环状",
                "name": "is_circular",
                "type": "bool",
            }
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "要分析的DNA序列",
                "name": "sequence",
                "type": "str",
            }
        ],
    },
    {
        "description": "将查询序列与参考序列进行比较以识别突变。",
        "name": "find_sequence_mutations",
        "optional_parameters": [
            {
                "default": 1,
                "description": "查询序列的起始位置",
                "name": "query_start",
                "type": "int",
            }
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "正在分析的序列",
                "name": "query_sequence",
                "type": "str",
            },
            {
                "default": None,
                "description": "要比较的参考序列",
                "name": "reference_sequence",
                "type": "str",
            },
        ],
    },
    {
        "description": "通过搜索预计算的sgRNA库为CRISPR敲除设计sgRNA。返回用于靶向特定基因的优化向导RNA。",
        "name": "design_knockout_sgrna",
        "optional_parameters": [
            {
                "default": "human",
                "description": "目标生物体物种",
                "name": "species",
                "type": "str",
            },
            {
                "default": 1,
                "description": "要返回的向导数量",
                "name": "num_guides",
                "type": "int",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "目标基因符号/名称（例如：'EGFR'、'TP53'）",
                "name": "gene_name",
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
        "description": "返回不含磷酸化的寡核苷酸退火标准方案。",
        "name": "get_oligo_annealing_protocol",
        "optional_parameters": [],
        "required_parameters": [],
    },
    {
        "description": "根据插入片段数量和特定DNA序列返回定制的Golden Gate组装方案。",
        "name": "get_golden_gate_assembly_protocol",
        "optional_parameters": [
            {
                "default": 1,
                "description": "要组装的插入片段数量",
                "name": "num_inserts",
                "type": "int",
            },
            {
                "default": 75.0,
                "description": "要使用的载体量（ng）",
                "name": "vector_amount_ng",
                "type": "float",
            },
            {
                "default": None,
                "description": "插入片段长度列表（bp）",
                "name": "insert_lengths",
                "type": "List[int]",
            },
            {
                "default": False,
                "description": "是否用于文库制备",
                "name": "is_library_prep",
                "type": "bool",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "要使用的Type IIS限制性内切酶",
                "name": "enzyme_name",
                "type": "str",
            },
            {
                "default": None,
                "description": "目标载体的长度（bp）",
                "name": "vector_length",
                "type": "int",
            },
        ],
    },
    {
        "description": "返回细菌转化的标准方案。",
        "name": "get_bacterial_transformation_protocol",
        "optional_parameters": [
            {
                "default": "ampicillin",
                "description": "筛选抗生素",
                "name": "antibiotic",
                "type": "str",
            },
            {
                "default": False,
                "description": "序列是否包含重复元件",
                "name": "is_repetitive",
                "type": "bool",
            },
        ],
        "required_parameters": [],
    },
    {
        "description": "在给定的序列窗口内设计单个引物。",
        "name": "design_primer",
        "optional_parameters": [
            {
                "default": 20,
                "description": "要设计的引物长度",
                "name": "primer_length",
                "type": "int",
            },
            {
                "default": 0.4,
                "description": "最小GC含量",
                "name": "min_gc",
                "type": "float",
            },
            {
                "default": 0.6,
                "description": "最大GC含量",
                "name": "max_gc",
                "type": "float",
            },
            {
                "default": 55.0,
                "description": "最小熔解温度（°C）",
                "name": "min_tm",
                "type": "float",
            },
            {
                "default": 65.0,
                "description": "最大熔解温度（°C）",
                "name": "max_tm",
                "type": "float",
            },
            {
                "default": 100,
                "description": "搜索引物的窗口大小",
                "name": "search_window",
                "type": "int",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "目标DNA序列",
                "name": "sequence",
                "type": "str",
            },
            {
                "default": None,
                "description": "引物搜索的起始位置",
                "name": "start_pos",
                "type": "int",
            },
        ],
    },
    {
        "description": "设计Sanger测序引物以验证质粒中的特定区域。首先尝试使用现有引物库中的引物。如果它们无法完全覆盖该区域，则根据需要设计额外的引物。",
        "name": "design_verification_primers",
        "optional_parameters": [
            {
                "default": None,
                "description": "现有引物列表，包含其序列和可选名称",
                "name": "existing_primers",
                "type": "Optional[List[Dict[str, str]]]",
            },
            {
                "default": True,
                "description": "质粒是否为环状",
                "name": "is_circular",
                "type": "bool",
            },
            {
                "default": 800,
                "description": "每个引物的典型读长（碱基对）",
                "name": "coverage_length",
                "type": "int",
            },
            {
                "default": 20,
                "description": "新设计引物的长度",
                "name": "primer_length",
                "type": "int",
            },
            {
                "default": 0.4,
                "description": "新引物的最小GC含量",
                "name": "min_gc",
                "type": "float",
            },
            {
                "default": 0.6,
                "description": "新引物的最大GC含量",
                "name": "max_gc",
                "type": "float",
            },
            {
                "default": 55.0,
                "description": "最小熔解温度（°C）",
                "name": "min_tm",
                "type": "float",
            },
            {
                "default": 65.0,
                "description": "最大熔解温度（°C）",
                "name": "max_tm",
                "type": "float",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "完整的质粒序列",
                "name": "plasmid_sequence",
                "type": "str",
            },
            {
                "default": None,
                "description": "要验证的起始和结束位置（基于0的索引）",
                "name": "target_region",
                "type": "Tuple[int, int]",
            },
        ],
    },
    {
        "description": "基于骨架的限制性位点分析，设计带有Type IIS限制性内切酶突出端的互补寡核苷酸，用于Golden Gate组装。",
        "name": "design_golden_gate_oligos",
        "optional_parameters": [
            {
                "default": True,
                "description": "骨架是否为环状",
                "name": "is_circular",
                "type": "bool",
            }
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "完整的骨架序列",
                "name": "backbone_sequence",
                "type": "str",
            },
            {
                "default": None,
                "description": "要插入的序列（例如：sgRNA靶序列）",
                "name": "insert_sequence",
                "type": "str",
            },
            {
                "default": None,
                "description": "要使用的Type IIS限制性内切酶",
                "name": "enzyme_name",
                "type": "str",
            },
        ],
    },
    {
        "description": "模拟Golden Gate组装以从骨架和片段序列预测最终构建体序列。",
        "name": "golden_gate_assembly",
        "optional_parameters": [
            {
                "default": True,
                "description": "骨架是否为环状",
                "name": "is_circular",
                "type": "bool",
            }
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "完整的骨架序列",
                "name": "backbone_sequence",
                "type": "str",
            },
            {
                "default": None,
                "description": "要使用的Type IIS限制性内切酶（例如：'BsmBI'、'BsaI'）",
                "name": "enzyme_name",
                "type": "str",
            },
            {
                "default": None,
                "description": "要插入的片段列表，包含以下之一：name + fwd_oligo + rev_oligo（具有匹配突出端的寡核苷酸对）或name + sequence（包含限制性位点的双链DNA片段）",
                "name": "fragments",
                "type": "List[Dict[str, str]]",
            },
        ],
    },
]
