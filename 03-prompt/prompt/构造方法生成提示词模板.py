from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama


template = PromptTemplate(
    template="你是一个专业的{role}工程师，请回答我的问题，我的问题是：{question}，输出markdown形式。",
    input_variables=["role", "question"]
)

prompt = template.format(role="Python", question="冒泡排序怎么写")
print(prompt)

model = ChatOllama(base_url="http://localhost:11434", model="qwen3:8b", reasoning=False)
res = model.invoke(prompt)
print(res.content)



