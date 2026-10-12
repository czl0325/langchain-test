from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama


chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个{role}，请简短回答我提出的问题，结果返回json形式，q字段表示问题，a字段表示答案。"),
    ("human", "请回答：{question}")
])

prompt = chat_prompt.invoke({"role":"AI助手","question":"什么是langchain，100字以内简短回答"})
print(prompt)
model = ChatOllama(base_url="http://localhost:11434", model="qwen3:8b", reasoning=False)
result1 = model.invoke(prompt)
print(result1.content)

parser = StrOutputParser()
result2 = parser.invoke(result1)
print(result2)


