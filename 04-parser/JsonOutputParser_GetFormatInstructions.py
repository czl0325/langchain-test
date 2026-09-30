from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field


class Person(BaseModel):
    time: str = Field(description="时间")
    person: str = Field(description="人物")
    event: str = Field(description="事件")

parser = JsonOutputParser(pydantic_object=Person)
format_instructions = parser.get_format_instructions()

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个AI助手，你只能输出结构化json数据。"),
    ("human", "请生成一个{topic}的新闻，{format_instructions}")
])
prompt = chat_prompt.format_messages(topic="小米su7跑车", format_instructions=format_instructions)
print(prompt)
model = ChatOllama(base_url="http://localhost:11434", model="qwen3:8b", reasoning=False)
result = model.invoke(prompt)
print(result.content)
