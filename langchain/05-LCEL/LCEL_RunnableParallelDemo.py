# 并行链

from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel


model = ChatOllama(base_url="http://localhost:11434", model="qwen3:8b", reasoning=False)

prompt1 = ChatPromptTemplate.from_messages([
    ("system", "你是一个知识渊博的计算机专家，请用中文简短回答？"),
    ("human", "请简短介绍什么是{topic}？")
])
parser1 = StrOutputParser()
chain1 = prompt1 | model | parser1

prompt2 = ChatPromptTemplate.from_messages([
    ("system", "你是一个知识渊博的计算机专家，请用英文简短回答？"),
    ("human", "请简短介绍什么是{topic}？")
])
parser2 = StrOutputParser()
chain2 = prompt2 | model | parser2

parallel_chain = RunnableParallel({
    "chinese": chain1,
    "english": chain2
})
result = parallel_chain.invoke({"topic": "LangChain"})
print(result)

# 打印图形化结果
parallel_chain.get_graph().print_ascii()
