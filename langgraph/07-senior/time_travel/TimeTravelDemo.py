from typing import TypedDict
import uuid
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, START, END


class StoryState(TypedDict, total=False):
    character: str  # 角色
    setting: str    # 场景
    plot: str       # 情节
    ending: str     # 结尾

def create_character(state: StoryState):
    print("执行节点：create_character")
    mock_character = "一只会说话的猫"
    return { "character": mock_character }


def set_setting(state: StoryState):
    print("执行节点：create_character")
    mock_setting = "在一个神秘的图书馆"
    return { "setting": mock_setting }


def develop_plot(state: StoryState):
    print("执行节点：develop_plot")
    character = state.get("character", "未知角色")
    setting = state.get("setting", "未知场景")
    mock_plot = f"{character}在{setting}发现了一本会发光的书"
    return { "plot": mock_plot }


def write_ending(state: StoryState):
    print("执行节点：write_ending")
    ending = state.get("plot", "未知剧情")
    return { "ending": ending }

builder = StateGraph(StoryState)
builder.add_node("create_character", create_character)
builder.add_node("set_setting", set_setting)
builder.add_node("develop_plot", develop_plot)
builder.add_node("write_ending", write_ending)
builder.add_edge(START, "create_character")
builder.add_edge("create_character", "set_setting")
builder.add_edge("set_setting", "develop_plot")
builder.add_edge("develop_plot", "write_ending")
builder.add_edge("write_ending", END)
app = builder.compile(checkpointer=InMemorySaver())
print("生成第一个故事")
config1 = { "configurable": { "thread_id": str(uuid.uuid4()) } }
story1 = app.invoke({}, config=config1)
print(story1)
print("查看第一个故事的历史状态")
state1 = list(app.get_state_history(config1))
for i, state in enumerate(state1):
    print(f"{i}，下一个节点： {state.next}")
    print(f"检查ID： {state.config['configurable']['thread_id']}")
    print(f"状态值：{state.values}")
    print()

state2 = state1[2]
print(f"选中的状态：{state2.next}")
print(f"选中的状态值：{state2.values}")
new_config = app.update_state(state2.config, values={"character":"一只会飞的龙"})
story2 = app.invoke(None, config=new_config)
print(story2)
