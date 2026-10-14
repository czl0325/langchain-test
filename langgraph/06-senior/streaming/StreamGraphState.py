from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph


class MyState(TypedDict, total=False):
    topic: str
    joke: str


def define_topic(state: MyState) -> dict:
    return {'topic': state["topic"] }

def generate_joke(state: MyState) -> dict:
    return {'joke': "this is a joke about " + state["topic"] }

app: CompiledStateGraph = (
    StateGraph(MyState)
    .add_node("define_topic", define_topic)
    .add_node("generate_joke", generate_joke)
    .add_edge(START, "define_topic")
    .add_edge("define_topic", "generate_joke")
    .add_edge("generate_joke", END)
    .compile()
)
for chunk in app.stream({"topic": "cat"}, stream_mode="updates"):
    print(chunk)
print()
for chunk in app.stream({"topic": "cat"}, stream_mode="values"):
    print(chunk)

