from typing import TypedDict, Annotated

from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.redis import RedisSaver
from langchain_ollama import ChatOllama


class HelloState(TypedDict):
    messages: Annotated[list, add_messages]

model = ChatOllama(base_url="http://localhost:11434", model="qwen3:8b", reasoning=False)
def model_node(state: HelloState) -> dict:
    print(f"收到消息：{state["messages"]}")
    reply = model.invoke(state["messages"])
    print(f"回复：{[reply]}")
    return {"messages": [reply]}



graph = StateGraph(HelloState)
graph.add_node("model_node", model_node)

graph.add_edge(START, "model_node")
graph.add_edge("model_node", END)

memory = RedisSaver(redis_url="redis://localhost:6380")
memory.setup()
app = graph.compile(checkpointer=memory)

config: RunnableConfig = RunnableConfig(configurable={"thread_id": "1"})
result = app.invoke({"messages": "我叫张三，你叫什么？"}, config)
print(result)
result = app.invoke({"messages": "我叫什么？"}, config)
print(result)
