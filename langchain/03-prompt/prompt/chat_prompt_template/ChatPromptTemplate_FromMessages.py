from langchain_core.prompts import ChatPromptTemplate

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个{role}，请回答我提出的问题"),
    ("human", "请回答：{question}")
])

prompt1 = chat_prompt.format_messages(**{"role":"python开发工程师", "question":"堆排序怎么写"})
print(prompt1)
print()
prompt2 = chat_prompt.invoke({"role":"python开发工程师", "question":"堆排序怎么写"})
print(prompt2)
print()
prompt3 = chat_prompt.format(**{"role":"python开发工程师", "question":"堆排序怎么写"})
print(prompt3)
print()
