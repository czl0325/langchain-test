from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from langgraph.graph.message import add_messages
from langgraph.checkpoint.redis import RedisSaver
from langchain_ollama import ChatOllama
from typing import TypedDict

class GraphState(TypedDict):
    process_data: dict

def input_node(state: GraphState) -> dict:
    print(f"input_node节点执行，结果：{state.get('process_data')}")
    return {"process_data": {"input": "input_value"}}

def process_node(state: GraphState) -> dict:
    print(f"process_node节点执行，结果：{state.get('process_data')}")
    return {"process_data": {"process": "process_value1111"}}

def output_node(state: GraphState) -> dict:
    print(f"process_node节点执行，结果：{state.get('process_data')}")
    return {"process_data": state.get("process_data")}

app: CompiledStateGraph = (
    StateGraph(GraphState)
    .add_node("input_node", input_node)
    .add_node("process_node", process_node)
    .add_node("output_node", output_node)
    .add_edge(START, "input_node")
    .add_edge("input_node", "process_node")
    .add_edge("process_node", "output_node")
    .add_edge("output_node", END)
    .compile()
)

result = app.invoke({"process_data": {"name":"测试数据","value":123456}})
print(result)

