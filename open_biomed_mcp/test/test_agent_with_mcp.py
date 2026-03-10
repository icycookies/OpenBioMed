#!/usr/bin/env python
"""
测试 Agent 使用修复后的 MCP 工具
"""

import sys
import os

os.chdir('/home/xiaoxiao/OpenBioMed')
sys.path.insert(0, '/home/xiaoxiao/OpenBioMed')

print("=" * 80)
print("测试 Agent 使用修复后的 MCP 工具")
print("=" * 80)

# 重新加载模块以使用最新的工具定义
import importlib
import open_biomed.tools.mcp_tools
import open_biomed.tools.tool_registry
import open_biomed.core.agent

importlib.reload(open_biomed.tools.mcp_tools)
importlib.reload(open_biomed.tools.tool_registry)
importlib.reload(open_biomed.core.agent)

from open_biomed.core.agent import PlannerExecutor, SUPPORTED_AGENTS
from open_biomed.utils.config import Config

# 初始化 Agent
print("\n初始化 Agent...")
cfg = Config(config_file="configs/agent/planner_executor.yaml")
agent = SUPPORTED_AGENTS[cfg.agent](cfg)

print(f"✓ Agent 已加载 {len(agent.tools.available_tools())} 个工具")

# 检查 System Prompt 中的工具信息
prompt = agent.prompt
if "name: string (required)" in prompt:
    print("✓ System Prompt 包含参数信息")
else:
    print("⚠ System Prompt 可能没有参数信息")

# 简单的测试任务
print("\n" + "=" * 80)
print("运行测试任务")
print("=" * 80)

user_prompt = """
我现在需要你帮我对人类 BRCA1 基因进行系统分析，并完成以下任务：
1、确认 BRCA1 的标准基因信息，包括 Entrez Gene ID、官方符号、全名和基因描述。
2、给出 BRCA1 在人类基因组中的染色体位置与基因组区间。
3、总结 BRCA1 的主要生物学功能，以及它与 DNA 修复、肿瘤抑制相关的功能注释。
4、查询 BRCA1 的主要基因产物信息，说明其对应的转录本或蛋白产物概况。
5、查询 BRCA1 的 ortholog 信息，至少给出小鼠对应同源基因及其基本信息。
6、提取与该基因相关的 NCBI 外部链接资源或下载信息，例如 gene links、dataset report、download summary。
"""

print(f"\n任务: {user_prompt.strip()}")
print("\n开始执行...")

try:
    thread_id, logs, captured_results = agent.run(user_prompt)
    
    print("\n" + "=" * 80)
    print("任务完成")
    print("=" * 80)
    print(f"Thread ID: {thread_id}")
    print(f"消息数: {len(logs)}")
    
    # 检查最后几条消息
    print("\n最后的消息:")
    for msg in logs[-3:]:
        print(f"\n{msg.type}: {msg.content[:200]}...")
    
    # 导出报告
    report_path = PlannerExecutor.export_report(logs[-1], thread_id)
    if report_path:
        print(f"\n✓ 报告已保存: {report_path}")
    else:
        print("\n⚠ 未生成报告")
        
except Exception as e:
    print(f"\n✗ 执行失败: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
