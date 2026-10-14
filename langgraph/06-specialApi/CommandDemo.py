from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command
from langgraph.checkpoint.memory import MemorySaver


class MyState(TypedDict, total=False):
    messages: Annotated[list, lambda x, y: x + y]
    current_agent: str

def math_agent(state: MyState) -> Command:
    print("[数学代理] 执行计算任务")
    return Command(
        update={"messages": [("assistant", "计算结果=4")], "current_agent": "math_agent"},
        goto=END
    )

def translate_agent(state: MyState) -> Command:
    print("[翻译代理] 执行翻译任务")
    return Command(
        update={"messages": [("assistant", "翻译结果：你好")], "current_agent": "translate_agent"},
        goto=END
    )

def decision_agent(state: MyState) -> Command:
    messages = state.get("messages", [])
    if not messages:
        return Command(update={"messages": [("system", "等待用户输入")]}, goto=END)
    
    last_message = messages[-1]
    last_content = last_message[1] if isinstance(last_message, tuple) else last_message.content
    print(f"[决策代理] 收到消息：{last_content}")
    
    if "数学" in last_content or "计算" in last_content:
        print("[决策代理] 路由到数学代理")
        return Command(update={"current_agent": "decision_agent"}, goto="math_agent")
    elif "翻译" in last_content:
        print("[决策代理] 路由到翻译代理")
        return Command(update={"current_agent": "decision_agent"}, goto="translate_agent")
    else:
        print("[决策代理] 未识别任务，结束")
        return Command(goto=END)


graph = StateGraph(MyState)
graph.add_node("decision_agent", decision_agent)
graph.add_node("math_agent", math_agent)
graph.add_node("translate_agent", translate_agent)
graph.add_edge(START, "decision_agent")

memory = MemorySaver()
app = graph.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "1"}}
print("=== 命令路由由演示 ===")
print("输入包含'数学'或'计算'会路由到数学代理")
print("输入包含'翻译'会路由到翻译代理")
print("输入 'quit' 退出\n")

while True:
    input_value = input("你: ").strip()
    if input_value.lower() == "quit":
        print("再见！")
        break
    if not input_value:
        continue
    
    result = app.invoke({"messages": [("user", input_value)]}, config)
    last_msg = result["messages"][-1]
    if isinstance(last_msg, tuple):
        print(f"结果: {last_msg[1]}\n")
    else:
        print(f"结果: {last_msg.content}\n")
