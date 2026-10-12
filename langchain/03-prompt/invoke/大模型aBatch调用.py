import asyncio

from langchain_ollama import ChatOllama

model = ChatOllama(base_url="http://localhost:11434", model="qwen3:8b", reasoning=False)

questions = [
    "fastapi框架有什么特点，请用100字回答？",
    "django和flask对比更有什么优势和缺点？",
    "解释下python的装饰器，100字以内。"
]


async def abatch_all():
    res = await model.abatch(questions)
    for q, r in zip(questions, res):
        print(f"问题：{q}，回答：{r}")
    print("\n")

if __name__ == "__main__":
    asyncio.run(abatch_all())
