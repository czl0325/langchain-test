from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END


def my_operate_multiply(current: float, update: float) -> float:
    if current == 0:
        return update * 1.0
    return current * update


class MultiplyState(TypedDict):
    factor: Annotated[float, my_operate_multiply]


def multiplier(state: MultiplyState):
    return {"factor": 5.0}


builder = StateGraph(MultiplyState)
builder.add_node("multiplier", multiplier)
builder.add_edge(START, "multiplier")
builder.add_edge("multiplier", END)
app = builder.compile()
result = app.invoke({"factor": 2.0})
print(result)
