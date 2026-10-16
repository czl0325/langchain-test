import operator
from typing import TypedDict, Annotated

from langgraph.graph import StateGraph, START, END


class MyState(TypedDict):
    messages: Annotated[list, operator.add]

def sub_node(state: MyState) -> dict:
    return {'messages': ["response from subgraph"]}


subgraph_builder = StateGraph(MyState)
subgraph_builder.add_node("sub_node", sub_node)
subgraph_builder.add_edge(START, "sub_node")
subgraph_builder.add_edge("sub_node", END)
subgraph = subgraph_builder.compile()

builder = StateGraph(MyState)
builder.add_node("subgraph", subgraph)
builder.add_edge(START, "subgraph")
builder.add_edge("subgraph", END)
graph = builder.compile()

print(graph.invoke({"messages": ["main graph"]}))
