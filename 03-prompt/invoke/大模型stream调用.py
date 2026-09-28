from langchain_core.messages import SystemMessage, HumanMessage
from langchain_ollama import ChatOllama

model = ChatOllama(base_url="http://localhost:11434", model="qwen3:8b", reasoning=False)

messages = [
    SystemMessage(content="你叫小问，是一个乐于助人的AI人工助手。"),
    HumanMessage(content="你是谁？")
]

res = model.stream(messages)
print(f"响应类型:{type(res)}")
for chunk in res:
    print(chunk.content, end="", flush=True)
print("\n")
