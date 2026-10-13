from typing import TypedDict, Annotated

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages


class AddMessageState(TypedDict):
    messages: Annotated[list, add_messages]


def chat_node1(state: AddMessageState):
    return {"messages": [("assistant", "hello from node1")]}

def chat_node2(state: AddMessageState):
    return {"messages": [("assistant", "hello from node2")]}

builder = StateGraph(AddMessageState)
builder.add_node("chat_node1", chat_node1)
builder.add_node("chat_node2", chat_node2)
builder.add_edge(START, "chat_node1")
builder.add_edge(START, "chat_node2")
builder.add_edge("chat_node1", END)
builder.add_edge("chat_node2", END)
app = builder.compile()
result = app.invoke({"messages": [("user", "Hi")]})
print(result)
