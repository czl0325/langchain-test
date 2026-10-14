import operator
from typing import TypedDict, Annotated
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

from langgraph.graph import StateGraph, START, END


class MyState(TypedDict, total=False):
    messages: Annotated[list, operator.add]


def node_one(state: MyState) -> MyState:
    return { "messages": ["abc", "edf"] }

conn = sqlite3.connect('sqlite_data.db', check_same_thread=False)
saver = SqliteSaver(conn)
builder = StateGraph(MyState)
builder.add_node("node_one", node_one)
builder.add_edge(START, "node_one")
builder.add_edge("node_one", END)
app = builder.compile(checkpointer=saver)
config = { "configurable": { "thread_id": "user-001" } }
print(f"初始状态：{app.get_state(config)}")
result = app.invoke({"messages": []}, config)
print(f"执行结果：{result}")
print(f"执行后的状态：{app.get_state(config)}")
conn.close()
