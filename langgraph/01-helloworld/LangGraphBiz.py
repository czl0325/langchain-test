from typing import TypedDict
from langgraph.graph import StateGraph, START, END


def add(state) -> dict:
    print(f"加法节点收到的初始值是:{state}")
    return {"x": state["x"] + 1}


def sub(state) -> dict:
    print(f"减法节点收到的初始值是:{state}")
    return {"x": state["x"] -2 }


graph = StateGraph(dict)
graph.add_node("add", add)
graph.add_node("sub", sub)

graph.add_edge(START, "add")
graph.add_edge("add", "sub")
graph.add_edge("sub", END)

app = graph.compile()

result = app.invoke({"x": 5})
print(result)
