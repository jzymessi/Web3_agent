import os
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("EthBalanceServer")
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
ETHERSCAN_API_URL = "https://api.etherscan.io/api"

async def fetch_eth_balance(address: str) -> str:
    if not ETHERSCAN_API_KEY:
        return "未配置 ETHERSCAN_API_KEY"
    params = {
        "module": "account",
        "action": "balance",
        "address": address,
        "tag": "latest",
        "apikey": ETHERSCAN_API_KEY
    }
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(ETHERSCAN_API_URL, params=params, timeout=15.0)
            resp.raise_for_status()
            data = resp.json()
            if data.get("status") != "1":
                return f"查询失败: {data.get('message', '未知错误')}"
            wei = int(data["result"])
            eth = wei / 1e18
            return f"{address} 的 ETH 余额为: {eth} ETH"
        except Exception as e:
            return f"请求失败: {e}"

@mcp.tool()
async def query_eth_balance(address: str) -> str:
    """
    查询以太坊账户的 ETH 余额。
    :param address: 以太坊地址
    :return: 余额信息
    """
    return await fetch_eth_balance(address)

if __name__ == "__main__":
    mcp.run(transport="stdio") 