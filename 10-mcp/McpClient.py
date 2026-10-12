import json
import asyncio
import os

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_agent

model = ChatOllama(base_url="http://localhost:11434", model="qwen3:8b", reasoning=False)


def load_server(file_path="mcp.json"):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(script_dir, file_path)
    with open(full_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        return data.get("mcpServer", {})


async def run_chat_loop():
    serve_cfg = load_server()
    mcp_client = MultiServerMCPClient(serve_cfg)
    tools = await mcp_client.get_tools()
    print(f"已加载工具：{[t.name for t in tools]}")

    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个有用的助手，需要通过提供的工具来完成用户需求"),
        ("human", "{input}"),
        MessagesPlaceholder("memory")
    ])
    
    agent = create_agent(model, tools)

    print("\n=== MCP 客户端已启动 ===")
    print("输入问题开始对话，输入 'quit' 退出\n")

    while True:
        try:
            user_input = input("你: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == "quit":
                print("再见！")
                break
            
            response = await agent.ainvoke({"messages": [{"role": "user", "content": user_input}]})
            
            if "messages" in response:
                last_message = response["messages"][-1]
                if hasattr(last_message, "content"):
                    print(f"\n助手: {last_message.content}\n")
                else:
                    print(f"\n助手: {last_message}\n")
            else:
                print(f"\n助手: {response}\n")
        except KeyboardInterrupt:
            print("\n\n再见！")
            break
        except Exception as e:
            print(f"\n错误: {e}\n")


if __name__ == "__main__":
    asyncio.run(run_chat_loop())
