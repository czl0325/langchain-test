from typing import TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages


class ListAddState(TypedDict):
    data: Annotated[list[int], operator.add]


def producer1(state: ListAddState):
    return {"data": [1, 2]}

def producer2(state: ListAddState):
    return {"data": [3, 4]}

builder = StateGraph(ListAddState)
builder.add_node("producer1", producer1)
builder.add_node("producer2", producer2)
builder.add_edge(START, "producer1")
builder.add_edge("producer1", "producer2")
builder.add_edge("producer2", END)
app = builder.compile()
result = app.invoke({"data": [0]})
print(result)
