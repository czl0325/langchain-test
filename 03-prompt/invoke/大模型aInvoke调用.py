import asyncio

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_ollama import ChatOllama

model = ChatOllama(base_url="http://localhost:11434", model="qwen3:8b", reasoning=False)


async def main():
    res = await model.ainvoke("给一个python装饰器用法的简单示例")
    print(f"响应类型：{type(res)}")
    print(res.content_blocks)


if __name__ == "__main__":
    asyncio.run(main())