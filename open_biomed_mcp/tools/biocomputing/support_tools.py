import base64
import io
import sys
from io import StringIO

# Create a persistent namespace that will be shared across all executions
_persistent_namespace = {}

# Global list to store captured plots
_captured_plots = []


def run_python_repl(command: str) -> str:
    """在持久环境中执行提供的 Python 命令并返回输出。
    在一次执行中定义的变量将在后续执行中可用。
    """

    def execute_in_repl(command: str) -> str:
        """在持久环境中执行命令的辅助函数。"""
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()

        # Use the persistent namespace
        global _persistent_namespace

        try:
            # Apply matplotlib monkey patches before execution
            _apply_matplotlib_patches()

            # Execute the command in the persistent namespace
            exec(command, _persistent_namespace)
            output = mystdout.getvalue()

            # Capture any matplotlib plots that were generated
            # _capture_matplotlib_plots()

        except Exception as e:
            output = f"Error: {str(e)}"
        finally:
            sys.stdout = old_stdout
        return output

    command = command.strip("```").strip()
    return execute_in_repl(command)


def _capture_matplotlib_plots():
    """捕获在执行期间可能生成的任何 matplotlib 图表。"""
    global _captured_plots
    try:
        import matplotlib.pyplot as plt

        # Check if there are any active figures
        if plt.get_fignums():
            for fig_num in plt.get_fignums():
                fig = plt.figure(fig_num)

                # Save figure to base64
                buffer = io.BytesIO()
                fig.savefig(buffer, format="png", dpi=150, bbox_inches="tight")
                buffer.seek(0)

                # Convert to base64
                image_data = base64.b64encode(buffer.getvalue()).decode("utf-8")
                plot_data = f"data:image/png;base64,{image_data}"

                # Add to captured plots if not already there
                if plot_data not in _captured_plots:
                    _captured_plots.append(plot_data)

                # Close the figure to free memory
                plt.close(fig)

    except ImportError:
        # matplotlib not available
        pass
    except Exception as e:
        print(f"Warning: Could not capture matplotlib plots: {e}")


def _apply_matplotlib_patches():
    """对 matplotlib 函数应用简单的猴子补丁以自动捕获图表。"""
    try:
        import matplotlib.pyplot as plt

        # Only patch if matplotlib is available and not already patched
        if hasattr(plt, "_biomni_patched"):
            return

        # Store original functions
        original_show = plt.show
        original_savefig = plt.savefig

        def show_with_capture(*args, **kwargs):
            """增强的 show 函数，在显示图表之前捕获它们。"""
            # Capture any plots before showing
            _capture_matplotlib_plots()
            # Print a message to indicate plot was generated
            print("Plot generated and displayed")
            # Call the original show function
            return original_show(*args, **kwargs)

        def savefig_with_capture(*args, **kwargs):
            """增强的 savefig 函数，在保存图表后捕获它们。"""
            # Get the filename from args if provided
            filename = args[0] if args else kwargs.get("fname", "unknown")
            # Call the original savefig function
            result = original_savefig(*args, **kwargs)
            # Capture the plot after saving
            _capture_matplotlib_plots()
            # Print a message to indicate plot was saved
            print(f"Plot saved to: {filename}")
            return result

        # Replace functions with enhanced versions
        plt.show = show_with_capture
        plt.savefig = savefig_with_capture

        # Mark as patched to avoid double-patching
        plt._biomni_patched = True

    except ImportError:
        # matplotlib not available
        pass
    except Exception as e:
        print(f"Warning: Could not apply matplotlib patches: {e}")


def get_captured_plots():
    """获取所有捕获的 matplotlib 图表。"""
    global _captured_plots
    return _captured_plots.copy()


def clear_captured_plots():
    """清除所有捕获的 matplotlib 图表。"""
    global _captured_plots
    _captured_plots = []


