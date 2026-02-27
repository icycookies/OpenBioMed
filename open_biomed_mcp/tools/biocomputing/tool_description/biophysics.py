description = [
    {
        "description": "使用 IUPred2A 预测蛋白质序列中的内在无序区域 (IDR)。",
        "name": "predict_protein_disorder_regions",
        "optional_parameters": [
            {
                "default": 0.5,
                "description": "无序评分阈值，高于该阈值的残基被认为是无序的",
                "name": "threshold",
                "type": "float",
            },
            {
                "default": "disorder_prediction_results.csv",
                "description": "保存每个残基无序评分的文件名",
                "name": "output_file",
                "type": "str",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "要分析的蛋白质的氨基酸序列",
                "name": "protein_sequence",
                "type": "str",
            }
        ],
    },
    {
        "description": "从荧光显微镜图像量化细胞形态和细胞骨架组织。",
        "name": "analyze_cell_morphology_and_cytoskeleton",
        "optional_parameters": [
            {
                "default": "./results",
                "description": "保存输出文件的目录",
                "name": "output_dir",
                "type": "str",
            },
            {
                "default": "otsu",
                "description": "细胞分割方法（'otsu'、'adaptive' 或 'manual'）",
                "name": "threshold_method",
                "type": "str",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "荧光显微镜图像文件的路径",
                "name": "image_path",
                "type": "str",
            }
        ],
    },
    {
        "description": "从显微镜图像序列量化组织变形和流动动力学。",
        "name": "analyze_tissue_deformation_flow",
        "optional_parameters": [
            {
                "default": "results",
                "description": "保存结果的目录",
                "name": "output_dir",
                "type": "str",
            },
            {
                "default": 1.0,
                "description": "像素的物理尺度（例如 μm/pixel），用于正确缩放度量",
                "name": "pixel_scale",
                "type": "float",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "显微镜图像序列（文件路径列表或 3D numpy 数组 [time, height, width]）",
                "name": "image_sequence",
                "type": "list or numpy.ndarray",
            }
        ],
    },
]
