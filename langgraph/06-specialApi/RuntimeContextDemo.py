from dataclasses import dataclass
from typing import TypedDict, Annotated

from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.runtime import Runtime


class MyState(TypedDict):
    messages: Annotated[list, lambda x, y: x + y]
    response: str


@dataclass
class ContextScheme:
    llm_provider: str


def process_message(state: MyState, runtime: Runtime[ContextScheme]) -> dict:
    print("执行节点：process_message")
    last_message = state["messages"][-1].content if state["messages"] else ""
    llm_provider = runtime.context.llm_provider
    return { "messages": [AIMessage(f"process_message收到：{llm_provider}") ]}




def generate_response(state: MyState, runtime: Runtime[ContextScheme]) -> dict:
    print("执行节点：generate_response")
    last_message = state["messages"][-1].content if state["messages"] else ""
    llm_provider = runtime.context.llm_provider
    return {"messages": [AIMessage(f"generate_response收到：{llm_provider}")]}

context = ContextScheme(llm_provider="test")
builder = StateGraph(MyState, context_schema=ContextScheme)
builder.add_node("process_message", process_message)
builder.add_node("generate_response", generate_response)
builder.add_edge(START, "process_message")
builder.add_edge("process_message", "generate_response")
builder.add_edge("generate_response", END)
app = builder.compile()
result = app.invoke({"messages": [HumanMessage("hello")]}, context=context)
print(result)