def read_function_source_code(function_name: str) -> str:
    """从任何模块路径读取函数的源代码。

    参数
    ----------
        function_name (str): 完全限定的函数名称（例如 'bioagentos.tool.support_tools.write_python_code'）

    返回
    -------
        str: 函数的源代码

    """
    import importlib
    import inspect

    # Split the function name into module path and function name
    parts = function_name.split(".")
    module_path = ".".join(parts[:-1])
    func_name = parts[-1]

    try:
        # Import the module
        module = importlib.import_module(module_path)

        # Get the function object from the module
        function = getattr(module, func_name)

        # Get the source code of the function
        source_code = inspect.getsource(function)

        return source_code
    except (ImportError, AttributeError) as e:
        return f"Error: Could not find function '{function_name}'. Details: {str(e)}"


# def request_human_feedback(question, context, reason_for_uncertainty):
#     """
#     Request human feedback on a question.

#     Parameters:
#         question (str): The question that needs human feedback.
#         context (str): Context or details that help the human understand the situation.
#         reason_for_uncertainty (str): Explanation for why the LLM is uncertain about its answer.

#     Returns:
#         str: The feedback provided by the human.
#     """
#     print("Requesting human feedback...")
#     print(f"Question: {question}")
#     print(f"Context: {context}")
#     print(f"Reason for Uncertainty: {reason_for_uncertainty}")

#     # Capture human feedback
#     human_response = input("Please provide your feedback: ")

#     return human_response


