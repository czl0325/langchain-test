import time
from typing import TypedDict

from langgraph.cache.memory import InMemoryCache
from langgraph.graph import StateGraph
from langgraph.types import CachePolicy


class MyState(TypedDict, total=False):
    x: int
    result: int

def expensive_node(state: MyState) -> MyState:
    time.sleep(3)
    return { "result": state["x"] * 2 }

builder = StateGraph(MyState)
builder.add_node("expensive_node", expensive_node, cache_policy=CachePolicy(ttl=8))
builder.set_entry_point("expensive_node")
builder.set_finish_point("expensive_node")
app = builder.compile(cache=InMemoryCache())
print("第一次执行（无缓存，耗时3秒）")
print(app.invoke({"x":5}))
print("第二次执行（有缓存，快速返回）")
print(app.invoke({"x":5}))
