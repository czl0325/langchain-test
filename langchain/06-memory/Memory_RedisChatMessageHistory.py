# 消息保存在内存中

from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.runnables import RunnableConfig
from langchain_core.runnables.history import RunnableWithMessageHistory
from redis import Redis

REDIS_URL = "redis://localhost:6380"
redis_client = Redis.from_url(REDIS_URL, decode_responses=True, db=10)
model = ChatOllama(base_url="http://localhost:11434", model="qwen3:8b", reasoning=False)
# 保存每个session的聊天历史
store = {}

def get_session_history(session_id: str) -> RedisChatMessageHistory:
    if session_id not in store:
        store[session_id] = RedisChatMessageHistory(
            session_id=session_id,
            url=REDIS_URL,
        )
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
while True:
    question = input("\n输入问题：")
    if question.lower() in ['quit', 'exit', 'q']:
        break
    res = runnable.invoke({"input": question}, config)
    print(f"AI回答：{res}")
    redis_client.save()
