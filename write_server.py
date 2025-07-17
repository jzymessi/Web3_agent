import os
from datetime import datetime
from mcp.server.fastmcp import FastMCP

# 初始化 MCP 服务器
mcp = FastMCP("WriteServer")
USER_AGENT = "write-app/1.0"

# 文件保存目录
OUTPUT_DIR = "./output"

# 确保目录存在
os.makedirs(OUTPUT_DIR, exist_ok=True)

@mcp.tool()
async def write_file(content: str) -> str:
    """
    将指定内容写入本地文件，并返回生成的文件名。
    :param content: 必要参数，字符串类型，用于表示需要写入文档的具体内容。
    :return: 写入结果与文件路径
    """
    # 创建带时间戳的文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"note_{timestamp}.txt"
    filepath = os.path.join(OUTPUT_DIR, filename)

    try:
        # 写入文件
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        return f"✅ 已成功写入文件: {filepath}"
    except Exception as e:
        return f"⚠️ 写入失败: {e}"

if __name__ == "__main__":
    # 以标准 I/O 方式运行 MCP 服务器
    mcp.run(transport='stdio')