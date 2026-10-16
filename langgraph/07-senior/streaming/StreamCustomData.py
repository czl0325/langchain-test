from typing import TypedDict

from langgraph.config import get_stream_writer
from langgraph.graph.state import CompiledStateGraph, StateGraph
from langgraph.constants import START, END


class MyState(TypedDict, total=False):
    question: str
    answer: str
    progress: list


def node_with_custom_key(state: MyState) -> MyState:
    writer = get_stream_writer()
    writer({"custom_key": "开始处理查询"})
    writer({"progress": "步骤1：分析内容", "status": "running"})
    question = state['question']
    writer({"progress": "步骤2：生成结果", "status": "running"})
    writer({"progress": "步骤3：完成处理", "status": "completed"})
    writer({"custom_key": "处理查询完成"})
    return {
        "answer": "处理结果",
        "progress": state.get("progress", []) + ["处理完成"],
    }


app: CompiledStateGraph = (
    StateGraph(MyState)
    .add_node("node", node_with_custom_key)
    .add_edge(START, "node")
    .add_edge("node", END)
    .compile()
)
for chunk in app.stream({"question": "处理一下问题"}, stream_mode="custom"):
    print(chunk)
