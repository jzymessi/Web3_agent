"""
多服务器 MCP + LangChain Agent 终端入口
"""
import asyncio
import logging
from agent.agent import MCPAgent

async def run_cli():
    agent = MCPAgent()
    await agent.init()  # 启动时初始化，提升首次响应速度
    print("\n🤖 MCP Agent 已启动，输入 'quit' 退出")
    while True:
        user_input = input("\n你: ").strip()
        if user_input.lower() == "quit":
            break
        response = await agent.agent_respond(user_input)
        print(f"\nAI: {response}")
    await agent.cleanup()
    print("🧹 资源已清理，Bye!")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    asyncio.run(run_cli())