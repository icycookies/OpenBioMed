import importlib
import inspect


class BiocomputingMcp:
    def __init__(self):
        """Initialize BiocomputingMcp with module2api mapping."""
        self.module2api = self.read_module2api()

    def create_mcp_servers_per_module(self):
        """
        为每个模块创建独立的 MCP 服务器。
        
        Returns:
            dict: 字典，键为模块名称，值为对应的 FastMCP 服务器对象
                  格式: {"literature": mcp_server, "biochemistry": mcp_server, ...}
        """
        from mcp.server.fastmcp import FastMCP
        import sys
        import os

        # 确保 chatdd-actions 在 Python 路径中
        current_dir = os.path.dirname(os.path.abspath(__file__))
        chatdd_actions_dir = os.path.dirname(os.path.dirname(current_dir))
        if chatdd_actions_dir not in sys.path:
            sys.path.insert(0, chatdd_actions_dir)

        servers = {}
        total_registered = 0
        failed_modules = []

        # print(f"\n{'='*80}")
        # print(f"🚀 为每个模块创建独立的 MCP 服务器...")
        # print(f"{'='*80}\n")

        for module_name in self.module2api.keys():
            # 提取模块简称（去掉 tools.biocomputing. 前缀）
            module_short_name = module_name.replace("tools.biocomputing.", "")
            
            try:
                # 为每个模块创建独立的 MCP 服务器
                # 服务器名称格式: "Biomni-Literature", "Biomni-Biochemistry" 等
                server_name = f"{module_short_name.title()}"
                mcp = FastMCP(server_name)
                
                # Import the actual module
                module = importlib.import_module(module_name)
                module_tools = self.module2api.get(module_name, [])

                module_registered = 0
                for tool_schema in module_tools:
                    tool_name = tool_schema.get("name")
                    if not tool_name:
                        continue

                    try:
                        # Get the actual function
                        fn = getattr(module, tool_name, None)
                        if fn is None:
                            fn = getattr(self, "_custom_functions", {}).get(tool_name)

                        if fn is None:
                            continue

                        # Extract parameters from your specific schema format
                        required_params = tool_schema.get("required_parameters", [])
                        optional_params = tool_schema.get("optional_parameters", [])
                        description = tool_schema.get("description", "")

                        # Generate the wrapper function
                        wrapper_func = self._generate_mcp_wrapper_from_biocomputing_schema(
                            fn, tool_name, required_params, optional_params, description
                        )

                        # Register with MCP
                        mcp.tool()(wrapper_func)
                        module_registered += 1
                        total_registered += 1

                    except Exception as e:
                        continue
                
                # 将创建的服务器添加到 servers 字典中
                if module_registered > 0:
                    servers[module_short_name] = mcp
                    # print(f" {module_short_name}: 成功注册 {module_registered} 个工具")
                else:
                    pass
                    # print(f" {module_short_name}: 没有工具被注册")

            except ImportError as e:
                failed_modules.append((module_short_name, str(e)))
                # print(f" {module_short_name}: 跳过（缺少依赖）")
                continue
            except Exception as e:
                failed_modules.append((module_short_name, str(e)))
                # print(f" {module_short_name}: 失败 - {e}")
                continue
        
        # 打印总结信息
        # print(f"\n{'='*80}")
        # print(f"   - 成功创建: {len(servers)} 个MCP模块服务器")
        # print(f"   - 总注册工具: {total_registered} 个")
        # print(f"   - 失败模块: {len(failed_modules)} 个")
        # if failed_modules:
        #     print(f"\n失败的模块:")
        #     for mod_name, error in failed_modules:
        #         print(f"   - {mod_name}: {error}")
        # print(f"{'='*80}\n")
  
        return servers

    def _generate_mcp_wrapper_from_biocomputing_schema(self, original_func, func_name, required_params, optional_params, description=""):
        """基于 Biocomputing schema 格式生成包装函数。"""
        # 合并所有参数
        all_params = required_params + optional_params

        if not all_params:
            # 无参数
            def wrapper() -> dict:
                try:
                    result = original_func()
                    if isinstance(result, dict):
                        return result
                    return {"result": result}
                except Exception as e:
                    return {"error": str(e)}

            wrapper.__name__ = func_name
            wrapper.__doc__ = description or original_func.__doc__
            return wrapper

        else:
            # 有参数
            def wrapper(**kwargs) -> dict:
                try:
                    # 构建参数字典
                    filtered_kwargs = {}

                    # 添加必需参数
                    for param_info in required_params:
                        param_name = param_info["name"]
                        if param_name in kwargs and kwargs[param_name] is not None:
                            filtered_kwargs[param_name] = kwargs[param_name]

                    # 仅在提供且不为 None 时添加可选参数
                    for param_info in optional_params:
                        param_name = param_info["name"]
                        if param_name in kwargs and kwargs[param_name] is not None:
                            filtered_kwargs[param_name] = kwargs[param_name]

                    result = original_func(**filtered_kwargs)
                    if isinstance(result, dict):
                        return result
                    return {"result": result}
                except Exception as e:
                    return {"error": str(e)}

            # 设置函数元数据
            wrapper.__name__ = func_name
            wrapper.__doc__ = description or original_func.__doc__

            # 创建正确的函数签名
            new_params = []

            # 将类型字符串映射到 Python 类型
            type_map = {"str": str, "int": int, "float": float, "bool": bool, "List[str]": list[str], "dict": dict}

            # 添加必需参数
            for param_info in required_params:
                param_name = param_info["name"]
                param_type_str = param_info["type"]
                param_type = type_map.get(param_type_str, str)

                new_params.append(inspect.Parameter(param_name, inspect.Parameter.KEYWORD_ONLY, annotation=param_type))

            # 添加可选参数
            for param_info in optional_params:
                param_name = param_info["name"]
                param_type_str = param_info["type"]
                param_type = type_map.get(param_type_str, str)

                # 设置为可选类型
                optional_type = param_type | None

                new_params.append(
                    inspect.Parameter(
                        param_name, inspect.Parameter.KEYWORD_ONLY, default=None, annotation=optional_type
                    )
                )

            # 设置函数签名
            wrapper.__signature__ = inspect.Signature(new_params, return_annotation=dict)

            return wrapper

    def read_module2api(self):
        """从工具描述中读取并构建 module2api 映射。"""
        import sys
        import os
        import importlib.util
        
        # 添加 chatdd-actions 目录到 Python 路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # current_dir 是 chatdd-actions/tools/biomni
        # 我们需要添加 chatdd-actions 到路径
        chatdd_actions_dir = os.path.dirname(os.path.dirname(current_dir))
        if chatdd_actions_dir not in sys.path:
            sys.path.insert(0, chatdd_actions_dir)
            print(f"已添加到 sys.path: {chatdd_actions_dir}")
        
        fields = [
            "literature",
            "biochemistry",
            "bioimaging",
            "bioengineering",
            "biophysics",
            "glycoengineering",
            "cancer_biology",
            "cell_biology",
            "molecular_biology",
            "genetics",
            "immunology",
            "microbiology",
            "pathology",
            "pharmacology",
            "physiology",
            "synthetic_biology",
            "systems_biology",
            "support_tools",
            "lab_automation",
        ]

        module2api = {}
        for field in fields:
            try:
                module_name = f"tools.biocomputing.tool_description.{field}"
                # 先尝试导入，如果失败则打印详细信息
                try:
                    module = importlib.import_module(module_name)
                    if hasattr(module, 'description'):
                        module2api[f"tools.biocomputing.{field}"] = module.description
                    else:
                        print(f"警告: 模块 '{module_name}' 没有 'description' 属性")
                except ModuleNotFoundError as e:
                    # 尝试直接从文件加载
                    tool_desc_dir = os.path.join(current_dir, "tool_description")
                    field_file = os.path.join(tool_desc_dir, f"{field}.py")
                    if os.path.exists(field_file):
                        # 使用 spec 加载模块
                        spec = importlib.util.spec_from_file_location(module_name, field_file)
                        if spec and spec.loader:
                            module = importlib.util.module_from_spec(spec)
                            sys.modules[module_name] = module
                            spec.loader.exec_module(module)
                            if hasattr(module, 'description'):
                                module2api[f"tools.biocomputing.{field}"] = module.description
                            else:
                                print(f"警告: 模块 '{module_name}' 没有 'description' 属性")
                        else:
                            print(f"警告: 无法为 '{field_file}' 创建 spec")
                    else:
                        print(f"警告: 文件未找到: {field_file}")
            except Exception as e:
                print(f"警告: 无法导入模块 '{module_name}': {e}")
                import traceback
                traceback.print_exc()
                continue
        
        # print(f"成功加载 {len(module2api)} 个工具描述模块")
        return module2api


