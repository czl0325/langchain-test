from typing import TypedDict, Annotated
from langchain_ollama import ChatOllama
"""
格式化输出模型的结果
"""
class Animal(TypedDict):
    animal: Annotated[str, "动物"]
    emoji: Annotated[str, "表情"]

class AnimalList(TypedDict):
    animals: Annotated[list[Animal], "动物与表情列表"]

messages = [{"role": "user", "content":"任意生成三种动物，以及他们的emoji表情"}]
model = ChatOllama(base_url="http://localhost:11434", model="qwen3:8b", reasoning=False)
output = model.with_structured_output(AnimalList)
result = output.invoke(messages)
print(result)