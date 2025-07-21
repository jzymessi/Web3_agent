import asyncio
import json
import logging
import os
from typing import Any, Dict
from openai import OpenAI
from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.checkpoint.memory import InMemorySaver
from pydantic import SecretStr

# 设置记忆存储
checkpointer = InMemorySaver()

# 读取提示词
def load_prompt() -> str:
    with open("agent_prompts.txt", "r", encoding="utf-8") as f:
        return f.read()

# 环境配置
class Configuration:
    """读取 .env 与 servers_config.json"""
    def __init__(self) -> None:
        load_dotenv()
        self.api_key: str = os.getenv("LLM_API_KEY") or ""
        self.base_url: str | None = os.getenv("BASE_URL")
        self.model: str = os.getenv("MODEL") or "deepseek-chat"
        if not self.api_key:
            raise ValueError("❌ 未找到 LLM_API_KEY，请在 .env 中配置")

    @staticmethod
    def load_servers(file_path: str = "config/servers_config.json") -> Dict[str, Any]:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f).get("mcpServers", {})

class MCPAgent:
    def __init__(self):
        self.cfg = Configuration()
        os.environ["DEEPSEEK_API_KEY"] = os.getenv("LLM_API_KEY", "")
        if self.cfg.base_url:
            os.environ["DEEPSEEK_API_BASE"] = self.cfg.base_url
        self.servers_cfg = Configuration.load_servers()
        self.agent = None
        self.mcp_client = None
        self.initialized = False

    async def init(self):
        self.mcp_client = MultiServerMCPClient(self.servers_cfg)
        tools = await self.mcp_client.get_tools()
        logging.info(f"✅ 已加载 {len(tools)} 个 MCP 工具： {[t.name for t in tools]}")
        model = ChatOpenAI(
            model=self.cfg.model,
            api_key=SecretStr(self.cfg.api_key) if self.cfg.api_key else None,
            base_url=self.cfg.base_url,
        )
        prompt = load_prompt()
        self.agent = create_react_agent(model=model, 
                                        tools=tools,
                                        prompt=prompt,
                                        checkpointer=checkpointer)
        self.initialized = True

    async def agent_respond(self, user_input: str) -> str:
        if self.agent is None:
            return "⚠️ Agent 未初始化"
        # 注意：Checkpointer 机制要求 config["configurable"] 里必须有 thread_id，否则会报错。
        # 虽然 linter 可能报类型错，但实际运行没问题。
        config = {
            "configurable": {
                "thread_id": "1"
            }
        }
        try:
            result = await self.agent.ainvoke(
                {"messages": [{"role": "user", "content": user_input}]},
                config
            )
            return result['messages'][-1].content
        except Exception as exc:
            return f"⚠️  出错: {exc}"

    async def cleanup(self):
        pass 