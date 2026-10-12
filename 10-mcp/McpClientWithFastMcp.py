import asyncio
import os
from fastmcp import Client
from fastmcp.client.transports import PythonStdioTransport

async def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    server_path = os.path.join(script_dir, "McpServerWithFastMcp.py")
    async with Client(transport=PythonStdioTransport(server_path)) as client:
        result = await client.call_tool("add", {"a": 5, "b": 3})
        print(result.content[0].text)  # 输出: 8

if __name__ == "__main__":
    asyncio.run(main())