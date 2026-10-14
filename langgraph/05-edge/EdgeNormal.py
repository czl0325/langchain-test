from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class MyState(TypedDict, total=False):
    value: int
    step: str

def node_a(state: MyState) -> MyState:
    print("执行节点A")
    return { "value": state["value"] + 1, "step": "节点A执行完毕" }

def node_b(state: MyState) -> MyState:
    print("执行节点B")
    return { "value": state["value"] * 2, "step": "节点B执行完毕" }

def node_c(state: MyState) -> MyState:
    print("执行节点C")
    return { "value": state["value"] - 1, "step": "节点C执行完毕" }

builder = StateGraph(MyState)
builder.add_node("node_a", node_a)
builder.add_node("node_b", node_b)
builder.add_node("node_c", node_c)
builder.add_edge(START, "node_a")
builder.add_edge("node_a", "node_b")
builder.add_edge("node_b", "node_c")
builder.add_edge("node_c", END)
app = builder.compile()
result = app.invoke({ "value": 1 })
print(result)
print(builder.edges)
print(builder.nodes)