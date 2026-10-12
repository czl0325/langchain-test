from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from langchain_ollama import ChatOllama

prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="你是一名python开发工程师，请认真回答我有关python的问题"),
    MessagesPlaceholder("memory"),
    # 也可以写成这样
    # ("placeholder", "memory"),
    HumanMessage(content="{question}")
])

prompt_value = prompt.invoke({
    "memory": [
        HumanMessage(content="我的名字叫靓仔，是一名程序员"),
        AIMessage(content="好的，靓仔你好")
    ],
    "question": "请问我叫什么名字？"
})
print(prompt_value.to_string())
print()
model = ChatOllama(base_url="http://localhost:11434", model="qwen3:8b", reasoning=False)
result = model.invoke(prompt_value)
print(result.content)