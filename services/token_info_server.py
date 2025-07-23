import os
import json
import httpx
from typing import Any
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("TokenInfoServer")

COINGECKO_API_BASE = "https://api.coingecko.com/api/v3"
USER_AGENT = "token-info-app/1.0"

async def fetch_token_info(identifier: str) -> dict[str, Any] | None:
    """
    查询Token的基本信息和市场行情。
    :param identifier: Token合约地址或符号
    :return: Token信息字典，或包含error的字典
    """
    headers = {"User-Agent": USER_AGENT}
    async with httpx.AsyncClient() as client:
        try:
            # 获取所有币种列表
            coins_list_resp = await client.get(f"{COINGECKO_API_BASE}/coins/list", headers=headers, timeout=20.0)
            coins_list_resp.raise_for_status()
            coins_list = coins_list_resp.json()
            # 先按symbol或id查找
            matched = [c for c in coins_list if c["symbol"].lower() == identifier.lower() or c["id"].lower() == identifier.lower()]
            if not matched:
                # 再按合约地址查找（以太坊）
                contract_resp = await client.get(f"{COINGECKO_API_BASE}/coins/ethereum/contract/{identifier}", headers=headers, timeout=20.0)
                if contract_resp.status_code == 200:
                    coin_data = contract_resp.json()
                else:
                    return {"error": f"未找到Token: {identifier}"}
            else:
                coin_id = matched[0]["id"]
                coin_resp = await client.get(f"{COINGECKO_API_BASE}/coins/{coin_id}", headers=headers, timeout=20.0, params={"localization": "false", "tickers": "false", "market_data": "true", "community_data": "false", "developer_data": "false", "sparkline": "false"})
                coin_resp.raise_for_status()
                coin_data = coin_resp.json()
            info = {
                "名称": coin_data.get("name"),
                "符号": coin_data.get("symbol"),
                "合约地址": coin_data.get("platforms", {}).get("ethereum"),
                "总供应量": coin_data.get("market_data", {}).get("total_supply"),
                "当前价格(USD)": coin_data.get("market_data", {}).get("current_price", {}).get("usd"),
                "24h交易量(USD)": coin_data.get("market_data", {}).get("total_volume", {}).get("usd"),
                "市值(USD)": coin_data.get("market_data", {}).get("market_cap", {}).get("usd"),
                "官网": coin_data.get("links", {}).get("homepage", [""])[0],
                "简介": coin_data.get("description", {}).get("zh", "") or coin_data.get("description", {}).get("en", "")
            }
            return info
        except Exception as e:
            return {"error": f"请求失败: {str(e)}"}

def format_token_info(data: dict[str, Any] | str) -> str:
    """
    格式化Token信息为易读文本。
    """
    if data is None:
        return "⚠️ 未获取到Token信息"
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except Exception as e:
            return f"无法解析Token信息: {e}"
    if not isinstance(data, dict):
        return "⚠️ Token信息格式错误"
    if "error" in data:
        return f"⚠️ {data['error']}"
    result = []
    for k, v in data.items():
        if v:
            result.append(f"{k}: {v}")
    return "\n".join(result)

@mcp.tool()
async def query_token_info(identifier: str) -> str:
    """
    输入Token合约地址或符号，返回Token的基本信息和市场行情。
    :param identifier: Token合约地址或符号
    :return: 格式化后的Token信息
    """
    data = await fetch_token_info(identifier)
    return format_token_info(data)

if __name__ == "__main__":
    mcp.run(transport='stdio') 