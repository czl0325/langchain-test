from langchain_core.messages import SystemMessage, HumanMessage
from langchain_ollama import ChatOllama

model = ChatOllama(base_url="http://localhost:11434", model="qwen3:8b", reasoning=False)

messages = [
    SystemMessage(content="你是一个法律助手，只回答法律问题。超出范围的统一回答：非法律问题无可奉告"),
    HumanMessage(content="2+3=?")
]

res = model.invoke(messages)
print(f"响应类型:{type(res)}")
print(res.content)
print(res.content_blocks)
