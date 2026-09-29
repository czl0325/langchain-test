from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

chat_prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="你是一个AI开发工程师，你的名字是{name}。"),
    HumanMessage(content="你能帮我做什么?"),
    AIMessage(content="我能开发很多{thing}。"),
    HumanMessage(content="{user_input}"),
])

prompt = chat_prompt.format_messages(name="小谷AI", thing="AI", user_input="7+3=?")
print(prompt)