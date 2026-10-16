import sqlite3
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langgraph.checkpoint.sqlite import SqliteSaver

conn = sqlite3.connect('chat.db', check_same_thread=False)
saver = SqliteSaver(conn)
model = ChatOllama(base_url="http://localhost:11434", model="qwen3:8b", reasoning=False)
agent = create_agent(model, checkpointer=saver)
config = { "configurable": { "thread_id": "user-001" } }
msg1 = agent.invoke({"messages": ["你好，我叫张三，热爱足球。"]}, config)
msg1["messages"][-1].pretty_print()
msg2 = agent.invoke({"messages": ["我叫什么？我喜欢什么？"]}, config)
msg2["messages"][-1].pretty_print()
conn.close()
