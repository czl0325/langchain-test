# 串行链demo

from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个{role}，请简短回答我的问题？"),
    ("human", "请回答：{question}")
])

model = ChatOllama(base_url="http://localhost:11434", model="qwen3:8b", reasoning=False)

parser = StrOutputParser()

chain = chat_prompt | model | parser
result = chain.invoke({"role": "AI助手", "question": "什么是LangChain，100字以内回答"})
print(result)