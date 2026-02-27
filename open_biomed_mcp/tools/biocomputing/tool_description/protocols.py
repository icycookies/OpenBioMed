description = [
    {
        "description": "在protocols.io中搜索与关键词匹配的公开实验方案",
        "name": "search_protocols",
        "optional_parameters": [],
        "required_parameters": [
            {
                "default": None,
                "description": "要搜索的最重要关键词或短语（标题、描述、作者）",
                "name": "query",
                "type": "str",
            }
        ],
    },
    {
        "description": "通过ID检索protocols.io中特定实验方案的详细元数据",
        "name": "get_protocol_details",
        "optional_parameters": [
            {
                "default": 30,
                "description": "请求超时时间，单位为秒",
                "name": "timeout",
                "type": "int",
            }
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "来自protocols.io的数字实验方案ID",
                "name": "protocol_id",
                "type": "int",
            }
        ],
    },
    {
        "description": "列出本地biomni/tool/protocols/目录中可用的实验方案文件。包括来自Addgene和Thermo Fisher Scientific的实验方案",
        "name": "list_local_protocols",
        "optional_parameters": [
            {
                "default": None,
                "description": "按源目录过滤（例如'addgene'或'thermofisher'）。如果为None，则列出所有实验方案",
                "name": "source",
                "type": "str",
            }
        ],
        "required_parameters": [],
    },
    {
        "description": "从biomni/tool/protocols/读取本地实验方案文件的内容。首先使用list_local_protocols()查找可用的实验方案文件名",
        "name": "read_local_protocol",
        "optional_parameters": [
            {
                "default": None,
                "description": "源目录（例如'addgene'或'thermofisher'）。如果为None，则搜索所有来源",
                "name": "source",
                "type": "str",
            }
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "实验方案文件名（例如'Addgene_ Protocol - How to Run an Agarose Gel.txt'）",
                "name": "filename",
                "type": "str",
            }
        ],
    },
]
