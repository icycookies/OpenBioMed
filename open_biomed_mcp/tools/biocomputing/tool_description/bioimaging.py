description = [
    # Segmentation functions
    {
        "description": "将 4D NIfTI 文件拆分为单独的模态文件以供 nnUNet 处理。处理包含 FLAIR、T1w、t1gd 和 T2w 模态的 BRATS 数据集格式。",
        "name": "split_modalities",
        "optional_parameters": [
            {
                "default": "BRAT",
                "description": "病例文件的基本名称",
                "name": "case_name",
                "type": "str",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "要拆分的 4D NIfTI 文件路径",
                "name": "input_file",
                "type": "str",
            },
            {
                "default": None,
                "description": "保存拆分模态文件的目录",
                "name": "output_dir",
                "type": "str",
            },
        ],
    },
    {
        "description": "通过处理 4D 和预拆分的模态文件为 nnUNet 准备输入数据。自动检测文件格式并相应地准备数据。",
        "name": "prepare_input_for_nnunet",
        "optional_parameters": [
            {
                "default": "BRAT",
                "description": "病例文件的基本名称",
                "name": "case_name",
                "type": "str",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "输入文件或目录的路径",
                "name": "input_path",
                "type": "str",
            },
            {
                "default": None,
                "description": "保存准备好的文件的目录",
                "name": "output_dir",
                "type": "str",
            },
        ],
    },
    {
        "description": "使用 nnUNet 进行图像分割，并进行适当的环境设置。支持脑肿瘤分割和其他医学图像分割任务。",
        "name": "segment_with_nn_unet",
        "optional_parameters": [
            {
                "default": "3d_fullres",
                "description": "用于分割的模型类型",
                "name": "model_type",
                "type": "str",
            },
            {
                "default": [0, 1, 2, 3, 4],
                "description": "用于集成预测的模型折叠",
                "name": "folds",
                "type": "list",
            },
            {
                "default": False,
                "description": "使用测试时增强",
                "name": "use_tta",
                "type": "bool",
            },
            {
                "default": 1,
                "description": "预处理的线程数",
                "name": "num_threads",
                "type": "int",
            },
            {
                "default": True,
                "description": "使用混合精度以加快推理速度",
                "name": "mixed_precision",
                "type": "bool",
            },
            {
                "default": True,
                "description": "启用详细日志记录",
                "name": "verbose",
                "type": "bool",
            },
            {
                "default": True,
                "description": "自动为 nnUNet 准备输入",
                "name": "auto_prepare_input",
                "type": "bool",
            },
            {
                "default": None,
                "description": "nnUNet 结果文件夹的路径",
                "name": "results_folder",
                "type": "str",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "输入图像文件或目录的路径",
                "name": "image_path",
                "type": "str",
            },
            {
                "default": None,
                "description": "保存分割结果的目录",
                "name": "output_dir",
                "type": "str",
            },
            {
                "default": None,
                "description": "任务标识符（例如 'Task001_BrainTumour'）",
                "name": "task_id",
                "type": "str",
            },
        ],
    },
    {
        "description": "使用 nilearn 创建并保存分割结果的可视化。生成叠加图和多个解剖视图。",
        "name": "create_segmentation_visualization",
        "optional_parameters": [
            {
                "default": "./visualization_output",
                "description": "保存可视化图像的目录",
                "name": "output_dir",
                "type": "str",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "原始 MRI 文件的路径",
                "name": "original_mri",
                "type": "str",
            },
            {
                "default": None,
                "description": "分割文件的路径",
                "name": "segmentation",
                "type": "str",
            },
        ],
    },
    # Image registration functions
    {
        "description": "使用 SimpleITK 在两个医学图像之间执行刚性图像配准。刚性配准仅处理平移和旋转，保持形状和大小。包括预处理、相似性度量计算和可视化生成。",
        "name": "quick_rigid_registration",
        "optional_parameters": [
            {
                "default": "mutual_information",
                "description": "配准的相似性度量：'mutual_information'、'mean_squares'、'correlation' 或 'normalized_correlation'",
                "name": "metric",
                "type": "str",
            },
            {
                "default": "gradient_descent",
                "description": "优化方法：'gradient_descent'、'lbfgsb'、'powell' 或 'amoeba'",
                "name": "optimizer",
                "type": "str",
            },
            {
                "default": True,
                "description": "是否预处理图像（去噪和归一化）",
                "name": "preprocess",
                "type": "bool",
            },
            {
                "default": True,
                "description": "是否创建可视化图表",
                "name": "create_visualizations",
                "type": "bool",
            },
            {
                "default": 0.01,
                "description": "梯度下降优化器的学习率",
                "name": "learning_rate",
                "type": "float",
            },
            {
                "default": 100,
                "description": "优化迭代的最大次数",
                "name": "number_of_iterations",
                "type": "int",
            },
            {
                "default": 1e-6,
                "description": "优化的收敛容差",
                "name": "gradient_convergence_tolerance",
                "type": "float",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "参考（固定）图像文件的路径（支持 .nii、.nii.gz、.nrrd、.mha、.mhd 格式）",
                "name": "fixed_image_path",
                "type": "str",
            },
            {
                "default": None,
                "description": "要配准的图像（移动图像）的路径",
                "name": "moving_image_path",
                "type": "str",
            },
            {
                "default": None,
                "description": "保存配准结果和输出的目录路径",
                "name": "output_dir",
                "type": "str",
            },
        ],
    },
    {
        "description": "使用 SimpleITK 在两个医学图像之间执行仿射图像配准。仿射配准处理平移、旋转、缩放和剪切。比刚性配准更灵活，但仍保持平行线。",
        "name": "quick_affine_registration",
        "optional_parameters": [
            {
                "default": "mutual_information",
                "description": "配准的相似性度量：'mutual_information'、'mean_squares'、'correlation' 或 'normalized_correlation'",
                "name": "metric",
                "type": "str",
            },
            {
                "default": "gradient_descent",
                "description": "优化方法：'gradient_descent'、'lbfgsb'、'powell' 或 'amoeba'",
                "name": "optimizer",
                "type": "str",
            },
            {
                "default": True,
                "description": "是否预处理图像（去噪和归一化）",
                "name": "preprocess",
                "type": "bool",
            },
            {
                "default": True,
                "description": "是否创建可视化图表",
                "name": "create_visualizations",
                "type": "bool",
            },
            {
                "default": 0.01,
                "description": "梯度下降优化器的学习率",
                "name": "learning_rate",
                "type": "float",
            },
            {
                "default": 100,
                "description": "优化迭代的最大次数",
                "name": "number_of_iterations",
                "type": "int",
            },
            {
                "default": 1e-6,
                "description": "优化的收敛容差",
                "name": "gradient_convergence_tolerance",
                "type": "float",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "参考（固定）图像文件的路径（支持 .nii、.nii.gz、.nrrd、.mha、.mhd 格式）",
                "name": "fixed_image_path",
                "type": "str",
            },
            {
                "default": None,
                "description": "要配准的图像（移动图像）的路径",
                "name": "moving_image_path",
                "type": "str",
            },
            {
                "default": None,
                "description": "保存配准结果和输出的目录路径",
                "name": "output_dir",
                "type": "str",
            },
        ],
    },
    {
        "description": "使用 SimpleITK 在两个医学图像之间执行可变形（B 样条）图像配准。可变形配准允许局部非线性变换，处理复杂的变形。最灵活但计算密集的配准方法。",
        "name": "quick_deformable_registration",
        "optional_parameters": [
            {
                "default": "mutual_information",
                "description": "配准的相似性度量：'mutual_information'、'mean_squares'、'correlation' 或 'normalized_correlation'",
                "name": "metric",
                "type": "str",
            },
            {
                "default": "gradient_descent",
                "description": "优化方法：'gradient_descent'、'lbfgsb'、'powell' 或 'amoeba'",
                "name": "optimizer",
                "type": "str",
            },
            {
                "default": True,
                "description": "是否预处理图像（去噪和归一化）",
                "name": "preprocess",
                "type": "bool",
            },
            {
                "default": True,
                "description": "是否创建可视化图表",
                "name": "create_visualizations",
                "type": "bool",
            },
            {
                "default": 0.01,
                "description": "梯度下降优化器的学习率",
                "name": "learning_rate",
                "type": "float",
            },
            {
                "default": 100,
                "description": "优化迭代的最大次数",
                "name": "number_of_iterations",
                "type": "int",
            },
            {
                "default": 1e-6,
                "description": "优化的收敛容差",
                "name": "gradient_convergence_tolerance",
                "type": "float",
            },
            {
                "default": 4,
                "description": "可变形配准每个维度的 B 样条控制点数量",
                "name": "number_of_control_points",
                "type": "int",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "参考（固定）图像文件的路径（支持 .nii、.nii.gz、.nrrd、.mha、.mhd 格式）",
                "name": "fixed_image_path",
                "type": "str",
            },
            {
                "default": None,
                "description": "要配准的图像（移动图像）的路径",
                "name": "moving_image_path",
                "type": "str",
            },
            {
                "default": None,
                "description": "保存配准结果和输出的目录路径",
                "name": "output_dir",
                "type": "str",
            },
        ],
    },
    {
        "description": "对多个图像执行批量配准到单个参考图像。自动处理目录中的所有医学图像文件并将它们配准到固定参考。支持对所有图像进行刚性、仿射或可变形配准。",
        "name": "batch_register_images",
        "optional_parameters": [
            {
                "default": "rigid",
                "description": "要执行的配准类型：'rigid'、'affine' 或 'deformable'",
                "name": "transform_type",
                "type": "str",
            },
            {
                "default": "mutual_information",
                "description": "配准的相似性度量：'mutual_information'、'mean_squares'、'correlation' 或 'normalized_correlation'",
                "name": "metric",
                "type": "str",
            },
            {
                "default": "gradient_descent",
                "description": "优化方法：'gradient_descent'、'lbfgsb'、'powell' 或 'amoeba'",
                "name": "optimizer",
                "type": "str",
            },
            {
                "default": True,
                "description": "是否预处理图像（去噪和归一化）",
                "name": "preprocess",
                "type": "bool",
            },
            {
                "default": True,
                "description": "是否为每个配准创建可视化图表",
                "name": "create_visualizations",
                "type": "bool",
            },
            {
                "default": 0.01,
                "description": "梯度下降优化器的学习率",
                "name": "learning_rate",
                "type": "float",
            },
            {
                "default": 100,
                "description": "优化迭代的最大次数",
                "name": "number_of_iterations",
                "type": "int",
            },
            {
                "default": 1e-6,
                "description": "优化的收敛容差",
                "name": "gradient_convergence_tolerance",
                "type": "float",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "参考（固定）图像文件的路径",
                "name": "fixed_image_path",
                "type": "str",
            },
            {
                "default": None,
                "description": "包含要配准的多个图像的目录路径（支持 .nii、.nii.gz、.nrrd、.mha、.mhd 格式）",
                "name": "moving_images_dir",
                "type": "str",
            },
            {
                "default": None,
                "description": "保存所有图像配准结果的目录路径",
                "name": "output_dir",
                "type": "str",
            },
        ],
    },
    {
        "description": "计算两个医学图像之间的相似性度量。支持互信息、均方误差、相关性和归一化互相关。",
        "name": "calculate_similarity_metrics",
        "required_parameters": [
            {
                "default": None,
                "description": "第一个图像文件的路径",
                "name": "image1_path",
                "type": "str",
            },
            {
                "default": None,
                "description": "第二个图像文件的路径",
                "name": "image2_path",
                "type": "str",
            },
        ],
    },
    {
        "description": "为配准结果创建可视化图表。生成比较图、差异图像、叠加图和度量图表。",
        "name": "create_registration_visualization",
        "optional_parameters": [
            {
                "default": "registration",
                "description": "输出文件的前缀",
                "name": "prefix",
                "type": "str",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "参考（固定）图像文件的路径",
                "name": "fixed_image_path",
                "type": "str",
            },
            {
                "default": None,
                "description": "原始移动图像文件的路径",
                "name": "moving_image_path",
                "type": "str",
            },
            {
                "default": None,
                "description": "配准后图像文件的路径",
                "name": "registered_image_path",
                "type": "str",
            },
            {
                "default": None,
                "description": "保存可视化文件的目录",
                "name": "output_dir",
                "type": "str",
            },
        ],
    },
]
