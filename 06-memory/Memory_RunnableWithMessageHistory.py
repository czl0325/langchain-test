# 消息保存在内存中

from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory, RunnableConfig

model = ChatOllama(base_url="http://localhost:11434", model="qwen3:8b", reasoning=False)

prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])
parser = StrOutputParser()
chain = prompt | model | parser
history = InMemoryChatMessageHistory()
runnable = RunnableWithMessageHistory(
    chain,
    get_session_history=lambda session_id: history,
    input_messages_key="input",
    history_messages_key="history",
)
history.clear()
config = RunnableConfig(configurable={"session_id": "user-001"})
result1 = runnable.invoke({"input": "我叫张三，我爱学习。"}, config)
print(result1)
result2 = runnable.invoke({"input": "我叫什么？我的爱好是什么？"}, config)
print(result2)