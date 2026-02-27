description = [
    {
        "description": "使用 LLM 基于基因标记和转移标签注释细胞类型。在 leiden 聚类后，使用差异表达基因注释簇，并可选地结合来自参考数据集的转移标签。",
        "name": "annotate_celltype_scRNA",
        "optional_parameters": [
            {
                "default": "leiden",
                "description": "用于细胞类型注释的聚类方法",
                "name": "cluster",
                "type": "str",
            },
            {
                "default": "claude-3-5-sonnet-20241022",
                "description": "用于细胞类型预测的语言模型实例",
                "name": "llm",
                "type": "str",
            },
            {
                "default": None,
                "description": "每个簇的转移细胞类型组成",
                "name": "composition",
                "type": "pd.DataFrame",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "包含 scRNA-seq 数据的 AnnData 文件名称",
                "name": "adata_filename",
                "type": "str",
            },
            {
                "default": None,
                "description": "包含数据文件的目录",
                "name": "data_dir",
                "type": "str",
            },
            {
                "default": None,
                "description": 'scRNA-seq 数据的信息（例如 "homo sapiens, brain tissue, normal"）',
                "name": "data_info",
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
        "description": "使用 Panhuman Azimuth 神经网络对单细胞 RNA-seq 数据执行细胞类型注释。此函数使用 panhumanpy 包实现 Panhuman Azimuth 工作流进行细胞类型注释，为人体各组织提供分层细胞类型标签。",
        "name": "annotate_celltype_with_panhumanpy",
        "optional_parameters": [
            {
                "default": None,
                "description": "adata.var 中包含基因符号的列名（默认：None，使用索引）",
                "name": "feature_names_col",
                "type": "str",
            },
            {
                "default": True,
                "description": "是否执行额外的标签细化以保持一致的粒度",
                "name": "refine",
                "type": "bool",
            },
            {
                "default": True,
                "description": "是否生成 ANN 嵌入和 UMAP",
                "name": "umap",
                "type": "bool",
            },
            {
                "default": "./output",
                "description": "保存结果的目录",
                "name": "output_dir",
                "type": "str",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "包含 scRNA-seq 数据的 AnnData 文件路径",
                "name": "adata_path",
                "type": "str",
            },
        ],
    },
    {
        "description": "为单细胞 RNA-seq 数据创建 scVI 和 scANVI 嵌入，将结果保存到 AnnData 对象。",
        "name": "create_scvi_embeddings_scRNA",
        "optional_parameters": [],
        "required_parameters": [
            {
                "default": None,
                "description": "要加载的 AnnData 对象的文件名",
                "name": "adata_filename",
                "type": "str",
            },
            {
                "default": None,
                "description": "adata.obs 中批次信息的列名",
                "name": "batch_key",
                "type": "str",
            },
            {
                "default": None,
                "description": "adata.obs 中细胞类型标签的列名",
                "name": "label_key",
                "type": "str",
            },
            {
                "default": None,
                "description": "AnnData 文件所在的目录路径以及输出将保存的位置",
                "name": "data_dir",
                "type": "str",
            },
        ],
    },
    {
        "description": "使用 Harmony 对单细胞 RNA-seq 数据执行批次整合并保存整合后的嵌入。",
        "name": "create_harmony_embeddings_scRNA",
        "optional_parameters": [],
        "required_parameters": [
            {
                "default": None,
                "description": "要加载的 AnnData 对象的文件名",
                "name": "adata_filename",
                "type": "str",
            },
            {
                "default": None,
                "description": "adata.obs 中定义整合批次变量的列名",
                "name": "batch_key",
                "type": "str",
            },
            {
                "default": None,
                "description": "输入文件所在的目录路径以及输出将保存的位置",
                "name": "data_dir",
                "type": "str",
            },
        ],
    },
    {
        "description": "为单细胞 RNA-seq 数据生成 UCE 嵌入，并将其映射到参考数据集以进行细胞类型注释。",
        "name": "get_uce_embeddings_scRNA",
        "optional_parameters": [
            {
                "default": "/dfs/project/bioagentos/data/singlecell/",
                "description": "单细胞数据存储的根目录",
                "name": "DATA_ROOT",
                "type": "str",
            },
            {
                "default": None,
                "description": "传递给 UCE 脚本的自定义命令行参数",
                "name": "custom_args",
                "type": "List[str]",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "要处理的 AnnData 对象的文件名",
                "name": "adata_filename",
                "type": "str",
            },
            {
                "default": None,
                "description": "输入数据存储和输出将保存的目录",
                "name": "data_dir",
                "type": "str",
            },
        ],
    },
    {
        "description": "使用 UCE 嵌入将输入数据集的细胞嵌入映射到 Integrated Megascale Atlas 参考数据集。",
        "name": "map_to_ima_interpret_scRNA",
        "optional_parameters": [
            {
                "default": None,
                "description": "自定义参数字典，包括最近邻搜索的 'n_neighbors' 和 'metric'",
                "name": "custom_args",
                "type": "dict",
            }
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "要映射的 AnnData 对象的文件名",
                "name": "adata_filename",
                "type": "str",
            },
            {
                "default": None,
                "description": "包含 AnnData 文件的目录",
                "name": "data_dir",
                "type": "str",
            },
        ],
    },
    {
        "description": "给定基因名称，获取 RNA-seq 表达数据，显示具有最高每百万转录本 (TPM) 值的前 K 个组织。",
        "name": "get_rna_seq_archs4",
        "optional_parameters": [
            {
                "default": 10,
                "description": "要返回的组织数量",
                "name": "K",
                "type": "int",
            }
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "正在获取 RNA-seq 数据的基因名称",
                "name": "gene_name",
                "type": "str",
            }
        ],
    },
    {
        "description": "返回基因集富集分析支持的数据库列表。",
        "name": "get_gene_set_enrichment_analysis_supported_database_list",
        "optional_parameters": [],
        "required_parameters": [],
    },
    {
        "description": "对基因列表执行富集分析，可选背景基因集和绘图功能。",
        "name": "gene_set_enrichment_analysis",
        "optional_parameters": [
            {
                "default": 10,
                "description": "要返回的顶级通路数量",
                "name": "top_k",
                "type": "int",
            },
            {
                "default": "ontology",
                "description": "用于富集分析的数据库（例如 pathway、transcription、ontology）",
                "name": "database",
                "type": "str",
            },
            {
                "default": None,
                "description": "用于富集分析的背景基因列表",
                "name": "background_list",
                "type": "list",
            },
            {
                "default": False,
                "description": "生成前 K 个富集结果的条形图",
                "name": "plot",
                "type": "bool",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "要分析的基因符号列表",
                "name": "genes",
                "type": "list",
            }
        ],
    },
    {
        "description": "从 Hi-C 数据分析染色质相互作用，以识别增强子-启动子相互作用和 TAD。",
        "name": "analyze_chromatin_interactions",
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
                "description": "Hi-C 数据文件的路径（.cool 或 .hic 格式）",
                "name": "hic_file_path",
                "type": "str",
            },
            {
                "default": None,
                "description": "包含调控元件（增强子、启动子、CTCF 位点等）基因组坐标的 BED 文件路径",
                "name": "regulatory_elements_bed",
                "type": "str",
            },
        ],
    },
    {
        "description": "对多个基因组样本执行比较基因组学和单倍型分析。将基因组样本比对到参考，识别变异，分析共享和独特的基因组区域，并确定单倍型结构。",
        "name": "analyze_comparative_genomics_and_haplotypes",
        "optional_parameters": [
            {
                "default": "./output",
                "description": "存储输出文件的目录",
                "name": "output_dir",
                "type": "str",
            }
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "包含要分析的全基因组序列的 FASTA 文件路径",
                "name": "sample_fasta_files",
                "type": "List[str]",
            },
            {
                "default": None,
                "description": "参考基因组 FASTA 文件的路径",
                "name": "reference_genome_path",
                "type": "str",
            },
        ],
    },
    {
        "description": "使用 MACS2 执行 ChIP-seq 峰调用以识别具有显著结合的基因组区域。",
        "name": "perform_chipseq_peak_calling_with_macs2",
        "optional_parameters": [
            {
                "default": "macs2_output",
                "description": "输出文件的前缀",
                "name": "output_name",
                "type": "str",
            },
            {
                "default": "hs",
                "description": "有效基因组大小简写：'hs' 表示人类，'mm' 表示小鼠等",
                "name": "genome_size",
                "type": "str",
            },
            {
                "default": 0.05,
                "description": "峰调用的 q 值（最小 FDR）截止值",
                "name": "q_value",
                "type": "float",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "ChIP-seq 读取数据文件的路径（BAM、BED 或其他支持的格式）",
                "name": "chip_seq_file",
                "type": "str",
            },
            {
                "default": None,
                "description": "对照/输入数据文件的路径（BAM、BED 或其他支持的格式）",
                "name": "control_file",
                "type": "str",
            },
        ],
    },
    {
        "description": "使用 HOMER 基序发现软件查找基因组区域中富集的 DNA 序列基序。",
        "name": "find_enriched_motifs_with_homer",
        "optional_parameters": [
            {
                "default": "hg38",
                "description": "用于序列提取的参考基因组",
                "name": "genome",
                "type": "str",
            },
            {
                "default": None,
                "description": "用于比较的背景区域 BED 文件路径。如果为 None，HOMER 将自动生成随机背景序列",
                "name": "background_file",
                "type": "str",
            },
            {
                "default": "8,10,12",
                "description": "要发现的基序长度的逗号分隔列表",
                "name": "motif_length",
                "type": "str",
            },
            {
                "default": "./homer_motifs",
                "description": "保存输出文件的目录",
                "name": "output_dir",
                "type": "str",
            },
            {
                "default": 10,
                "description": "要查找的基序数量",
                "name": "num_motifs",
                "type": "int",
            },
            {
                "default": 4,
                "description": "要使用的 CPU 线程数",
                "name": "threads",
                "type": "int",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "BED 格式的峰文件路径，包含要分析基序富集的基因组区域",
                "name": "peak_file",
                "type": "str",
            }
        ],
    },
    {
        "description": "分析两个或多个基因组区域集之间的重叠。",
        "name": "analyze_genomic_region_overlap",
        "optional_parameters": [
            {
                "default": "overlap_analysis",
                "description": "输出文件的前缀",
                "name": "output_prefix",
                "type": "str",
            }
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "基因组区域集列表。每个项目可以是 BED 文件的字符串路径，或格式为 (chrom, start, end) 或 (chrom, start, end, name) 的元组/列表的列表",
                "name": "region_sets",
                "type": "list",
            }
        ],
    },
    {
        "description": "使用 popV 将细胞类型标签从已注释的参考 scRNA-seq 数据集转移到未注释的查询数据集。加载两个 AnnData .h5ad 文件，为 scVI 准备计数层，针对参考处理查询，并运行选定的注释方法（默认：SCANVI_POPV）。将预测保存到 'output_folder/popv_output/predictions.csv'。此函数允许您使用不同的注释方法，即 CELLTYPIST、KNN_BBKNN、KNN_HARMONY、KNN_SCANORAMA、KNN_SCVI、ONCLASS、Random_Forest、SCANVI_POPV、Support_Vector、XGboost。根据您的转移任务，您可以选择多个最佳注释方法。请注意，每种注释方法都会增加运行工具的计算需求。默认情况下使用 SCANVI_POPV 方法。",
        "name": "unsupervised_celltype_transfer_between_scRNA_datasets",
        "optional_parameters": [
            {
                "default": None,
                "description": "查询 adata.obs 中包含批次信息的列，您很可能会从用户那里获得此信息",
                "name": "query_batch_key",
                "type": "str",
            },
            {
                "default": None,
                "description": "参考 adata.obs 中包含批次信息的列，您很可能会从用户那里获得此信息",
                "name": "ref_batch_key",
                "type": "str",
            },
            {
                "default": False,
                "description": "启用 CELLTYPiST（基于参考的分类器）。工作原理：在精选参考上训练的正则化逻辑回归预测每个细胞的概率；可选的邻居校正细化标签。优势：快速、可扩展、对常见人类/小鼠类型表现强劲。劣势：依赖参考覆盖范围；对新颖或分布外细胞类型有限。",
                "name": "CELLTYPIST",
                "type": "bool",
            },
            {
                "default": False,
                "description": "启用 KNN 与 BBKNN 整合。工作原理：通过强制每个批次固定数量的邻居来构建批次平衡的 kNN 图，然后将此图用于下游分析。优势：简单、快速、跨批次保留局部邻域结构。劣势：全局对齐有限；当共享细胞类型稀疏时存在残留批次效应；对 k/邻居参数敏感。",
                "name": "KNN_BBKNN",
                "type": "bool",
            },
            {
                "default": False,
                "description": "启用 KNN 与 Harmony 整合。工作原理：通过软聚类和线性校正迭代调整 PCA 嵌入，以最小化批次效应同时保留结构。优势：可扩展、在低维空间中有效的批次校正、通常保留生物学特性。劣势：可能过度校正并合并真实的生物学差异；依赖 PCA/参数。",
                "name": "KNN_HARMONY",
                "type": "bool",
            },
            {
                "default": False,
                "description": "启用 KNN 与 Scanorama 整合。工作原理：识别跨数据集的相互最近邻并执行流形对齐/低秩校正以合并'全景'。优势：对共享群体的跨数据集对齐强。劣势：在大数据上更慢且更占内存；可能扭曲稀有或独特的群体。",
                "name": "KNN_SCANORAMA",
                "type": "bool",
            },
            {
                "default": False,
                "description": "启用 KNN 与 scVI 整合（scVI 潜在空间中的 KNN）。工作原理：训练变分自编码器（负二项似然）以学习批次校正的潜在空间；在此空间中运行 KNN 以转移标签。优势：对计数和批次建模的稳健概率嵌入；良好的转移性能。劣势：需要训练（首选 GPU）；对嵌入质量和 k 敏感。",
                "name": "KNN_SCVI",
                "type": "bool",
            },
            {
                "default": False,
                "description": "启用 OnClass（本体感知分类器）。工作原理：嵌入细胞本体图并在本体节点上训练分类器；使用语义相似性泛化到未见标签（零样本）。优势：利用细胞本体；可以映射到未见/细粒度类型；可解释。劣势：依赖本体完整性和映射质量；可能分配过于通用的标签。",
                "name": "ONCLASS",
                "type": "bool",
            },
            {
                "default": False,
                "description": "启用随机森林分类器。工作原理：在自举样本上训练的决策树集成，具有特征子采样；通过多数投票/概率聚合预测。优势：对噪声和非线性信号稳健；训练快速；可用特征重要性。劣势：概率校准可能较差；稀疏数据需要特征选择；对类别不平衡敏感。",
                "name": "Random_Forest",
                "type": "bool",
            },
            {
                "default": True,
                "description": "通过 popV 启用 scANVI（默认）。工作原理：扩展 scVI，添加分类头以从标记的参考和未标记的查询中学习（半监督），产生潜在嵌入和带有不确定性的概率标签。优势：半监督；对批次、标签噪声建模；利用未标记数据；提供不确定性。劣势：训练时间较长；推荐 GPU；在严重标签偏移或噪声参考下可能降级。",
                "name": "SCANVI_POPV",
                "type": "bool",
            },
            {
                "default": False,
                "description": "启用支持向量分类器。工作原理：找到最大间隔超平面；使用核（例如 RBF）对非线性边界建模。优势：在高维、小样本设置中有效；核灵活性。劣势：需要超参数调整；默认情况下不是概率性的；对非常大的数据集扩展性差。",
                "name": "Support_Vector",
                "type": "bool",
            },
            {
                "default": False,
                "description": "启用 XGBoost 分类器。工作原理：使用二阶优化和正则化顺序训练梯度提升决策树以最小化损失。优势：高准确性；捕获非线性交互；内置正则化。劣势：许多超参数；对噪声、稀疏计数过拟合的风险；可解释性较差。",
                "name": "XGboost",
                "type": "bool",
            },
            {
                "default": 1,
                "description": "popV 的并行作业数",
                "name": "n_jobs",
                "type": "int",
            },
            {
                "default": "./tmp/",
                "description": "保存训练模型和预测的目录",
                "name": "output_folder",
                "type": "str",
            },
            {
                "default": 10,
                "description": "每个标签的样本数（当前未使用）",
                "name": "n_samples_per_label",
                "type": "int",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "已注释参考 AnnData (.h5ad) 的路径",
                "name": "path_to_annotated_h5ad",
                "type": "str",
            },
            {
                "default": None,
                "description": "未注释查询 AnnData (.h5ad) 的路径",
                "name": "path_to_not_annotated_h5ad",
                "type": "str",
            },
            {
                "default": None,
                "description": "参考 adata.obs 中包含细胞类型标签的列",
                "name": "ref_labels_key",
                "type": "str",
            },
        ],
    },
    {
        "description": "使用 SE-600M 模型为单细胞 RNA-seq 数据生成 State 嵌入。此函数从 Hugging Face 下载 SE-600M 模型，安装所需的依赖项（git-lfs、uv、arc-state），并为输入的 AnnData 对象生成嵌入。SE-600M 模型是用于单细胞数据的最先进嵌入模型，可以捕获复杂的生物学模式和细胞状态。功能包括实时流式输出、失败时自动重试并减少批次大小、GPU 检测和警告以及输入验证。",
        "name": "generate_embeddings_with_state",
        "optional_parameters": [
            {
                "default": None,
                "description": "输出嵌入文件的名称。如果为 None，将使用带有 '_state_embeddings' 后缀的输入文件名",
                "name": "output_filename",
                "type": "str",
            },
            {
                "default": None,
                "description": "特定模型检查点的路径。如果为 None，使用 model_folder 中的最新检查点",
                "name": "checkpoint",
                "type": "str",
            },
            {
                "default": "X_state",
                "description": "在输出 AnnData 对象中存储嵌入的键名称",
                "name": "embed_key",
                "type": "str",
            },
            {
                "default": None,
                "description": "蛋白质嵌入覆盖的路径 (.pt)。如果省略，在模型文件夹中自动检测",
                "name": "protein_embeddings",
                "type": "str",
            },
            {
                "default": 500,
                "description": "嵌入前向传递的批次大小。增加以使用更多 VRAM 并加快嵌入速度",
                "name": "batch_size",
                "type": "int",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "输入 AnnData 文件的名称（.h5ad 格式）",
                "name": "adata_filename",
                "type": "str",
            },
            {
                "default": None,
                "description": "包含输入数据文件的目录",
                "name": "data_dir",
                "type": "str",
            },
            {
                "default": None,
                "description": "SE-600M 模型将被下载和存储的目录",
                "name": "model_folder",
                "type": "str",
            },
        ],
    },
    {
        "description": "使用 BioMart 同源性映射在不同物种之间转换 ENSEMBL 基因 ID。此函数使用 Ensembl BioMart 数据库将一个物种的 ENSEMBL 基因 ID 列表转换为另一个物种的同源对应物。转换基于物种之间的一对一直系同源映射。",
        "name": "interspecies_gene_conversion",
        "optional_parameters": [],
        "required_parameters": [
            {
                "default": None,
                "description": "要转换的 ENSEMBL 基因 ID 列表（例如 ['ENSG00000007372', 'ENSG00000181449']）",
                "name": "gene_list",
                "type": "list[str]",
            },
            {
                "default": None,
                "description": "源物种名称。支持的物种：human、mouse、rat、zebrafish、fly、drosophila、worm、yeast、chicken、pig、cow、dog、macaque",
                "name": "source_species",
                "type": "str",
            },
            {
                "default": None,
                "description": "目标物种名称。与 source_species 支持的物种相同",
                "name": "target_species",
                "type": "str",
            },
        ],
    },
    {
        "description": "使用 ESM（进化尺度建模）蛋白质语言模型为 Ensembl 基因 ID 列表生成平均蛋白质嵌入。此函数获取每个基因的所有蛋白质同工型序列，使用指定的 ESM 模型和层为每个同工型计算嵌入，然后对所有同工型的嵌入进行平均，为每个基因创建单个代表性嵌入。嵌入保存为 PyTorch 张量以供将来使用。内存友好的实现，具有滚动平均、小批次处理和自动内存管理。自动处理 GPU/CPU 设备选择，并包括内存不足情况的错误恢复，通过回退到单序列处理。",
        "name": "generate_gene_embeddings_with_ESM_models",
        "optional_parameters": [
            {
                "default": "esm2_t6_8M_UR50D",
                "description": "用于生成嵌入的 ESM 模型名称",
                "name": "model_name",
                "type": "str",
            },
            {
                "default": 6,
                "description": "从 ESM 模型的哪一层提取嵌入，通常使用最后一层",
                "name": "layer",
                "type": "int",
            },
            {
                "default": None,
                "description": "将嵌入保存为 PyTorch 字典的可选路径",
                "name": "save_path",
                "type": "str",
            },
            {
                "default": 1,
                "description": "一次处理的序列数量以管理内存使用",
                "name": "batch_size",
                "type": "int",
            },
            {
                "default": 1024,
                "description": "要处理的最大序列长度，较长的序列将被过滤掉",
                "name": "max_sequence_length",
                "type": "int",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "Ensembl 基因 ID 列表（例如 ['ENSG00000012048', 'ENSG00000012049']）",
                "name": "ensembl_gene_ids",
                "type": "List[str]",
            }
        ],
    },
    {
        "description": "为单细胞 RNA-seq 数据生成 Transcriptformer 嵌入。此函数下载模型检查点，使用所需字段（ensembl_id、原始计数、测定元数据）准备 AnnData 对象，并运行推理以生成细胞或基因嵌入。Transcriptformer 是一个基于 transformer 的模型，可以学习单细胞基因表达数据的丰富表示。该函数自动处理 Ensembl ID 模式检测、模型下载、数据预处理，并在需要时创建缺失的测定元数据列，使用 'unknown' 值。",
        "name": "generate_transcriptformer_embeddings",
        "optional_parameters": [
            {
                "default": None,
                "description": "输出嵌入文件的名称。如果为 None，将使用带有 '_transcriptformer_embeddings' 后缀的输入文件名",
                "name": "output_filename",
                "type": "str",
            },
            {
                "default": "tf-sapiens",
                "description": "要下载和使用的 transcriptformer 模型类型。选项：'tf-sapiens'、'tf-exemplar'、'tf-metazoa'",
                "name": "model_type",
                "type": "str",
            },
            {
                "default": None,
                "description": "transcriptformer 检查点目录的路径。如果为 None，将使用 './checkpoints/{model_type}'",
                "name": "checkpoint_path",
                "type": "str",
            },
            {
                "default": 8,
                "description": "推理的批次大小",
                "name": "batch_size",
                "type": "int",
            },
            {
                "default": "16-mixed",
                "description": "推理的精度。选项：'16-mixed'、'32'",
                "name": "precision",
                "type": "str",
            },
            {
                "default": 30,
                "description": "要裁剪到的最大计数值",
                "name": "clip_counts",
                "type": "int",
            },
            {
                "default": -1,
                "description": "从哪一层提取嵌入（-1 表示最后一层）",
                "name": "embedding_layer_index",
                "type": "int",
            },
            {
                "default": 1,
                "description": "要使用的 GPU 数量",
                "name": "num_gpus",
                "type": "int",
            },
            {
                "default": 0,
                "description": "数据加载工作线程数",
                "name": "n_data_workers",
                "type": "int",
            },
            {
                "default": "ensembl_id",
                "description": "AnnData.var 中包含基因标识符的列名",
                "name": "gene_col_name",
                "type": "str",
            },
            {
                "default": None,
                "description": "用于分布外物种的预训练嵌入路径",
                "name": "pretrained_embedding",
                "type": "str",
            },
            {
                "default": True,
                "description": "是否将基因过滤为仅词汇表中的基因",
                "name": "filter_to_vocabs",
                "type": "bool",
            },
            {
                "default": "None",
                "description": "是否使用 AnnData.raw.X 的原始计数（True）、adata.X（False）或自动检测（None/auto）",
                "name": "use_raw",
                "type": "str",
            },
            {
                "default": "cell",
                "description": "要提取的嵌入类型：'cell' 表示平均池化的细胞嵌入，'cge' 表示上下文基因嵌入",
                "name": "emb_type",
                "type": "str",
            },
            {
                "default": False,
                "description": "如果发现重复基因，则删除而不是引发错误",
                "name": "remove_duplicate_genes",
                "type": "bool",
            },
            {
                "default": False,
                "description": "使用映射样式的内存外 DataLoader（DistributedSampler 友好）",
                "name": "oom_dataloader",
                "type": "bool",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "输入 AnnData 文件的名称（.h5ad 格式）",
                "name": "adata_filename",
                "type": "str",
            },
            {
                "default": None,
                "description": "包含输入数据文件的目录",
                "name": "data_dir",
                "type": "str",
            },
        ],
    },
]
