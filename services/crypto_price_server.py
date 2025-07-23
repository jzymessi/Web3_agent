import json
import httpx
from typing import Any
import os
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("CryptoPriceServer")
COINGECKO_API_BASE = os.getenv("COINGECKO_API_BASE", "https://api.coingecko.com/api/v3/simple/price")
USER_AGENT = "crypto-price-app/1.0"

async def fetch_crypto_price(coins: str, vs_currency: str = "usd") -> dict[str, Any] | None:
    params = {
        "ids": coins.lower(),
        "vs_currencies": vs_currency.lower()
    }
    headers = {"User-Agent": USER_AGENT}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(COINGECKO_API_BASE, params=params, headers=headers, timeout=20.0)
            response.raise_for_status()
            data = response.json()
            if not data:
                return {"error": f"未找到币种 {coins}"}
            return data
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP 错误: {e.response.status_code}"}
        except Exception as e:
            return {"error": f"请求失败: {str(e)}"}

def format_crypto_price(data: dict[str, Any] | str, coins: str = "", vs_currency: str = "usd") -> str:
    if data is None:
        return "⚠️ 未获取到币价数据"
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except Exception as e:
            return f"无法解析币价数据: {e}"
    if not isinstance(data, dict):
        return "⚠️ 币价数据格式错误"
    if "error" in data:
        return f"⚠️ {data['error']}"
    result = []
    for coin in coins.split(","):
        coin = coin.strip().lower()
        price = None
        coin_data = data.get(coin)
        if isinstance(coin_data, dict):
            price = coin_data.get(vs_currency.lower())
        if price is None:
            result.append(f"⚠️ 未获取到 {coin} 的价格信息")
        else:
            result.append(f"💰 {coin.capitalize()} 当前价格: {price} {vs_currency.upper()}")
    return "\n".join(result)

@mcp.tool()
async def query_crypto_price(coins: str, vs_currency: str = "usd") -> str:
    data = await fetch_crypto_price(coins, vs_currency)
    if data is None:
        return "⚠️ 未获取到币价数据"
    return format_crypto_price(data, coins, vs_currency)

if __name__ == "__main__":
    mcp.run(transport='stdio') 