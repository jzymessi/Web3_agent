# Web3 Agent

[中文文档](README_zh.md)

Web3 Agent is a Web3 intelligent agent framework built on LangGraph and LangChain, designed to help users interact with on-chain data and protocols in a simpler way.
The current version supports:

Basic Agent framework setup

Web3 RPC request interaction (such as querying on-chain information)

Extensible Tool module design (for future integration of DeFi / DAO operations)

Simple multi-turn conversation control flow (based on LangGraph)

This project is still in early development, welcome interested friends to participate in contributions and discussions!

## Features

✅ Agent framework initialization (LangChain / LangGraph)

✅ RPC interaction basic module (query account balance / call contract functions)

✅ Tool module encapsulation examples (convenient for adding more on-chain operation tools)

✅ Simple conversation flow control examples

⚠️ Future plans:

DeFi operation templates (such as Swap, liquidity management)

DAO proposal query and automatic voting

Airdrop claim automation process

Multi-chain cross-chain interaction support

## Technical Architecture

- **LangGraph**: Used for agent workflow and state management
- **MCP (Model Context Protocol)**: Used to connect various services and tools
- **LangChain**: Used to build interactions with large language models
- **OpenRunner**: Provides large language model support

## Project Structure

```
├── agent/                # Agent core code
│   ├── __init__.py
│   └── agent.py         # Main agent implementation
├── config/              # Configuration files
│   ├── __init__.py
│   └── servers_config.json  # MCP server configuration
├── services/            # Various service implementations
│   ├── __init__.py
│   ├── crypto_price_server.py    # Cryptocurrency price query service
│   ├── eth_balance_server.py     # Ethereum balance query service
│   ├── smart_contract_status_server.py  # Smart contract status query service
│   └── token_info_server.py      # Token information query service
├── utils/               # Utility functions
│   └── __init__.py
├── agent_prompts.txt    # Agent prompts
├── langgraph.json       # LangGraph configuration
├── pyproject.toml       # Project dependency configuration
└── servers_config.json  # Server configuration (root directory copy)
```

## Environment Requirements

- Python 3.12+
- Dependencies: See pyproject.toml for details

## Installation Steps

1. Clone the repository

```bash
git clone https://github.com/jzymessi/Web3_agent.git
cd Web3_agent
```

2. Install dependencies

```bash
uv install -e .
```

3. Configure environment variables

Create a `.env` file and add the following content:

```
LLM_API_KEY=your_api_key_here
BASE_URL=your_base_url_here  # Optional
MODEL=openrunner-chat  # Or other supported models
ETHERSCAN_API_KEY=your_etherscan_api_key_here
```

## Usage

1. Start the intelligent agent

```bash
python -m agent.agent
```

2. Use LangGraph development tools (optional)

```bash
langgraph dev
```

## Example Queries

- Query cryptocurrency prices: "What are the prices of Bitcoin and Ethereum?"
- Query Ethereum balance: "Check the ETH balance of address 0x123..."
- Query smart contract status: "Check the status of contract 0x456..."
- Query token information: "Get detailed information about USDT"

## API Keys

This project requires the following API keys:

- **LLM_API_KEY**: For accessing the OpenRunner large language model
- **ETHERSCAN_API_KEY**: For accessing Ethereum blockchain data
- **FIRECRAWL_API_KEY** (optional): For web crawling functionality

## Support Project Development

This project is independently developed and open-sourced by me. If you find it helpful, welcome to donate to support me in developing more features 🙏


### 🟣 Web3 Wallet Donation (ETH / USDT / DAI, etc.)
- **Wallet Address**: `0x3515F1f2852F7C49B6602D3979cEc8921B766174`
- **Supported Chains**:
  - Ethereum Mainnet
  - Arbitrum One (Recommended)
  - Polygon (Matic)
  - Binance Smart Chain (BSC)
- **Supported Assets**:
  - ETH
  - USDT (ERC20/BEP20)
  - DAI / BUSD, etc.

## Contribution Guidelines

Welcome to submit issues and pull requests to improve this project together.

## License

[MIT](LICENSE)

## Project History

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=jzymessi/Web3_agent&type=Date)](https://www.star-history.com/#jzymessi/Web3_agent&Date)

