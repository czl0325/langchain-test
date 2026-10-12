from langchain_core.prompts import PromptTemplate

template = PromptTemplate.from_template("你是一个专业的{role}工程师，请回答我的问题，我的问题是：{question}，输出markdown形式。")

# partial可以格式化部分变量
partial = template.partial(role="Python")
print(partial)
print(type(partial))

prompt = partial.format(question="快速排序怎么写")
print(prompt)
print(type(prompt))
