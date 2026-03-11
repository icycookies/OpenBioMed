# OpenBioMed接入MCP工具快速启动指南

本文档将指导你从零开始配置和测试OpenBioMed Agent接入MCP工具的完整流程。

---

## 目录

1. [环境准备](#1-环境准备)
2. [配置MCP服务](#2-配置mcp服务)
3. [启动MCP服务](#3-启动mcp服务)
4. [配置Agent的MCP连接](#4-配置agent的mcp连接)
5. [运行测试](#5-运行测试)
6. [验证结果](#6-验证结果)
7. [常见问题](#7-常见问题)

---

## 1. 环境准备

### 1.1 系统要求

- Python 3.11+
- Conda（推荐）或 virtualenv
- 至少 4GB 可用内存
- 稳定的网络连接（用于访问外部API）

### 1.2 创建Python环境

```bash
# 进入项目根目录
cd /home/yourName/OpenBioMed

# 创建OpenBioMed的conda环境（推荐Python 3.9）
conda create -n openbiomed python=3.9.7
conda activate openbiomed

# 创建OpenBioMed_MCP的conda环境（推荐Python 3.11）
conda create -n openbiomed_mcp python=3.11
conda activate openbiomed_mcp

# 或使用virtualenv
# python3.11 -m venv venv
# source venv/bin/activate
```

### 1.3 安装依赖

#### 安装OpenBioMed主项目依赖

```bash
# 在OpenBioMed根目录
conda activate openbiomed
pip install -r requirements.txt
```

#### 安装MCP服务依赖

```bash
# 进入MCP服务目录
cd open_biomed_mcp

# 安装MCP服务依赖
conda activate openbiomed_mcp
pip install -r requirements.txt
```

**重要依赖说明**:
- `fastapi`: Web框架
- `uvicorn`: ASGI服务器
- `httpx`: HTTP客户端（用于Agent调用MCP服务）
- `nest_asyncio`: 异步事件循环支持
- `langchain`: LLM框架
- `langgraph`: Agent工作流框架

### 1.4 配置API密钥

编辑 `open_biomed_mcp/.env` 文件，配置必要的API密钥：

```bash
cd /home/xiaoxiao/OpenBioMed/open_biomed_mcp
nano .env  # 或使用你喜欢的编辑器
```

`.env` 文件内容示例：

```env
# 搜索引擎API密钥（可选，如果不使用搜索工具可以不配置）
tavily_api_key = "your_tavily_api_key_here"
jina_api_key = "your_jina_api_key_here"
```

**注意**: 
- 如果只测试NCBI、PubChem等数据库工具，可以不配置这些API密钥
- 如果需要使用搜索工具，请到相应网站申请API密钥

### 1.5 配置LLM API密钥

编辑OpenBioMed主项目的 `.env` 文件：

```bash
cd /home/xiaoxiao/OpenBioMed
nano .env
```

添加你的LLM API密钥（根据使用的模型选择）：

```env
# DeepSeek API（推荐，性价比高）
DEEPSEEK_API_KEY=your_deepseek_api_key
DEEPSEEK_API_URL=https://api.deepseek.com

# 或 OpenAI API
# OPENAI_API_KEY=your_openai_api_key
# OPENAI_API_URL=https://api.openai.com/v1

# 或 Anthropic Claude API
# ANTHROPIC_API_KEY=your_anthropic_api_key
# ANTHROPIC_API_URL=https://api.anthropic.com
```

---

## 2. 配置MCP服务

MCP服务已经配置好，无需额外配置。但你可以了解配置文件的位置：

- **主配置文件**: `open_biomed_mcp/main.py`
- **工具注册**: `open_biomed_mcp/registry.py`
- **工具模块**: `open_biomed_mcp/tools/`

### 2.1 查看可用的MCP端点

MCP服务提供了多个端点，你可以选择使用：

- **全局端点**（包含所有工具）: `http://localhost:8086/mcp`
- **NCBI端点**（56个基因数据库工具）: `http://localhost:8086/ncbi/mcp`
- **PubChem端点**（39个化合物工具）: `http://localhost:8086/pubchem/mcp`
- **UniProt端点**（22个蛋白质工具）: `http://localhost:8086/uniprot/mcp`
- **STRING端点**（8个蛋白质网络工具）: `http://localhost:8086/string/mcp`
- **ChEMBL端点**（101个生物活性工具）: `http://localhost:8086/chembl/mcp`

更多端点请参考 `README.md`。

---

## 3. 启动MCP服务

### 3.1 启动服务

打开一个新的终端窗口（保持这个窗口运行）：

```bash
# 激活环境
conda activate openbiomed_mcp

# 进入MCP服务目录
cd /home/xiaoxiao/OpenBioMed/open_biomed_mcp

# 启动服务（使用8086端口）
uvicorn main:app --host 0.0.0.0 --port 8086 --reload
```

**启动参数说明**:
- `--host 0.0.0.0`: 允许外部访问（如果只本地测试可以用127.0.0.1）
- `--port 8086`: 使用8086端口（与mcp.json配置一致）
- `--reload`: 开发模式，代码修改后自动重启

### 3.2 验证服务启动

服务启动后，你应该看到类似输出：

```
INFO:     Uvicorn running on http://0.0.0.0:8086 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 3.3 测试服务是否正常

打开浏览器或使用curl测试：

```bash
# 测试健康检查
curl http://localhost:8086/healthz

# 应该返回: {"status": "healthy"}

# 查看工具摘要
curl http://localhost:8086/tools/summary

# 应该返回包含所有服务器和工具数量的JSON

# 查看API文档（在浏览器中打开）
http://localhost:8086/docs
```

**重要**: 保持这个终端窗口运行，不要关闭！MCP服务需要持续运行。

---

## 4. 配置Agent的MCP连接

### 4.1 创建MCP配置文件

在OpenBioMed根目录创建MCP配置：

```bash
cd /home/xiaoxiao/OpenBioMed

# 创建配置目录（如果不存在）
mkdir -p .kiro/settings

# 创建或编辑mcp.json
nano .kiro/settings/mcp.json
```

### 4.2 配置文件内容

根据你的需求选择配置方案：

#### 方案A: 只使用NCBI工具（推荐新手）

```json
{
  "mcpServers": {
    "ncbi": {
      "comment": "NCBI 基因数据库工具（56个工具）",
      "url": "http://localhost:8086/ncbi/mcp",
      "timeout": 60,
      "verify_ssl": false,
      "disabled": false
    }
  }
}
```

#### 方案B: 使用多个数据库工具

```json
{
  "mcpServers": {
    "ncbi": {
      "comment": "NCBI 基因数据库工具（56个工具）",
      "url": "http://localhost:8086/ncbi/mcp",
      "timeout": 60,
      "verify_ssl": false,
      "disabled": false
    },
    "pubchem": {
      "comment": "PubChem 化合物数据库工具（39个工具）",
      "url": "http://localhost:8086/pubchem/mcp",
      "timeout": 60,
      "verify_ssl": false,
      "disabled": false
    },
    "uniprot": {
      "comment": "UniProt 蛋白质数据库工具（22个工具）",
      "url": "http://localhost:8086/uniprot/mcp",
      "timeout": 60,
      "verify_ssl": false,
      "disabled": false
    },
    "string": {
      "comment": "STRING 蛋白质网络工具（8个工具）",
      "url": "http://localhost:8086/string/mcp",
      "timeout": 60,
      "verify_ssl": false,
      "disabled": false
    }
  }
}
```

#### 方案C: 使用所有工具（不推荐，工具太多可能影响LLM性能）

```json
{
  "mcpServers": {
    "biomed-all": {
      "comment": "所有 OpenBioMed MCP 工具",
      "url": "http://localhost:8086/mcp",
      "timeout": 60,
      "verify_ssl": false,
      "disabled": false
    }
  }
}
```

**配置说明**:
- `url`: MCP服务的端点地址
- `timeout`: 工具调用超时时间（秒）
- `verify_ssl`: 是否验证SSL证书（本地测试设为false）
- `disabled`: 是否禁用该服务器（true=禁用，false=启用）

### 4.3 验证配置文件

```bash
# 检查配置文件是否存在
ls -la /home/xiaoxiao/OpenBioMed/.kiro/settings/mcp.json

# 查看配置内容
cat /home/xiaoxiao/OpenBioMed/.kiro/settings/mcp.json
```

---

## 5. 运行测试

### 5.1 打开新终端

保持MCP服务运行，打开一个新的终端窗口。

### 5.2 激活环境并进入测试目录

```bash
# 激活环境
conda activate openbiomed

# 进入测试目录
cd /home/xiaoxiao/OpenBioMed/open_biomed_mcp/test
```

### 5.3 查看测试文件

```bash
# 查看测试文件内容
cat test_agent_with_mcp.py
```

测试文件包含两个示例任务：
1. **BRCA1基因系统分析**（已注释）
2. **BRAF靶点小分子抑制剂分析**（当前启用）

### 5.4 运行测试

```bash
# 运行测试
python test_agent_with_mcp.py
```

### 5.5 观察输出

测试运行时，你会看到：

```
初始化 Agent...
✓ Agent 已加载 88 个工具
✓ System Prompt 包含参数信息

================================================================================
运行测试任务
================================================================================

任务: 对 BRAF 靶点相关的小分子抑制剂进行分析...

开始执行...

AI Message
我将帮你分析BRAF靶点相关的小分子抑制剂...

计划：
1. [ ] 找到 BRAF 对应的 target ChEMBL ID
2. [ ] 检索 BRAF 相关的小分子活性数据
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

**执行过程说明**:
- Agent会自动生成执行计划
- 逐步调用MCP工具
- 显示每一步的执行结果
- 最终生成分析报告

### 5.6 等待完成

测试可能需要几分钟时间，取决于：
- LLM响应速度
- MCP工具调用次数
- 网络状况

---

## 6. 验证结果

### 6.1 查看终端输出

测试完成后，你会看到：

```
================================================================================
任务完成
================================================================================
Thread ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
消息数: XX

最后的消息:
...

✓ 报告已保存: /home/xiaoxiao/OpenBioMed/tmp/planner_executor-xxxxx/report.md
```

### 6.2 查看生成的报告

```bash
# 找到报告目录
ls -la /home/xiaoxiao/OpenBioMed/tmp/

# 查看最新的报告
cd /home/xiaoxiao/OpenBioMed/tmp/planner_executor-xxxxx/
cat report.md
```

报告应该包含：
- 任务执行步骤
- 工具调用结果
- 数据分析
- 最终结论

### 6.3 验证MCP工具调用

检查MCP服务的终端输出，你应该看到类似：

```
INFO:     127.0.0.1:xxxxx - "POST /tools/chembl/search_chembl_target HTTP/1.1" 200 OK
INFO:     127.0.0.1:xxxxx - "POST /tools/chembl/get_activity HTTP/1.1" 200 OK
...
```

这表示Agent成功调用了MCP工具。

---

## 7. 常见问题

### 7.1 MCP服务无法启动

**问题**: `uvicorn: command not found`

**解决**:
```bash
pip install uvicorn
```

**问题**: `Address already in use`

**解决**:
```bash
# 查找占用8086端口的进程
lsof -i :8086

# 杀死进程
kill -9 <PID>

# 或使用其他端口
uvicorn main:app --host 0.0.0.0 --port 8087 --reload
# 记得同时修改mcp.json中的端口号
```

### 7.2 Agent无法加载MCP工具

**问题**: `Warning: No MCP configuration file found`

**解决**:
```bash
# 检查配置文件路径
ls -la /home/xiaoxiao/OpenBioMed/.kiro/settings/mcp.json

# 如果不存在，创建配置文件（参考步骤4.2）
```

**问题**: `Failed to load tools from ncbi: Connection refused`

**解决**:
1. 确认MCP服务正在运行
2. 检查端口号是否正确（8086）
3. 检查URL格式是否正确

### 7.3 工具调用失败

**问题**: `Tool execution failed: timeout`

**解决**:
```json
// 在mcp.json中增加timeout
{
  "mcpServers": {
    "ncbi": {
      "url": "http://localhost:8086/ncbi/mcp",
      "timeout": 120,  // 增加到120秒
      ...
    }
  }
}
```

**问题**: `KeyError: 'ncbi_get_gene_metadata_by_gene_name'`

**解决**:
```bash
# 重启Python进程以重新加载工具
# 或在代码中添加模块重载（test_agent_with_mcp.py已包含）
```

### 7.4 LLM API错误

**问题**: `API key not found`

**解决**:
```bash
# 检查.env文件
cat /home/xiaoxiao/OpenBioMed/.env

# 确保API密钥已配置
```

**问题**: `Rate limit exceeded`

**解决**:
- 等待一段时间后重试
- 或使用其他LLM服务

### 7.5 测试运行缓慢

**原因**: 
- LLM生成响应需要时间
- MCP工具调用外部API需要时间
- 网络延迟

**优化建议**:
1. 使用更快的LLM（如DeepSeek）
2. 减少任务复杂度
3. 只启用必要的MCP工具

---

## 8. 修改测试任务

### 8.1 编辑测试文件

```bash
cd /home/xiaoxiao/OpenBioMed/open_biomed_mcp/test
nano test_agent_with_mcp.py
```

### 8.2 修改任务内容

找到 `user_prompt` 变量，修改为你想测试的任务：

```python
# 简单的基因查询任务
user_prompt = """
查询人类BRCA1基因的基本信息，包括：
1. 基因ID
2. 染色体位置
3. 基因描述
"""

# 或化合物查询任务
user_prompt = """
搜索阿司匹林（aspirin）的化合物信息，包括：
1. PubChem CID
2. 分子式
3. 分子量
4. SMILES结构
"""
```

### 8.3 重新运行测试

```bash
python test_agent_with_mcp.py
```

---

## 9. 下一步

### 9.1 探索更多工具

查看可用的工具：

```bash
# 在浏览器中打开API文档
# http://localhost:8086/docs

# 或查看README.md了解所有工具
cat /home/xiaoxiao/OpenBioMed/open_biomed_mcp/README.md
```

### 9.2 开发自己的Agent应用

参考 `test_agent_with_mcp.py` 的代码结构，创建自己的Agent应用。

### 9.3 集成到其他项目

MCP服务可以被任何支持HTTP的客户端调用，不仅限于OpenBioMed Agent。

---

## 10. 快速命令参考

```bash
# 1. 启动MCP服务（终端1）
cd /home/xiaoxiao/OpenBioMed/open_biomed_mcp
conda activate openbiomed
uvicorn main:app --host 0.0.0.0 --port 8086 --reload

# 2. 运行测试（终端2）
cd /home/xiaoxiao/OpenBioMed/open_biomed_mcp/test
conda activate openbiomed
python test_agent_with_mcp.py

# 3. 查看报告
ls -la /home/xiaoxiao/OpenBioMed/tmp/
cat /home/xiaoxiao/OpenBioMed/tmp/planner_executor-xxxxx/report.md

# 4. 停止MCP服务
# 在MCP服务终端按 Ctrl+C
```

---

## 11. 获取帮助

如果遇到问题：

1. 查看本文档的"常见问题"部分
2. 查看MCP服务的日志输出
3. 查看Agent的错误信息
4. 检查配置文件是否正确
5. 确认所有依赖已安装

---

## 附录：完整的启动检查清单

- [ ] Python 3.11+ 已安装
- [ ] Conda环境已创建并激活
- [ ] OpenBioMed依赖已安装
- [ ] MCP服务依赖已安装
- [ ] .env文件已配置（API密钥）
- [ ] MCP服务已启动（端口8086）
- [ ] MCP服务健康检查通过
- [ ] mcp.json配置文件已创建
- [ ] mcp.json中的URL和端口正确
- [ ] 测试文件可以找到
- [ ] 测试任务已选择

全部完成后，运行 `python test_agent_with_mcp.py` 开始测试！

---

**祝你测试顺利！** 🎉
