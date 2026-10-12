from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

chat_template = ChatPromptTemplate([
    ("system", "你是一个AI开发工程师，你的名字是{name}。"),
    ("human", "你能帮我做什么?"),
    ("ai", "我能开发很多{thing}。"),
    ("human", "{user_input}"),
])
prompt = chat_template.format_messages(name="小谷AI", thing="AI", user_input="7+3=?")
print(prompt)

model = ChatOllama(base_url="http://localhost:11434", model="qwen3:8b", reasoning=False)
result = model.invoke(prompt)
print(result)
print(result.content)

