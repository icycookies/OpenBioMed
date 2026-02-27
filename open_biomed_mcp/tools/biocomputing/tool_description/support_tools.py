description = [
    {
        "description": "在notebook环境中执行提供的Python命令并返回输出",
        "name": "run_python_repl",
        "optional_parameters": [],
        "required_parameters": [
            {
                "default": None,
                "description": "要在notebook环境中执行的Python命令",
                "name": "command",
                "type": "str",
            }
        ],
    },
    {
        "description": "从任何模块路径读取函数的源代码",
        "name": "read_function_source_code",
        "optional_parameters": [],
        "required_parameters": [
            {
                "default": None,
                "description": "完全限定的函数名（例如'bioagentos.tool.support_tools.write_python_code'）",
                "name": "function_name",
                "type": "str",
            }
        ],
    },
    {
        "description": "使用实体ID从Synapse下载数据。需要SYNAPSE_AUTH_TOKEN环境变量进行身份验证。重要提示：始终根据要下载的内容指定entity_type参数（file、dataset、folder、project）。检查用户提示（如'files'）或搜索结果以确定正确的类型。多个ID仅适用于entity_type='file'。递归下载仅适用于entity_type='folder'",
        "name": "download_synapse_data",
        "optional_parameters": [
            {
                "name": "download_location",
                "type": "str",
                "description": "文件下载的目录",
                "default": ".",
            },
            {
                "name": "follow_link",
                "type": "bool",
                "description": "是否跟随链接下载链接的实体",
                "default": False,
            },
            {
                "name": "recursive",
                "type": "bool",
                "description": "是否递归下载文件夹及其内容。仅对entity_type='folder'有效",
                "default": False,
            },
            {
                "name": "timeout",
                "type": "int",
                "description": "每个下载操作的超时时间，单位为秒",
                "default": 300,
            },
            {
                "name": "entity_type",
                "type": "str",
                "description": "Synapse实体类型：'file'、'dataset'、'folder'或'project'。必须与实际实体类型匹配！检查用户提示（例如'files'表示entity_type='file'）或搜索结果（'node_type'字段）。默认值'dataset'仅应用于实际的数据集",
                "default": "dataset",
            },
        ],
        "required_parameters": [
            {
                "name": "entity_ids",
                "type": "str|list[str]",
                "description": "要下载的Synapse实体ID。对于文件：单个ID或ID列表。对于数据集/文件夹/项目：仅单个ID",
                "default": None,
            }
        ],
    },
]
