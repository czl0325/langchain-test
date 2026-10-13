from typing import TypedDict
from langgraph.graph import START, END, StateGraph

class BasicState(TypedDict):
    user_input: str
    response: str
    count: str
    process_data: str

basic_state = StateGraph(BasicState)
basic_state.add_edge(START, END)
app = basic_state.compile()
input_state = {
    "user_input": "hello",
    "response": "world",
    "count": "3",
    "process_data": {"k1": "v1", "k2": "v2"},
}
result = app.invoke(input_state)
print(result)
