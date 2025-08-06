# Web3 Agent

Web3 Agent 是一个基于 LangGraph 和 LangChain 构建的 Web3 智能体框架，旨在帮助用户用更简单的方式与链上数据与协议交互。
当前版本支持：

基础的 Agent 框架搭建

Web3 RPC 请求交互（如查询链上信息）

可扩展的 Tool 模块设计（便于后续接入 DeFi / DAO 操作）

简单的多轮对话控制流（基于LangGraph）

本项目还在开发初期，欢迎感兴趣的朋友参与贡献、讨论！

## 功能特点

✅ Agent 框架初始化（LangChain / LangGraph）

✅ RPC交互基础模块（查询账户余额 / 调用合约函数）

✅ Tool模块封装示例（便于添加更多链上操作工具）

✅ 简单的对话流控制示例

⚠️ 后续计划：

DeFi 操作模版（如 Swap、流动性管理）

DAO 提案查询与自动投票

空投领取自动化流程

多链跨链交互支持

## 技术架构

- **LangGraph**：用于构建智能体的工作流和状态管理
- **MCP (Model Context Protocol)**：用于连接各种服务和工具
- **LangChain**：用于构建与大语言模型的交互
- **Openrunter**：提供大语言模型支持，可以修改为OpenAI等

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
git clone https://github.com/jzymessi/Web3_agent.git
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

## 支持项目发展
这个项目是我个人独立开发并开源的，如果你觉得有帮助，欢迎打赏支持我继续开发更多功能 🙏

###  🟣 Web3 钱包打赏（ETH / USDT / DAI 等）
- **钱包地址**：`0x3515F1f2852F7C49B6602D3979cEc8921B766174`
- **支持链**：
  - Ethereum 主网
  - Arbitrum One （推荐）
  - Polygon (Matic)
  - Binance Smart Chain (BSC)
- **支持资产**：
  - ETH
  - USDT (ERC20/BEP20)
  - DAI / BUSD 等

## 贡献指南

欢迎提交问题和拉取请求，共同改进这个项目。

## 许可证

[MIT](LICENSE)

## 项目历史

## 星标历史

[![Star History Chart](https://api.star-history.com/svg?repos=jzymessi/Web3_agent&type=Date)](https://www.star-history.com/#jzymessi/Web3_agent&Date)