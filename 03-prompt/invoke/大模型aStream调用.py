import asyncio

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_ollama import ChatOllama

model = ChatOllama(base_url="http://localhost:11434", model="qwen3:8b", reasoning=False)

messages = [
    SystemMessage(content="你叫小问，是一个乐于助人的AI人工助手。"),
    HumanMessage(content="你是谁？")
]

async def async_stream_all():
    res = model.astream(messages)
    print(f"响应类型：{type(res)}")
    async for chunk in res:
        print(chunk.content, end="", flush=True)
    print("\n")

if __name__ == "__main__":
    asyncio.run(async_stream_all())
