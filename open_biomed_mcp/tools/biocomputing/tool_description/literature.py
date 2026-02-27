description = [
    {
        "description": "根据给定的DOI获取论文的补充信息并保存到指定目录。",
        "name": "fetch_supplementary_info_from_doi",
        "optional_parameters": [
            {
                "default": "supplementary_info",
                "description": "保存补充文件的目录",
                "name": "output_dir",
                "type": "str",
            }
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "论文的DOI",
                "name": "doi",
                "type": "str",
            }
        ],
    },
    {
        "description": "根据提供的搜索查询在arXiv中查询论文。",
        "name": "query_arxiv",
        "optional_parameters": [
            {
                "default": 10,
                "description": "要检索的最大论文数量。",
                "name": "max_papers",
                "type": "int",
            }
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "搜索查询字符串。",
                "name": "query",
                "type": "str",
            }
        ],
    },
    {
        "description": "根据提供的搜索查询在Google Scholar中查询论文并返回第一个搜索结果。",
        "name": "query_scholar",
        "optional_parameters": [],
        "required_parameters": [
            {
                "default": None,
                "description": "搜索查询字符串。",
                "name": "query",
                "type": "str",
            }
        ],
    },
    {
        "description": "根据提供的搜索查询在PubMed中查询论文。",
        "name": "query_pubmed",
        "optional_parameters": [
            {
                "default": 10,
                "description": "要检索的最大论文数量。",
                "name": "max_papers",
                "type": "int",
            },
            {
                "default": 3,
                "description": "使用修改后的查询进行重试的最大尝试次数。",
                "name": "max_retries",
                "type": "int",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "搜索查询字符串。",
                "name": "query",
                "type": "str",
            }
        ],
    },
    {
        "description": "使用Google搜索并返回格式化的结果。",
        "name": "search_google",
        "optional_parameters": [
            {
                "default": 3,
                "description": "要返回的结果数量",
                "name": "num_results",
                "type": "int",
            },
            {
                "default": "en",
                "description": "搜索结果的语言代码",
                "name": "language",
                "type": "str",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "搜索查询（例如：'protocol text or search question'）",
                "name": "query",
                "type": "str",
            }
        ],
    },
    {
        "description": "使用requests和BeautifulSoup提取网页的文本内容。",
        "name": "extract_url_content",
        "optional_parameters": [],
        "required_parameters": [
            {
                "default": None,
                "description": "要提取内容的网页URL",
                "name": "url",
                "type": "str",
            }
        ],
    },
    {
        "description": "从PDF文件中提取文本内容。",
        "name": "extract_pdf_content",
        "optional_parameters": [],
        "required_parameters": [
            {
                "default": None,
                "description": "PDF文件的URL",
                "name": "url",
                "type": "str",
            }
        ],
    },
    {
        "description": "启动高级网络搜索，通过启动专门的代理对给定查询进行多轮网络搜索，收集相关信息和引用。",
        "name": "advanced_web_search_claude",
        "optional_parameters": [
            {
                "default": 1,
                "description": "最大搜索次数",
                "name": "max_searches",
                "type": "int",
            },
            {
                "default": 3,
                "description": "使用修改后的查询进行重试的最大尝试次数。",
                "name": "max_retries",
                "type": "int",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "搜索查询字符串。",
                "name": "query",
                "type": "str",
            }
        ],
    },
]
