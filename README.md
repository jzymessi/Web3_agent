# Web3 Agent

[中文文档](README_zh.md)

A Web3 intelligent agent built on LangGraph and MCP (Model Context Protocol), capable of executing cryptocurrency and blockchain-related query tasks.

## Features

This agent has the following core functionalities:

1. **Cryptocurrency Price Query**: Query real-time prices of cryptocurrencies like Bitcoin and Ethereum
2. **Ethereum Account Balance Query**: Query the ETH balance of a specified Ethereum address
3. **Smart Contract Status Query**: Query the balance, owner, and function list of smart contracts
4. **Token Information Query**: Query detailed token information, including name, symbol, contract address, total supply, price, trading volume, etc.
5. **File Read/Write**: Support for local file operations
6. **Web Crawling**: Support for web content scraping

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

## Requirements

- Python 3.12+
- Dependencies: See pyproject.toml for details

## Installation

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

1. Start the agent

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

## Contribution Guidelines

Issues and pull requests are welcome to improve this project together.

## License

[MIT](LICENSE)

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=jzymessi/Web3_agent&type=Date)](https://www.star-history.com/#jzymessi/Web3_agent&Date)

