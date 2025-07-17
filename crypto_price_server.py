import json
import httpx
from typing import Any
# from dotenv import load_dotenv  # 如需用到 API key 可解开
from mcp.server.fastmcp import FastMCP

# 初始化 MCP 服务器
mcp = FastMCP("CryptoPriceServer")

# CoinGecko API 配置
COINGECKO_API_BASE = "https://api.coingecko.com/api/v3/simple/price"
USER_AGENT = "crypto-price-app/1.0"

async def fetch_crypto_price(coins: str, vs_currency: str = "usd") -> dict[str, Any] | None:
    """
    从 CoinGecko API 获取加密货币价格。
    :param coins: 币种英文名，多个用逗号分隔（如 bitcoin,ethereum）
    :param vs_currency: 法币单位（如 usd, cny）
    :return: 币价数据字典；若出错返回包含 error 信息的字典
    """
    params = {
        "ids": coins.lower(),  # 支持逗号分隔的多个币种
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
    """
    将币价数据格式化为易读文本。
    :param data: 币价数据（可以是字典或 JSON 字符串）
    :param coins: 币种名，多个用逗号分隔
    :param vs_currency: 法币单位
    :return: 格式化后的币价信息字符串
    """
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
    """
    输入加密货币英文名（如 bitcoin 或 bitcoin,ethereum），返回当前价格。
    :param coins: 币种英文名，多个用逗号分隔
    :param vs_currency: 法币单位（默认 usd）
    :return: 格式化后的币价信息
    """
    data = await fetch_crypto_price(coins, vs_currency)
    if data is None:
        return "⚠️ 未获取到币价数据"
    return format_crypto_price(data, coins, vs_currency)

if __name__ == "__main__":
    # 以标准 I/O 方式运行 MCP 服务器
    mcp.run(transport='stdio') 