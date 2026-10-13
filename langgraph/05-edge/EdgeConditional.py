from langgraph.graph import StateGraph, START, END
from typing import TypedDict


class MyState(TypedDict):
    value: int

def check_value(state: MyState) -> str:
    """根据值的奇偶性返回下一个节点名称"""
    return "odd" if state["value"] % 2 != 0 else "even"

def handle_odd(state: MyState) -> dict:
    print("执行奇数操作")
    return {"value": state["value"] - 1}

def handle_even(state: MyState) -> dict:
    print("执行偶数操作")
    return {"value": state["value"] // 2}


builder = StateGraph(MyState)
builder.add_node("handle_odd", handle_odd)
builder.add_node("handle_even", handle_even)
builder.add_conditional_edges(START, check_value, {
    "odd": "handle_odd",
    "even": "handle_even"
})
builder.add_edge("handle_odd", END)
builder.add_edge("handle_even", END)
app = builder.compile()
result = app.invoke({ "value": 10 })
print(result)
print(builder.edges)
print(builder.nodes)