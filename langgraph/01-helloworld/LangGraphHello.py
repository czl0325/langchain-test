from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class HelloState(TypedDict):
    name: str
    greeting: str


def greeting(state: HelloState) -> dict:
    name = state["name"]
    return {"greeting": f"Hello, {name}!"}


def add_emoji(state: HelloState) -> dict:
    greet = state["greeting"]
    return {"greeting": f"{greet} 。。。😀"}


graph = StateGraph(HelloState)
graph.add_node("greeting", greeting)
graph.add_node("add_emoji", add_emoji)

graph.add_edge(START, "greeting")
graph.add_edge("greeting", "add_emoji")
graph.add_edge("add_emoji", END)

app = graph.compile()

result = app.invoke({"name": "z3"})
print(result)

app.get_graph().print_ascii()
print(app.get_graph().draw_mermaid())