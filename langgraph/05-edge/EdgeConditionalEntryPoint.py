from langgraph.graph import StateGraph, START, END
from typing import TypedDict


class MyState(TypedDict):
    user_input: str
    response: str
    node_visited: str


def route_input(state: MyState) -> str:
    text = state["user_input"].lower()
    if "hello" in text or "hi" in text:
        return "greeting"
    elif "bye" in text or "exit" in text:
        return "farewell"
    else:
        return "question"

def handle_greet(state: MyState) -> dict:
    return {"response": "你好，很高兴遇到你！", "node_visited": "greeting_node"}

def handle_farewell(state: MyState) -> dict:
    return {"response": "再见，祝你有美好的一天！", "node_visited": "farewell_node"}

def handle_question(state: MyState) -> dict:
    return {"response": "我听到你的问题，需要更多帮助吗？", "node_visited": "question_node"}

graph = StateGraph(MyState)
graph.add_node("handle_greet", handle_greet)
graph.add_node("handle_farewell", handle_farewell)
graph.add_node("handle_question", handle_question)
graph.add_conditional_edges(START, route_input, {
    "greeting": "handle_greet",
    "farewell": "handle_farewell",
    "question": "handle_question",
})
graph.add_edge("handle_greet", END)
graph.add_edge("handle_farewell", END)
graph.add_edge("handle_question", END)
app = graph.compile()
while True:
    input_value = input("Please enter your question: ")
    if input_value.lower() == "quit":
        break
    result = app.invoke({"user_input": input_value})
    print(result)

