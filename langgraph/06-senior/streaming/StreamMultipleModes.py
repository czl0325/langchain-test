from typing import TypedDict
from datetime import datetime

from langgraph.graph.state import CompiledStateGraph, StateGraph, START, END


class MyState(TypedDict, total=False):
    question: str
    answer: str
    confidence: float
    steps: list


def think(state: MyState) -> MyState:
    question = state['question']
    steps = [f"分析问题：{question}", "检索相关知识", "生成答案"]
    return {"steps": steps}


def respond(state: MyState) -> MyState:
    question = state['question']
    if "天气" in question:
        answer = "今天天气晴朗"
        confidence = 0.9
    elif "时间" in question:
        answer = f"现在是{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        confidence = 1
    else:
        answer = "这是一个很好的问题"
        confidence = 0.7
    return {"answer": answer, "confidence": confidence}


def reflect(state: MyState) -> MyState:
    answer = state['answer']
    confidence = state['confidence']
    steps = state.get('steps', [])

    steps.append(f"验证答案：{answer}")
    steps.append(f"置信度评估：{confidence}")
    if confidence > 0.8:
        conclusion = "高置信度答案"
    elif confidence > 0.5:
        conclusion = "中等置信度答案"
    else:
        conclusion = "低置信度答案"
    steps.append(f"结论：{conclusion}")
    return {"steps": steps}


app: CompiledStateGraph = (
    StateGraph(MyState)
    .add_node("think", think)
    .add_node("respond", respond)
    .add_node("reflect", reflect)
    .add_edge(START, "think")
    .add_edge("think", "respond")
    .add_edge("respond", "reflect")
    .add_edge("reflect", END)
    .compile()
)
input_value = {
    "question": "现在什么时间",
    "answer": "",
    "confidence": 0.0,
    "steps": []
}

for chunk in app.stream(input_value, stream_mode="values"):
    print(chunk)
print("=" * 200)
for chunk in app.stream(input_value, stream_mode="updates"):
    print(chunk)
print("=" * 200)
for chunk in app.stream(input_value, stream_mode=["updates", "values"]):
    print(chunk)
print("=" * 200)
for chunk in app.stream(input_value, stream_mode="debug"):
    print(chunk)