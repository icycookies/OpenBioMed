# OpenBioMed MCP Tools Quick Start Guide

This guide walks you through the complete process of configuring and testing the OpenBioMed Agent with MCP tools from scratch.

---

## Table of Contents

1. [Environment Setup](#1-environment-setup)
2. [Configure MCP Service](#2-configure-mcp-service)
3. [Start MCP Service](#3-start-mcp-service)
4. [Configure Agent MCP Connection](#4-configure-agent-mcp-connection)
5. [Run Tests](#5-run-tests)
6. [Verify Results](#6-verify-results)
7. [Troubleshooting](#7-troubleshooting)

---

## 1. Environment Setup

### 1.1 System Requirements

- Python 3.11+
- Conda (recommended) or virtualenv
- At least 4GB available memory
- Stable network connection (for accessing external APIs)

### 1.2 Create Python Environment

```bash
# Navigate to the project root
cd /home/yourName/OpenBioMed

# Create conda environment for OpenBioMed (Python 3.9 recommended)
conda create -n openbiomed python=3.9.7
conda activate openbiomed

# Create conda environment for OpenBioMed_MCP (Python 3.11 recommended)
conda create -n openbiomed_mcp python=3.11
conda activate openbiomed_mcp

# Or use virtualenv
# python3.11 -m venv venv
# source venv/bin/activate
```

### 1.3 Install Dependencies

#### Install OpenBioMed main project dependencies

```bash
# In the OpenBioMed root directory
conda activate openbiomed
pip install -r requirements.txt
```

#### Install MCP service dependencies

```bash
# Navigate to the MCP service directory
cd open_biomed_mcp

# Install MCP service dependencies
conda activate openbiomed_mcp
pip install -r requirements.txt
```

**Key dependencies**:
- `fastapi`: Web framework
- `uvicorn`: ASGI server
- `httpx`: HTTP client (used by Agent to call MCP service)
- `nest_asyncio`: Async event loop support
- `langchain`: LLM framework
- `langgraph`: Agent workflow framework

### 1.4 Configure API Keys

Edit the `open_biomed_mcp/.env` file to set the required API keys:

```bash
cd /home/xiaoxiao/OpenBioMed/open_biomed_mcp
nano .env  # or use your preferred editor
```

Example `.env` file content:

```env
# Search engine API keys (optional, not required if not using search tools)
tavily_api_key = "your_tavily_api_key_here"
jina_api_key = "your_jina_api_key_here"
```

**Notes**:
- If you only test database tools like NCBI or PubChem, these API keys are not required
- If you need search tools, apply for API keys on the respective websites

### 1.5 Configure LLM API Keys

Edit the `.env` file in the OpenBioMed main project:

```bash
cd /home/xiaoxiao/OpenBioMed
nano .env
```

Add your LLM API key (choose based on the model you use):

```env
# DeepSeek API (recommended, cost-effective)
DEEPSEEK_API_KEY=your_deepseek_api_key
DEEPSEEK_API_URL=https://api.deepseek.com

# Or OpenAI API
# OPENAI_API_KEY=your_openai_api_key
# OPENAI_API_URL=https://api.openai.com/v1

# Or Anthropic Claude API
# ANTHROPIC_API_KEY=your_anthropic_api_key
# ANTHROPIC_API_URL=https://api.anthropic.com
```

---

## 2. Configure MCP Service

The MCP service is pre-configured and requires no additional setup. Key file locations for reference:

- **Main config**: `open_biomed_mcp/main.py`
- **Tool registry**: `open_biomed_mcp/registry.py`
- **Tool modules**: `open_biomed_mcp/tools/`

### 2.1 Available MCP Endpoints

The MCP service provides multiple endpoints:

- **Global endpoint** (all tools): `http://localhost:8086/mcp`
- **NCBI endpoint** (56 gene database tools): `http://localhost:8086/ncbi/mcp`
- **PubChem endpoint** (39 compound tools): `http://localhost:8086/pubchem/mcp`
- **UniProt endpoint** (22 protein tools): `http://localhost:8086/uniprot/mcp`
- **STRING endpoint** (8 protein network tools): `http://localhost:8086/string/mcp`
- **ChEMBL endpoint** (101 bioactivity tools): `http://localhost:8086/chembl/mcp`

See `README.md` for the full list of endpoints.

---

## 3. Start MCP Service

### 3.1 Start the Service

Open a new terminal window (keep it running):

```bash
# Activate environment
conda activate openbiomed_mcp

# Navigate to MCP service directory
cd /home/xiaoxiao/OpenBioMed/open_biomed_mcp

# Start service on port 8086
uvicorn main:app --host 0.0.0.0 --port 8086 --reload
```

**Startup parameter notes**:
- `--host 0.0.0.0`: Allow external access (use 127.0.0.1 for local-only)
- `--port 8086`: Use port 8086 (matches mcp.json configuration)
- `--reload`: Development mode, auto-restarts on code changes

### 3.2 Verify Service Startup

After startup, you should see output like:

```
INFO:     Uvicorn running on http://0.0.0.0:8086 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 3.3 Test the Service

Use a browser or curl to verify:

```bash
# Health check
curl http://localhost:8086/healthz
# Expected: {"status": "healthy"}

# View tools summary
curl http://localhost:8086/tools/summary
# Expected: JSON with all servers and tool counts

# View API docs (open in browser)
http://localhost:8086/docs
```

**Important**: Keep this terminal window running. The MCP service must stay active.

---

## 4. Configure Agent MCP Connection

### 4.1 Create MCP Configuration File

In the OpenBioMed root directory:

```bash
cd /home/xiaoxiao/OpenBioMed

# Create config directory if it doesn't exist
mkdir -p .kiro/settings

# Create or edit mcp.json
nano .kiro/settings/mcp.json
```

### 4.2 Configuration Options

Choose a configuration based on your needs:

#### Option A: NCBI tools only (recommended for beginners)

```json
{
  "mcpServers": {
    "ncbi": {
      "comment": "NCBI gene database tools (56 tools)",
      "url": "http://localhost:8086/ncbi/mcp",
      "timeout": 60,
      "verify_ssl": false,
      "disabled": false
    }
  }
}
```

#### Option B: Multiple database tools

```json
{
  "mcpServers": {
    "ncbi": {
      "comment": "NCBI gene database tools (56 tools)",
      "url": "http://localhost:8086/ncbi/mcp",
      "timeout": 60,
      "verify_ssl": false,
      "disabled": false
    },
    "pubchem": {
      "comment": "PubChem compound database tools (39 tools)",
      "url": "http://localhost:8086/pubchem/mcp",
      "timeout": 60,
      "verify_ssl": false,
      "disabled": false
    },
    "uniprot": {
      "comment": "UniProt protein database tools (22 tools)",
      "url": "http://localhost:8086/uniprot/mcp",
      "timeout": 60,
      "verify_ssl": false,
      "disabled": false
    },
    "string": {
      "comment": "STRING protein network tools (8 tools)",
      "url": "http://localhost:8086/string/mcp",
      "timeout": 60,
      "verify_ssl": false,
      "disabled": false
    }
  }
}
```

#### Option C: All tools (not recommended — too many tools may degrade LLM performance)

```json
{
  "mcpServers": {
    "biomed-all": {
      "comment": "All OpenBioMed MCP tools",
      "url": "http://localhost:8086/mcp",
      "timeout": 60,
      "verify_ssl": false,
      "disabled": false
    }
  }
}
```

**Configuration notes**:
- `url`: MCP service endpoint address
- `timeout`: Tool call timeout in seconds
- `verify_ssl`: Whether to verify SSL certificate (set to false for local testing)
- `disabled`: Whether to disable this server (true = disabled, false = enabled)

### 4.3 Verify Configuration File

```bash
# Check if the config file exists
ls -la /home/xiaoxiao/OpenBioMed/.kiro/settings/mcp.json

# View config content
cat /home/xiaoxiao/OpenBioMed/.kiro/settings/mcp.json
```

---

## 5. Run Tests

### 5.1 Open a New Terminal

Keep the MCP service running and open a new terminal window.

### 5.2 Activate Environment and Navigate to Test Directory

```bash
# Activate environment
conda activate openbiomed

# Navigate to test directory
cd /home/xiaoxiao/OpenBioMed/open_biomed_mcp/test
```

### 5.3 Review the Test File

```bash
cat test_agent_with_mcp.py
```

The test file contains two example tasks:
1. **BRCA1 gene systematic analysis** (commented out)
2. **BRAF target small molecule inhibitor analysis** (currently active)

### 5.4 Run the Test

```bash
python test_agent_with_mcp.py
```

### 5.5 Observe the Output

During the test run, you will see:

```
Initializing Agent...
✓ Agent loaded 88 tools
✓ System Prompt contains parameter information

================================================================================
Running test task
================================================================================

Task: Analyze small molecule inhibitors related to the BRAF target...

Starting execution...

AI Message
I will help you analyze BRAF target-related small molecule inhibitors...

Plan:
1. [ ] Find the target ChEMBL ID for BRAF
2. [ ] Retrieve small molecule activity data related to BRAF
...

<execute>
from open_biomed.tools.tool_registry import TOOLS
tool = TOOLS["search_chembl_target"]
result, messages = tool.run(query="BRAF")
print(result)
</execute>

Tool Message
Code execution succeeded.
The stdout is:
...
```

**Execution process**:
- The Agent automatically generates an execution plan
- Calls MCP tools step by step
- Displays the result of each step
- Generates a final analysis report

### 5.6 Wait for Completion

The test may take a few minutes depending on:
- LLM response speed
- Number of MCP tool calls
- Network conditions

---

## 6. Verify Results

### 6.1 Check Terminal Output

After the test completes, you will see:

```
================================================================================
Task completed
================================================================================
Thread ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
Message count: XX

Last messages:
...

✓ Report saved: /home/xiaoxiao/OpenBioMed/tmp/planner_executor-xxxxx/report.md
```

### 6.2 View the Generated Report

```bash
# Find the report directory
ls -la /home/xiaoxiao/OpenBioMed/tmp/

# View the latest report
cd /home/xiaoxiao/OpenBioMed/tmp/planner_executor-xxxxx/
cat report.md
```

The report should include:
- Task execution steps
- Tool call results
- Data analysis
- Final conclusions

### 6.3 Verify MCP Tool Calls

Check the MCP service terminal output — you should see entries like:

```
INFO:     127.0.0.1:xxxxx - "POST /tools/chembl/search_chembl_target HTTP/1.1" 200 OK
INFO:     127.0.0.1:xxxxx - "POST /tools/chembl/get_activity HTTP/1.1" 200 OK
...
```

This confirms the Agent successfully called the MCP tools.

---

## 7. Troubleshooting

### 7.1 MCP Service Fails to Start

**Issue**: `uvicorn: command not found`

**Fix**:
```bash
pip install uvicorn
```

**Issue**: `Address already in use`

**Fix**:
```bash
# Find the process using port 8086
lsof -i :8086

# Kill the process
kill -9 <PID>

# Or use a different port
uvicorn main:app --host 0.0.0.0 --port 8087 --reload
# Remember to update the port in mcp.json as well
```

### 7.2 Agent Cannot Load MCP Tools

**Issue**: `Warning: No MCP configuration file found`

**Fix**:
```bash
# Check the config file path
ls -la /home/xiaoxiao/OpenBioMed/.kiro/settings/mcp.json

# If it doesn't exist, create it (see section 4.2)
```

**Issue**: `Failed to load tools from ncbi: Connection refused`

**Fix**:
1. Confirm the MCP service is running
2. Check that the port number is correct (8086)
3. Verify the URL format is correct

### 7.3 Tool Call Failures

**Issue**: `Tool execution failed: timeout`

**Fix**:
```json
// Increase timeout in mcp.json
{
  "mcpServers": {
    "ncbi": {
      "url": "http://localhost:8086/ncbi/mcp",
      "timeout": 120,
      ...
    }
  }
}
```

**Issue**: `KeyError: 'ncbi_get_gene_metadata_by_gene_name'`

**Fix**:
```bash
# Restart the Python process to reload tools
# Or add module reloading in code (test_agent_with_mcp.py already includes this)
```

### 7.4 LLM API Errors

**Issue**: `API key not found`

**Fix**:
```bash
# Check the .env file
cat /home/xiaoxiao/OpenBioMed/.env

# Ensure the API key is configured
```

**Issue**: `Rate limit exceeded`

**Fix**:
- Wait a moment and retry
- Or switch to a different LLM service

### 7.5 Slow Test Execution

**Causes**:
- LLM response generation takes time
- MCP tool calls to external APIs take time
- Network latency

**Optimization tips**:
1. Use a faster LLM (e.g., DeepSeek)
2. Reduce task complexity
3. Only enable the MCP tools you need

---

## 8. Modify Test Tasks

### 8.1 Edit the Test File

```bash
cd /home/xiaoxiao/OpenBioMed/open_biomed_mcp/test
nano test_agent_with_mcp.py
```

### 8.2 Change the Task Content

Find the `user_prompt` variable and replace it with your desired task:

```python
# Simple gene query task
user_prompt = """
Query basic information about the human BRCA1 gene, including:
1. Gene ID
2. Chromosomal location
3. Gene description
"""

# Or compound query task
user_prompt = """
Search for compound information on aspirin, including:
1. PubChem CID
2. Molecular formula
3. Molecular weight
4. SMILES structure
"""
```

### 8.3 Re-run the Test

```bash
python test_agent_with_mcp.py
```

---

## 9. Next Steps

### 9.1 Explore More Tools

View available tools:

```bash
# Open API docs in browser
# http://localhost:8086/docs

# Or read README.md for all tools
cat /home/xiaoxiao/OpenBioMed/open_biomed_mcp/README.md
```

### 9.2 Build Your Own Agent Application

Use `test_agent_with_mcp.py` as a reference to create your own Agent application.

### 9.3 Integrate into Other Projects

The MCP service can be called by any HTTP-capable client, not just the OpenBioMed Agent.

---

## 10. Quick Command Reference

```bash
# 1. Start MCP service (Terminal 1)
cd /home/xiaoxiao/OpenBioMed/open_biomed_mcp
conda activate openbiomed_mcp
uvicorn main:app --host 0.0.0.0 --port 8086 --reload

# 2. Run test (Terminal 2)
cd /home/xiaoxiao/OpenBioMed/open_biomed_mcp/test
conda activate openbiomed
python test_agent_with_mcp.py

# 3. View report
ls -la /home/xiaoxiao/OpenBioMed/tmp/
cat /home/xiaoxiao/OpenBioMed/tmp/planner_executor-xxxxx/report.md

# 4. Stop MCP service
# Press Ctrl+C in the MCP service terminal
```

---

## 11. Getting Help

If you encounter issues:

1. Check the Troubleshooting section in this document
2. Review the MCP service log output
3. Check the Agent error messages
4. Verify configuration files are correct
5. Confirm all dependencies are installed

---

## Appendix: Complete Startup Checklist

- [ ] Python 3.11+ installed
- [ ] Conda environment created and activated
- [ ] OpenBioMed dependencies installed
- [ ] MCP service dependencies installed
- [ ] .env file configured (API keys)
- [ ] MCP service started (port 8086)
- [ ] MCP service health check passed
- [ ] mcp.json configuration file created
- [ ] URL and port in mcp.json are correct
- [ ] Test file is accessible
- [ ] Test task selected

Once all items are checked, run `python test_agent_with_mcp.py` to start testing!

---

**Good luck with your testing!** 🎉
