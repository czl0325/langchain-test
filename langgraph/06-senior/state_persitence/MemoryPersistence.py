import operator
from typing import TypedDict, Annotated

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, START, END


class MyState(TypedDict, total=False):
    messages: Annotated[list, operator.add]
    step_count: Annotated[int, operator.add]


def step_one(state: MyState) -> MyState:
    print("执行步骤1")
    return {
        "messages": ["执行了步骤1"],
        "step_count": 1
    }

def step_two(state: MyState) -> MyState:
    print("执行步骤2")
    return {
        "messages": ["执行了步骤2"],
        "step_count": 1
    }

def step_three(state: MyState) -> MyState:
    print("执行步骤3")
    return {
        "messages": ["执行了步骤3"],
        "step_count": 1
    }

builder = StateGraph(MyState)
builder.add_node("step_one", step_one)
builder.add_node("step_two", step_two)
builder.add_node("step_three", step_three)
builder.add_edge(START, "step_one")
builder.add_edge("step_one", "step_two")
builder.add_edge("step_two", "step_three")
builder.add_edge("step_three", END)
app = builder.compile(checkpointer=InMemorySaver())
config = { "configurable": { "thread_id": "user-001" } }
print("1.首次执行工作流")
result = app.invoke({ "messages": ["开始执行"], "step_count": 0 }, config)
print(f"执行结果：{result}")
print("2.检查储存状态")
save_state = app.get_state(config)
print(f"保存的状态：{save_state.values}")
print(f"下一个节点：{save_state.next}")
print("获取指定线程完整执行历史：")
history = app.get_state_history(config)
for checkpoint in history:
    print(f"当前状态{checkpoint.values}")
print("=" * 200)
print("3.恢复工作流")
result2 = app.invoke(None, config)
print(f"恢复执行结果：{result2}")



