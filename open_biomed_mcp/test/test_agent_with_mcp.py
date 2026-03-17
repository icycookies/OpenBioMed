#!/usr/bin/env python
"""
Test whether the Agent with MCP tools integrated has the ability to call the corresponding tools
"""

import sys
import os

os.chdir('/home/xiaoxiao/OpenBioMed')
sys.path.insert(0, '/home/xiaoxiao/OpenBioMed')



# Reload modules to use the latest tool definitions
import importlib
import open_biomed.tools.mcp_tools
import open_biomed.tools.tool_registry
import open_biomed.core.agent

importlib.reload(open_biomed.tools.mcp_tools)
importlib.reload(open_biomed.tools.tool_registry)
importlib.reload(open_biomed.core.agent)

from open_biomed.core.agent import PlannerExecutor, SUPPORTED_AGENTS
from open_biomed.utils.config import Config

# Initialize Agent
print("\nInitializing Agent...")
cfg = Config(config_file="configs/agent/planner_executor.yaml")
agent = SUPPORTED_AGENTS[cfg.agent](cfg)

print(f"✓ Agent loaded {len(agent.tools.available_tools())} tools")

# Check tool information in System Prompt
prompt = agent.prompt
if "name: string (required)" in prompt:
    print("✓ System Prompt contains parameter information")
else:
    print("⚠ System Prompt may not contain parameter information")

# Simple test task
print("\n" + "=" * 80)
print("Running test task")
print("=" * 80)

# user_prompt = """
# I need you to systematically analyze the human BRCA1 gene and complete the following tasks:
# 1. Confirm the standard gene information for BRCA1, including Entrez Gene ID, official symbol, full name, and gene description.
# 2. Provide the chromosomal location and genomic interval of BRCA1 in the human genome.
# 3. Summarize the main biological functions of BRCA1 and its functional annotations related to DNA repair and tumor suppression.
# 4. Query the main gene product information for BRCA1, describing its corresponding transcripts or protein product overview.
# 5. Query the ortholog information for BRCA1, providing at least the corresponding mouse homolog gene and its basic information.
# 6. Extract NCBI external link resources or download information related to this gene, such as gene links, dataset report, and download summary.
# """

user_prompt = """
Analyze small molecule inhibitors related to the BRAF target and identify the most representative candidate drugs. Complete the following tasks:
1. Find the target ChEMBL ID corresponding to BRAF.
2. Retrieve small molecule activity data related to BRAF, filtering for compounds with significantly low IC50 or Ki values.
3. Query the molecule information for these highly active compounds.
4. For each compound, further query the mechanism to determine whether it directly acts on BRAF and whether the mode of action is inhibition.
5. Query the drug indication / max phase / drug development status for these molecules (if supported by the tools).
6. Select the 5 most representative candidate molecules and compare them on:
6.1. Activity potency
6.2. Completeness of mechanism annotation
6.3. Clinical development stage
6.4. Basic physicochemical properties
7. Output a ranked report and explain the rationale for the recommendations.
"""


print(f"\nTask: {user_prompt.strip()}")
print("\nStarting execution...")

try:
    thread_id, logs, captured_results = agent.run(user_prompt)
    
    print("\n" + "=" * 80)
    print("Task completed")
    print("=" * 80)
    print(f"Thread ID: {thread_id}")
    print(f"Message count: {len(logs)}")
    
    # Check the last few messages
    print("\nLast messages:")
    for msg in logs[-3:]:
        print(f"\n{msg.type}: {msg.content[:200]}...")
    
    # Export report
    report_path = PlannerExecutor.export_report(logs[-1], thread_id)
    if report_path:
        print(f"\n✓ Report saved: {report_path}")
    else:
        print("\n⚠ No report generated")
        
except Exception as e:
    print(f"\n✗ Execution failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
