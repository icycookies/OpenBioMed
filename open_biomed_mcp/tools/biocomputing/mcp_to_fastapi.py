import importlib
import inspect


class BiocomputingMcp:
    def __init__(self):
        """Initialize BiocomputingMcp with module2api mapping."""
        self.module2api = self.read_module2api()

    def create_mcp_servers_per_module(self):
        """
        Create an independent MCP server for each module.
        
        Returns:
            dict: Dictionary where keys are module names and values are the corresponding FastMCP server objects.
                  Format: {"literature": mcp_server, "biochemistry": mcp_server, ...}
        """
        from mcp.server.fastmcp import FastMCP
        import sys
        import os

        # Ensure chatdd-actions is in the Python path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        chatdd_actions_dir = os.path.dirname(os.path.dirname(current_dir))
        if chatdd_actions_dir not in sys.path:
            sys.path.insert(0, chatdd_actions_dir)

        servers = {}
        total_registered = 0
        failed_modules = []

        # print(f"\n{'='*80}")
        # print(f"🚀 Creating independent MCP servers for each module...")
        # print(f"{'='*80}\n")

        for module_name in self.module2api.keys():
            # Extract the short module name (strip the tools.biocomputing. prefix)
            module_short_name = module_name.replace("tools.biocomputing.", "")
            
            try:
                # Create an independent MCP server for each module
                # Server name format: "Biomni-Literature", "Biomni-Biochemistry", etc.
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
                
                # Add the created server to the servers dictionary
                if module_registered > 0:
                    servers[module_short_name] = mcp
                    # print(f" {module_short_name}: Successfully registered {module_registered} tools")
                else:
                    pass
                    # print(f" {module_short_name}: No tools were registered")

            except ImportError as e:
                failed_modules.append((module_short_name, str(e)))
                # print(f" {module_short_name}: Skipped (missing dependencies)")
                continue
            except Exception as e:
                failed_modules.append((module_short_name, str(e)))
                # print(f" {module_short_name}: Failed - {e}")
                continue
        
        # Print summary information
        # print(f"\n{'='*80}")
        # print(f"   - Successfully created: {len(servers)} MCP module servers")
        # print(f"   - Total registered tools: {total_registered}")
        # print(f"   - Failed modules: {len(failed_modules)}")
        # if failed_modules:
        #     print(f"\nFailed modules:")
        #     for mod_name, error in failed_modules:
        #         print(f"   - {mod_name}: {error}")
        # print(f"{'='*80}\n")
  
        return servers

    def _generate_mcp_wrapper_from_biocomputing_schema(self, original_func, func_name, required_params, optional_params, description=""):
        """Generate a wrapper function based on the Biocomputing schema format."""
        # Merge all parameters
        all_params = required_params + optional_params

        if not all_params:
            # No parameters
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
            # Has parameters
            def wrapper(**kwargs) -> dict:
                try:
                    # Build the parameter dictionary
                    filtered_kwargs = {}

                    # Add required parameters
                    for param_info in required_params:
                        param_name = param_info["name"]
                        if param_name in kwargs and kwargs[param_name] is not None:
                            filtered_kwargs[param_name] = kwargs[param_name]

                    # Add optional parameters only when provided and not None
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

            # Set function metadata
            wrapper.__name__ = func_name
            wrapper.__doc__ = description or original_func.__doc__

            # Create the correct function signature
            new_params = []

            # Map type strings to Python types
            type_map = {"str": str, "int": int, "float": float, "bool": bool, "List[str]": list[str], "dict": dict}

            # Add required parameters
            for param_info in required_params:
                param_name = param_info["name"]
                param_type_str = param_info["type"]
                param_type = type_map.get(param_type_str, str)

                new_params.append(inspect.Parameter(param_name, inspect.Parameter.KEYWORD_ONLY, annotation=param_type))

            # Add optional parameters
            for param_info in optional_params:
                param_name = param_info["name"]
                param_type_str = param_info["type"]
                param_type = type_map.get(param_type_str, str)

                # Set as optional type
                optional_type = param_type | None

                new_params.append(
                    inspect.Parameter(
                        param_name, inspect.Parameter.KEYWORD_ONLY, default=None, annotation=optional_type
                    )
                )

            # Set the function signature
            wrapper.__signature__ = inspect.Signature(new_params, return_annotation=dict)

            return wrapper

    def read_module2api(self):
        """Read and build the module2api mapping from tool descriptions."""
        import sys
        import os
        import importlib.util
        
        # Add the chatdd-actions directory to the Python path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # current_dir is chatdd-actions/tools/biomni
        # We need to add chatdd-actions to the path
        chatdd_actions_dir = os.path.dirname(os.path.dirname(current_dir))
        if chatdd_actions_dir not in sys.path:
            sys.path.insert(0, chatdd_actions_dir)
            print(f"Added to sys.path: {chatdd_actions_dir}")
        
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
                # Try importing first; print details if it fails
                try:
                    module = importlib.import_module(module_name)
                    if hasattr(module, 'description'):
                        module2api[f"tools.biocomputing.{field}"] = module.description
                    else:
                        print(f"Warning: module '{module_name}' has no 'description' attribute")
                except ModuleNotFoundError as e:
                    # Try loading directly from file
                    tool_desc_dir = os.path.join(current_dir, "tool_description")
                    field_file = os.path.join(tool_desc_dir, f"{field}.py")
                    if os.path.exists(field_file):
                        # Load the module using spec
                        spec = importlib.util.spec_from_file_location(module_name, field_file)
                        if spec and spec.loader:
                            module = importlib.util.module_from_spec(spec)
                            sys.modules[module_name] = module
                            spec.loader.exec_module(module)
                            if hasattr(module, 'description'):
                                module2api[f"tools.biocomputing.{field}"] = module.description
                            else:
                                print(f"Warning: module '{module_name}' has no 'description' attribute")
                        else:
                            print(f"Warning: unable to create spec for '{field_file}'")
                    else:
                        print(f"Warning: file not found: {field_file}")
            except Exception as e:
                print(f"Warning: unable to import module '{module_name}': {e}")
                import traceback
                traceback.print_exc()
                continue
        
        # print(f"Successfully loaded {len(module2api)} tool description modules")
        return module2api


