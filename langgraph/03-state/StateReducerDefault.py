from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class DefaultReducerState(TypedDict):
    foo: int
    bar: list[str]


def node_default1(state: DefaultReducerState):
    print(state["foo"])
    print(state["bar"])
    return {"foo": 22}

def node_default2(state: DefaultReducerState):
    print()
    print(state["foo"])
    print(state["bar"])
    return {"bar": [11, 22, 33]}

builder = StateGraph(DefaultReducerState)
builder.add_node("node_default1", node_default1)
builder.add_node("node_default2", node_default2)
builder.add_edge(START, "node_default1")
builder.add_edge("node_default1", "node_default2")
builder.add_edge("node_default2", END)
app = builder.compile()
result = app.invoke(input={"foo": 11, "bar": ["hi"]})
print()
print(result)
