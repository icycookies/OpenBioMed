description = [
    {
        "description": "基于脚本内容测试PyLabRobot脚本。",
        "name": "test_pylabrobot_script",
        "optional_parameters": [
            {
                "default": False,
                "description": "如果为True，启用脚本执行的跟踪功能",
                "name": "enable_tracking",
                "type": "bool",
            },
            {
                "default": 60,
                "description": "脚本执行的超时时间（秒）",
                "name": "timeout_seconds",
                "type": "int",
            },
            {
                "default": False,
                "description": "如果为True，将测试结果保存为.json文件",
                "name": "save_test_report",
                "type": "bool",
            },
            {
                "default": None,
                "description": "保存测试结果的目录。如果提供，测试结果将作为.json文件保存在此目录中",
                "name": "test_report_dir",
                "type": "str",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "要测试的脚本内容",
                "name": "script_input",
                "type": "str",
            }
        ],
    },
    {
        "description": "获取PyLabRobot教程中液体处理部分的文档。",
        "name": "get_pylabrobot_documentation_liquid",
        "optional_parameters": [],
        "required_parameters": [],
    },
    {
        "description": "获取PyLabRobot教程中材料处理部分的文档。",
        "name": "get_pylabrobot_documentation_material",
        "optional_parameters": [],
        "required_parameters": [],
    },
]
