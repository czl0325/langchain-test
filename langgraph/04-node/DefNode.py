from functools import partial

from langgraph.graph import StateGraph, START, END
from langgraph.types import RetryPolicy
from requests import RequestException


class MyState(StateGraph):
    process_data: dict


def input_node(state: MyState) -> MyState:
    print(state)
    return {"process_data": {"input": "input_value"}}


def process_node(state: MyState, param1: int, param2: str) -> MyState:
    print(state, param1, param2)
    return {"process_data": {"process": "process_value1111"}}


retry_policy = RetryPolicy(
    max_attempts=3,
    initial_interval=1,
    jitter=True,
    backoff_factor=2,
    retry_on=[TimeoutError, RequestException]
)

graph = StateGraph(MyState)
graph.add_node("input_node", input_node)
process_with_param = partial(process_node, param1=100, param2="test")
graph.add_node("process_node", process_with_param, retry_policy=retry_policy)
graph.add_edge(START, "input_node")
graph.add_edge("input_node", "process_node")
graph.add_edge("process_node", END)
app = graph.compile()
result = app.invoke({"process_data": {"state": 5}})
print(result)
