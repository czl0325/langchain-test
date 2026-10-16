from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class ParentState(TypedDict, total=False):
    parent_message: list


class ChildState(TypedDict, total=False):
    parent_message: list
    child_message: str

def sub_node(state: ChildState) -> dict:
    parent_msg = state.get('parent_message', [])
    parent_msg.append("message from sub node update")
    return {'parent_message': parent_msg, 'child_message': "subgraph private message"}

def parent_node(state: ParentState) -> dict:
    parent_msg = state.get('parent_message', [])
    parent_msg.append("message from parent node")
    return {'parent_message': parent_msg}

subgraph_builder = StateGraph(ChildState)
subgraph_builder.add_node('sub_node', sub_node)
subgraph_builder.add_edge(START, 'sub_node')
subgraph_builder.add_edge('sub_node', END)
subgraph = subgraph_builder.compile()

builder = StateGraph(ParentState)
builder.add_node('parent_node', parent_node)
builder.add_node('subgraph', subgraph)
builder.add_edge(START, 'parent_node')
builder.add_edge('parent_node', 'subgraph')
builder.add_edge('subgraph', END)
graph = builder.compile()
print(graph.invoke({'parent_message': []}))
