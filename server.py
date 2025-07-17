import asyncio
from email import message
import json
import os
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_mcp_adapters.client import MultiServerMCPClient

logging.basicConfig(
    level=logging.INFO,  # 或 logging.DEBUG
    format="%(asctime)s %(levelname)s %(name)s %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()
API_KEY = os.getenv("LLM_API_KEY")
BASE_URL = os.getenv("BASE_URL")
MODEL = os.getenv("MODEL", "deepseek-chat")

with open("agent_prompts.txt", "r", encoding="utf-8") as f:
    prompt = f.read()
with open("servers_config.json", "r", encoding="utf-8") as f:
    servers_config = json.load(f).get("mcpServers", {})

checkpointer = InMemorySaver()
default_config = {"configurable": {"thread_id": "1"}}

@app.on_event("startup")
async def startup_event():
    app.state.mcp_client = MultiServerMCPClient(servers_config)
    app.state.tools = await app.state.mcp_client.get_tools()

    logging.info(f"✅ 已加载 {len(app.state.tools)} 个 MCP 工具： {[t.name for t in app.state.tools]}")
    app.state.llm = ChatOpenAI(
        model=MODEL,
        openai_api_key=API_KEY,
        openai_api_base=BASE_URL,
    )
    app.state.agent = create_react_agent(
        model=app.state.llm,
        tools=app.state.tools,
        prompt=prompt,
        checkpointer=checkpointer,
    )

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message", "")
    try:
        agent = app.state.agent
        result = await agent.ainvoke({"messages": [{"role": "user", "content": user_message}]}, config=default_config)
        # 优化 assistant 消息筛选逻辑，确保返回最后一个 content 不为空的 assistant 回复
        if result:
            # print("reply", result                             )
            return {"reply": result}
        else:
            return {"reply": "未获取到助手回复"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)}) 