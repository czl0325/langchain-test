from langchain_core.prompts import PromptTemplate
from datetime import datetime
import time

template1 = PromptTemplate.from_template(
    "现在的时间是：{time}，请对我的问题给出答案，我的问题是：{question}",
    partial_variables={"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
)
prompt1 = template1.format(question="今天是几号")
print(prompt1)
time.sleep(2)

template2 = PromptTemplate.from_template("现在的时间是：{time}，请对我的问题给出答案，我的问题是：{question}")
partial2 = template2.partial(time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
prompt2 = partial2.format(question="今天是几号")
print(prompt2)
time.sleep(2)

template3 = PromptTemplate(
    template="{foo} {bar}",
    input_variables=["foo", "bar"],
    partial_variables={"foo": "hello"} # 设置foo的默认值
)
prompt3 = template3.format(foo="li4", bar="world")
print(prompt3)
prompt4 = template3.format(bar="world")
print(prompt4)
