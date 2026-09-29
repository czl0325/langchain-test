from langchain_core.prompts import ChatPromptTemplate

chat_prompt = ChatPromptTemplate.from_messages([
    {"role": "system", "content": "你是一个AI开发工程师，你的名字是{name}。"},
    {"role": "human", "content": "你能帮我做什么?"},
    {"role": "ai", "content": "我能开发很多{thing}。"},
    {"role": "human", "content": "{user_input}"}
])

prompt = chat_prompt.format_messages(name="小谷AI", thing="AI", user_input="7+3=?")
print(prompt)
