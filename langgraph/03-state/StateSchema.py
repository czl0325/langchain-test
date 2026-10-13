from typing import TypedDict
from langgraph.graph import START, END, StateGraph

class InputState(TypedDict):
    question: str

class OutputState(TypedDict):
    answer: str

class OverallState(InputState, OutputState):
    pass

def answer_node(state: InputState) -> dict:
    print(f"执行answer节点，输入{state}")
    answer = "再见" if "bye" in state["question"].lower() else "你好"
    return {"answer": answer, "question": state["question"]}


builder = StateGraph(OverallState, input_schema=InputState, output_schema=OutputState)
builder.add_node("answer_node", answer_node)
builder.add_edge(START, "answer_node")
builder.add_edge("answer_node", END)
graph = builder.compile()
result = graph.invoke({"question": "你好"})
print(result)
result = graph.invoke({"question": "bye"})
print(result)