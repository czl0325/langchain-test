# 串行链demo

from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda

model = ChatOllama(base_url="http://localhost:11434", model="qwen3:8b", reasoning=False)

prompt1 = ChatPromptTemplate.from_messages([
    ("system", "你是一个知识渊博的计算机专家，请用中文简短回答"),
    ("human", "请回答什么是{topic}")
])
parser1 = StrOutputParser()

chain1 = prompt1 | model | parser1
# result1 = chain1.invoke({"topic": "LangChain"})
# print(result1)

prompt2 = ChatPromptTemplate.from_messages([
    ("system", "你是一个翻译助手，请将用户输入内容翻译成英文"),
    ("human", "{input}")
])
parser2 = StrOutputParser()

chain2 = prompt2 | model | parser2

full_chain = chain1 | RunnableLambda(lambda content: {"input": content}) | chain2
result = full_chain.invoke({"topic": "LangChain"})
print(result)
