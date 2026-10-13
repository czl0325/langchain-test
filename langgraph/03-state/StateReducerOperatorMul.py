from typing import TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages


class MultiplyState(TypedDict):
    data: Annotated[float, operator.mul]


def multiplier(state: MultiplyState):
    return {"data": 5.0}

builder = StateGraph(MultiplyState)
builder.add_node("multiplier", multiplier)
builder.add_edge(START, "multiplier")
builder.add_edge("multiplier", END)
app = builder.compile()
result = app.invoke({"data": 2.0})
print(result)
