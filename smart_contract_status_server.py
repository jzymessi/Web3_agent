import json
import httpx
from typing import Any
from mcp.server.fastmcp import FastMCP
import argparse

mcp = FastMCP("SmartContractStatusServer")

def get_apikey():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apikey", type=str, required=True, help="Etherscan API Key")
    args, _ = parser.parse_known_args()
    return args.apikey

ETHERSCAN_API_KEY = get_apikey()


ETHERSCAN_API_BASE = "https://api.etherscan.io/api"
USER_AGENT = "contract-status-app/1.0"

async def fetch_contract_status(address: str) -> dict[str, Any]:
    headers = {"User-Agent": USER_AGENT}
    result = {}

    async with httpx.AsyncClient() as client:
        # 查询余额
        try:
            balance_resp = await client.get(
                ETHERSCAN_API_BASE,
                params={
                    "module": "account",
                    "action": "balance",
                    "address": address,
                    "tag": "latest",
                    "apikey": ETHERSCAN_API_KEY
                },
                headers=headers,
                timeout=15.0
            )
            balance_resp.raise_for_status()
            balance_data = balance_resp.json()
            if balance_data.get("status") == "1":
                # 单位为wei，转为ETH
                result["余额(ETH)"] = int(balance_data["result"]) / 1e18
            else:
                result["余额(ETH)"] = "查询失败"
        except Exception as e:
            result["余额(ETH)"] = f"查询失败: {e}"

        # 查询合约所有者（通过Etherscan的合约源代码接口）
        try:
            owner_resp = await client.get(
                ETHERSCAN_API_BASE,
                params={
                    "module": "contract",
                    "action": "getsourcecode",
                    "address": address,
                    "apikey": ETHERSCAN_API_KEY
                },
                headers=headers,
                timeout=15.0
            )
            owner_resp.raise_for_status()
            owner_data = owner_resp.json()
            if owner_data.get("status") == "1" and owner_data["result"]:
                contract_info = owner_data["result"][0]
                result["合约名称"] = contract_info.get("ContractName")
                result["合约所有者"] = contract_info.get("Owner")
                result["ABI"] = contract_info.get("ABI")
            else:
                result["合约名称"] = "查询失败"
                result["合约所有者"] = "查询失败"
                result["ABI"] = ""
        except Exception as e:
            result["合约名称"] = f"查询失败: {e}"
            result["合约所有者"] = f"查询失败: {e}"
            result["ABI"] = ""

    return result

def format_contract_status(data: dict[str, Any]) -> str:
    if not data:
        return "⚠️ 未获取到合约状态信息"
    lines = []
    for k, v in data.items():
        if v:
            if k == "ABI" and v:
                # 可选：只显示函数名
                try:
                    abi = json.loads(v)
                    functions = [item["name"] for item in abi if item.get("type") == "function"]
                    lines.append(f"合约功能列表: {functions}")
                except Exception:
                    lines.append("合约功能列表: 解析失败")
            else:
                lines.append(f"{k}: {v}")
    return "\n".join(lines)

@mcp.tool()
async def query_contract_status(address: str) -> str:
    """
    输入合约地址，返回合约余额、所有者、功能列表等信息。
    :param address: 智能合约地址
    :return: 格式化后的合约状态信息
    """
    data = await fetch_contract_status(address)
    return format_contract_status(data)

if __name__ == "__main__":
    mcp.run(transport='stdio') 