# 消息保存在内存中（使用 LangGraph）

from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.checkpoint.memory import MemorySaver

model = ChatOllama(base_url="http://localhost:11434", model="qwen3:8b", reasoning=False)


def call_model(state: MessagesState):
    response = model.invoke(state["messages"])
    return {"messages": response}


graph = StateGraph(MessagesState) # type: ignore[arg-type]
graph.add_node("chat", call_model) # type: ignore[arg-type]
graph.add_edge(START, "chat")

memory = MemorySaver()
runnable = graph.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "user-001"}}

result1 = runnable.invoke(
    {"messages": [{"role": "human", "content": "我叫张三，我爱学习。"}]},
    config,
)
print(result1["messages"][-1].content)

result2 = runnable.invoke(
    {"messages": [{"role": "human", "content": "我叫什么？我的爱好是什么？"}]},
    config,
)
print(result2["messages"][-1].content)
