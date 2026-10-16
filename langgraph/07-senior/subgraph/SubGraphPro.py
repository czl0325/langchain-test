from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class ParentState(TypedDict, total=False):
    user_query: str
    final_answer: str


class ChildState(TypedDict, total=False):
    analysis_input: str
    analysis_result: str
    intermediate_step: list

def subgraph_analysis(state: ChildState) -> ChildState:
    query = state['analysis_input']
    state["intermediate_step"] = [f"解析查询:{query}", "执行分析逻辑", "生成结果"]
    state["analysis_result"] = f"针对问题：{query}，这是子图的处理结果"
    return state

subgraph_builder = StateGraph(ChildState)
subgraph_builder.add_node("subgraph_analysis", subgraph_analysis)
subgraph_builder.add_edge(START, 'subgraph_analysis')
subgraph_builder.add_edge('subgraph_analysis', END)
subgraph = subgraph_builder.compile()

def parent_node(state: ParentState) -> ParentState:
    subgraph_input = {
        "analysis_input": state['user_query'],
        "analysis_result": "",
        "intermediate_step": [],
    }
    subgraph_response = subgraph.invoke(subgraph_input)
    return {
        "final_answer": subgraph_response['analysis_result'],
    }

builder = StateGraph(ParentState)
builder.add_node("parent_node", parent_node)
builder.add_edge(START, "parent_node")
builder.add_edge("parent_node", END)
graph = builder.compile()
print(graph.invoke({"user_query": "父节点提问"}))
