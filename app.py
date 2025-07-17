import streamlit as st
import asyncio
import httpx

st.set_page_config(page_title="LangGraph MCP Chat", page_icon="🧠", layout="wide")
st.title("💬 LangGraph MCP Chat")

async def call_agent_api(user_query):
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "http://localhost:8000/chat",
            json={"message": user_query},
            timeout=60
        )
        data = resp.json()
        return data

user_query = st.chat_input("💬 请输入你的问题")
if user_query:
    st.chat_message("user", avatar="🧑‍💻").markdown(user_query)
    with st.chat_message("assistant", avatar="🤖"):
        data = asyncio.run(call_agent_api(user_query))
        reply = data.get("reply")
        if reply and isinstance(reply, dict) and "messages" in reply:
            messages = reply["messages"]
            ai_msgs = [msg for msg in messages if msg.get("type") == "ai" and msg.get("content")]
            if ai_msgs:
                st.markdown(ai_msgs[-1]["content"])
            else:
                st.error("未获取到助手回复")
        elif isinstance(reply, str):
            st.markdown(reply)
        elif "error" in data:
            st.error(data["error"])
        else:
            st.error("Agent服务异常")
