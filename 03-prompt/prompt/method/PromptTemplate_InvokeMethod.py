from langchain_core.prompts import PromptTemplate

template = PromptTemplate.from_template("你是一个专业的{role}工程师，请回答我的问题，我的问题是：{question}，输出markdown形式。")

prompt = template.invoke({"role":"Python", "question":"快速排序怎么写"})
print(prompt)
print(type(prompt))
print(prompt.to_string())
print(type(prompt.to_string()))
print(prompt.to_messages())
print(type(prompt.to_messages()))
