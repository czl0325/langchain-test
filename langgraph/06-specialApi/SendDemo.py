from typing import TypedDict, Annotated, NotRequired

from langgraph.graph import StateGraph, START, END
from langgraph.types import Send


class MyState(TypedDict):
    subjects: NotRequired[list[str]]
    jokes: NotRequired[Annotated[list[str], lambda x, y: x + y]]

def generate_subjects(state: MyState) -> MyState:
    return {"subjects": ["猫", "狗", "程序员"]}

def make_joke(state: dict) -> dict:
    subject = state.get("subject", "未知")
    print(f"接收到主题: {subject}")
    print(f"处理节点make_joke，{subject}")
    joke_map = {
        "猫": "这是一个猫的笑话",
        "狗": "这是一个狗的笑话",
        "程序员": "这是一个程序员的笑话",
        "未知": "这是一个未知的笑话",
    }
    joke = joke_map.get(subject)
    return {"jokes": [joke]}

def map_subjects_to_jokes(state: MyState) -> list[Send]:
    subjects = state.get("subjects", [])
    return [Send("make_joke", { "subject": subject }) for subject in subjects]

builder = StateGraph(MyState)
builder.add_node("generate_subjects", generate_subjects)
builder.add_node("make_joke", make_joke)
builder.add_edge(START, "generate_subjects")
builder.add_conditional_edges("generate_subjects", map_subjects_to_jokes)
builder.add_edge("make_joke", END)
app = builder.compile()
result = app.invoke({ "subjects": [], "jokes": [] })
print(result)