def download_synapse_data(
    entity_ids: str | list[str],
    download_location: str = ".",
    follow_link: bool = False,
    recursive: bool = False,
    timeout: int = 300,
    entity_type: str = "dataset",
):
    """使用实体 ID 从 Synapse 下载数据。

    使用 synapse CLI 从 Synapse 下载文件、文件夹或项目。
    需要 SYNAPSE_AUTH_TOKEN 环境变量进行身份验证。
    如果不可用，会自动安装 synapseclient。

    关键提示：始终从 query_synapse() 搜索结果或用户提示中检查实体类型，并传递正确的 entity_type！
    默认的 entity_type="dataset" 可能不适合您的实体。

    重要提示：仅 entity_type="file" 支持多个实体 ID。
    对于数据集、文件夹和项目，仅支持单个 entity_id。

    参数
    ----------
    entity_ids : str or list of str
        要下载的 Synapse 实体 ID。
        - 对于文件：可以是单个 ID 字符串或 ID 字符串列表
        - 对于数据集/文件夹/项目：必须仅为单个 ID 字符串
    download_location : str, 默认 "."
        文件将下载到的目录（默认为当前目录）
    follow_link : bool, 默认 False
        是否跟随链接下载链接的实体
    recursive : bool, 默认 False
        是否递归下载文件夹及其内容
        仅对 entity_type="folder" 有效 - 对其他类型忽略
    timeout : int, 默认 300
        每个下载操作的超时时间（秒）
    entity_type : str, 默认 "dataset"
        Synapse 实体的类型（"dataset"、"file"、"folder"、"project"）
        必须与搜索结果或用户提示中的实际实体类型匹配！
        默认的 "dataset" 应仅用于实际的数据集。
        检查搜索结果中的 'node_type' 字段以确定正确的类型。

    返回
    -------
    dict
        包含下载结果和任何错误的字典

    注意
    -----
    需要 SYNAPSE_AUTH_TOKEN 环境变量，其中包含您的 Synapse 个人
    访问令牌以进行身份验证。

    代理使用指南：
    1. 始终检查 query_synapse() 搜索结果或用户提示中的 'node_type' 字段
    2. 传递与 node_type 匹配的正确 entity_type 参数
    3. 除非确认，否则不要依赖默认的 entity_type="dataset"
    4. 对于多个下载，确保所有实体都是 "file" 类型
    5. 仅对 entity_type="folder" 使用 recursive=True

    示例
    --------
    # 使用 query_synapse() 搜索后，检查 node_type 并使用适当的 entity_type：

    # 如果搜索结果显示 'node_type': 'dataset'
    download_synapse_data("syn123456", entity_type="dataset")

    # 如果搜索结果显示 'node_type': 'file'
    download_synapse_data("syn654321", entity_type="file")

    # 如果搜索结果显示 'node_type': 'folder'
    download_synapse_data("syn789012", entity_type="folder", recursive=True)

    # 多个文件（仅当所有都是 'node_type': 'file' 时）
    download_synapse_data(["syn111", "syn222"], entity_type="file")
    """
    import os
    import subprocess

    # Check for required authentication token
    synapse_token = os.environ.get("SYNAPSE_AUTH_TOKEN")
    if not synapse_token:
        return {
            "success": False,
            "error": "SYNAPSE_AUTH_TOKEN environment variable is required for downloading",
            "suggestion": "Set SYNAPSE_AUTH_TOKEN with your Synapse personal access token",
        }

    # Check if synapse CLI is available
    try:
        subprocess.run(["synapse", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            # Try to install synapseclient
            print("Installing synapseclient...")
            subprocess.run(["pip", "install", "synapseclient"], check=True)
            print("✓ synapseclient installed successfully")
        except subprocess.CalledProcessError as e:
            return {
                "success": False,
                "error": f"Failed to install synapseclient: {e}",
                "suggestion": "Please install manually: pip install synapseclient",
            }

    # Ensure entity_ids is a list
    if isinstance(entity_ids, str):
        entity_ids = [entity_ids]

    # Validate that multiple IDs are only used with file entity type
    if len(entity_ids) > 1 and entity_type != "file":
        return {
            "success": False,
            "error": f"Multiple entity IDs are only supported for entity_type='file'. "
            f"For entity_type='{entity_type}', only a single entity_id is supported.",
            "suggestion": "Use a single entity_id string instead of a list, or change entity_type to 'file'",
        }

    # Validate that recursive is only used with folder entity type
    if recursive and entity_type != "folder":
        return {
            "success": False,
            "error": f"recursive=True is only valid for entity_type='folder'. "
            f"For entity_type='{entity_type}', recursive should be False.",
            "suggestion": "Set recursive=False, or change entity_type to 'folder' if appropriate",
        }

    # Create download directory if it doesn't exist
    os.makedirs(download_location, exist_ok=True)

    results = []
    errors = []

    for entity_id in entity_ids:
        try:
            # Build synapse download command with authentication
            if entity_type == "dataset":
                # For datasets, use query syntax to download the actual files
                cmd = [
                    "synapse",
                    "-p",
                    synapse_token,
                    "get",
                    "-q",
                    f"select * from {entity_id}",
                    "--downloadLocation",
                    download_location,
                ]
            else:
                # For files, folders, projects, use direct ID
                cmd = ["synapse", "-p", synapse_token, "get", entity_id, "--downloadLocation", download_location]

            # Add recursive flag only for folders (validation above ensures recursive is only True for folders)
            if entity_type == "folder" and recursive:
                cmd.append("-r")

            if follow_link:
                cmd.append("--followLink")

            # Execute download
            result = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=timeout)

            results.append(
                {
                    "entity_id": entity_id,
                    "success": True,
                    "stdout": result.stdout,
                    "download_location": download_location,
                }
            )

        except subprocess.CalledProcessError as e:
            error_msg = f"Failed to download {entity_id}: {e.stderr if e.stderr else str(e)}"
            errors.append(error_msg)
            results.append({"entity_id": entity_id, "success": False, "error": error_msg})
        except subprocess.TimeoutExpired:
            error_msg = f"Download timeout for {entity_id} (>{timeout} seconds)"
            errors.append(error_msg)
            results.append({"entity_id": entity_id, "success": False, "error": error_msg})

    # Summary
    successful_downloads = [r for r in results if r["success"]]
    failed_downloads = [r for r in results if not r["success"]]

    return {
        "success": len(failed_downloads) == 0,
        "total_requested": len(entity_ids),
        "successful": len(successful_downloads),
        "failed": len(failed_downloads),
        "download_location": download_location,
        "results": results,
        "errors": errors if errors else None,
    }
