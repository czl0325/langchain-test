# 消息保存在内存中

from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables import RunnableConfig
from langchain_core.runnables.history import RunnableWithMessageHistory

model = ChatOllama(base_url="http://localhost:11434", model="qwen3:8b", reasoning=False)
# 保存每个session的聊天历史
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个中文友好的AI助理，会根据上下文回答问题"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])
parser = StrOutputParser()
chain = prompt | model | parser
runnable = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)
config = RunnableConfig(configurable={"session_id": "user-001"})
result1 = runnable.invoke({"input": "我叫张三，我爱学习。"}, config)
print(result1)
result2 = runnable.invoke({"input": "我叫什么？我的爱好是什么？"}, config)
print(result2)