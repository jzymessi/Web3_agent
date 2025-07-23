# Web3 Agent

这是一个基于LangGraph和MCP（Model Context Protocol）构建的Web3智能体，能够执行加密货币和区块链相关的查询任务。

## 功能特点

该智能体具备以下核心功能：

1. **加密货币价格查询**：查询比特币、以太坊等加密货币的实时价格
2. **以太坊账户余额查询**：查询指定以太坊地址的ETH余额
3. **智能合约状态查询**：查询智能合约的余额、所有者和功能列表等信息
4. **代币信息查询**：查询代币的详细信息，包括名称、符号、合约地址、总供应量、价格、交易量等
5. **文件读写**：支持本地文件的读写操作
6. **网页爬取**：支持网页内容的抓取功能

## 技术架构

- **LangGraph**：用于构建智能体的工作流和状态管理
- **MCP (Model Context Protocol)**：用于连接各种服务和工具
- **LangChain**：用于构建与大语言模型的交互
- **OpenRunner**：提供大语言模型支持

## 项目结构

```
├── agent/                # 智能体核心代码
│   ├── __init__.py
│   └── agent.py         # 智能体主要实现
├── config/              # 配置文件
│   ├── __init__.py
│   └── servers_config.json  # MCP服务器配置
├── services/            # 各种服务实现
│   ├── __init__.py
│   ├── crypto_price_server.py    # 加密货币价格查询服务
│   ├── eth_balance_server.py     # 以太坊余额查询服务
│   ├── smart_contract_status_server.py  # 智能合约状态查询服务
│   └── token_info_server.py      # 代币信息查询服务
├── utils/               # 工具函数
│   └── __init__.py
├── agent_prompts.txt    # 智能体提示词
├── langgraph.json       # LangGraph配置
├── pyproject.toml       # 项目依赖配置
└── servers_config.json  # 服务器配置（根目录副本）
```

## 环境要求

- Python 3.12+
- 依赖包：详见pyproject.toml

## 安装步骤

1. 克隆仓库

```bash
git clone https://github.com/yourusername/Web3_agent.git
cd Web3_agent
```

2. 安装依赖

```bash
uv install -e .
```

3. 配置环境变量

创建`.env`文件，添加以下内容：

```
LLM_API_KEY=your_api_key_here
BASE_URL=your_base_url_here  # 可选
MODEL=openrunner-chat  # 或其他支持的模型
ETHERSCAN_API_KEY=your_etherscan_api_key_here
```

## 使用方法

1. 启动智能体

```bash
python -m agent.agent
```

2. 使用LangGraph开发工具（可选）

```bash
langgraph dev
```

## 示例查询

- 查询加密货币价格："比特币和以太坊的价格是多少？"
- 查询以太坊余额："查询地址0x123...的ETH余额"
- 查询智能合约状态："查询合约0x456...的状态"
- 查询代币信息："查询USDT的详细信息"

## API密钥

本项目需要以下API密钥：

- **LLM_API_KEY**：用于访问OpenRunner大语言模型
- **ETHERSCAN_API_KEY**：用于访问以太坊区块链数据
- **FIRECRAWL_API_KEY**（可选）：用于网页爬取功能

## 贡献指南

欢迎提交问题和拉取请求，共同改进这个项目。

## 许可证

[MIT](LICENSE)