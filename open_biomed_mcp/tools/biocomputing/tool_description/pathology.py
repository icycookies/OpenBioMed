description = [
    {
        "description": "从心血管成像数据中分析主动脉直径和几何形状，测量主动脉根部直径、升主动脉直径，并计算几何参数，如迂曲度和扩张指数。",
        "name": "analyze_aortic_diameter_and_geometry",
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
                "description": "心血管成像数据的路径（DICOM、JPG、PNG）",
                "name": "image_path",
                "type": "str",
            }
        ],
    },
    {
        "description": "分析基于发光的ATP测定数据以确定细胞内ATP浓度。",
        "name": "analyze_atp_luminescence_assay",
        "optional_parameters": [
            {
                "default": "cell_count",
                "description": "用于归一化ATP值的方法，可选cell_count或protein_content",
                "name": "normalization_method",
                "type": "str",
            },
            {
                "default": None,
                "description": "包含归一化数据的CSV文件路径或以样品ID为键、归一化值为值的字典",
                "name": "normalization_data",
                "type": "str or dict",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "包含样品发光读数的CSV文件路径，包含Sample_ID和Luminescence_Value列",
                "name": "data_file",
                "type": "str",
            },
            {
                "default": None,
                "description": "包含标准曲线数据的CSV文件路径，包含ATP_Concentration（nM）和Luminescence_Value列",
                "name": "standard_curve_file",
                "type": "str",
            },
        ],
    },
    {
        "description": "分析H&E染色的血栓样本组织学图像，以识别和量化不同的血栓成分（新鲜、细胞溶解、内皮化、成纤维细胞反应）。",
        "name": "analyze_thrombus_histology",
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
                "description": "H&E染色的血栓样本组织学图像路径",
                "name": "image_path",
                "type": "str",
            }
        ],
    },
    {
        "description": "使用Rhod-2荧光指示剂从显微镜图像中分析细胞内钙浓度。",
        "name": "analyze_intracellular_calcium_with_rhod2",
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
                "description": "背景图像的路径（无细胞，仅培养基）",
                "name": "background_image_path",
                "type": "str",
            },
            {
                "default": None,
                "description": "对照图像的路径（无钙刺激的细胞）",
                "name": "control_image_path",
                "type": "str",
            },
            {
                "default": None,
                "description": "样品图像的路径（有钙刺激的细胞）",
                "name": "sample_image_path",
                "type": "str",
            },
        ],
    },
    {
        "description": "量化免疫荧光标记的角膜神经纤维的体积/密度。",
        "name": "quantify_corneal_nerve_fibers",
        "optional_parameters": [
            {
                "default": "./output",
                "description": "保存输出文件的目录",
                "name": "output_dir",
                "type": "str",
            },
            {
                "default": "otsu",
                "description": "阈值处理方法（'otsu'、'adaptive'、'manual'）",
                "name": "threshold_method",
                "type": "str",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "免疫荧光显微镜图像文件的路径",
                "name": "image_path",
                "type": "str",
            },
            {
                "default": None,
                "description": "神经纤维标记物类型（例如：'βIII-tubulin'、'SP'、'L1CAM'）",
                "name": "marker_type",
                "type": "str",
            },
        ],
    },
    {
        "description": "从多通道组织图像中分割细胞并量化蛋白质表达水平。",
        "name": "segment_and_quantify_cells_in_multiplexed_images",
        "optional_parameters": [
            {
                "default": 0,
                "description": "核标记物通道的索引（通常为DAPI）",
                "name": "nuclear_channel_index",
                "type": "int",
            },
            {
                "default": "./output",
                "description": "保存输出文件的目录",
                "name": "output_dir",
                "type": "str",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "多通道图像文件的路径（tiff堆栈或类似格式）",
                "name": "image_path",
                "type": "str",
            },
            {
                "default": None,
                "description": "与图像中每个通道对应的标记物名称列表",
                "name": "markers_list",
                "type": "List[str]",
            },
        ],
    },
    {
        "description": "从3D显微CT图像中分析骨微结构参数，计算骨矿物质密度、骨体积、骨小梁数量、厚度和间距。",
        "name": "analyze_bone_microct_morphometry",
        "optional_parameters": [
            {
                "default": "./results",
                "description": "保存输出文件的目录",
                "name": "output_dir",
                "type": "str",
            },
            {
                "default": None,
                "description": "骨分割的阈值。如果为None，将使用Otsu方法",
                "name": "threshold_value",
                "type": "float",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "显微CT扫描数据文件的路径（TIFF堆栈或类似的3D格式）",
                "name": "input_file_path",
                "type": "str",
            }
        ],
    },
]
