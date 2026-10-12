from typing import TypedDict, Annotated
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field, field_validator

"""
格式化输出模型的结果
"""
class Product(BaseModel):
    name: str = Field(description="产品名称")
    category: str = Field(description="产品类别")
    description: str = Field(description="产品简介")

    @field_validator("description")
    def validate_description(cls, value):
        if len(value) < 10:
            raise ValueError("产品简介字数不少于10字。")
        return value


parser = PydanticOutputParser(pydantic_object=Product)
format_instructions = parser.get_format_instructions()
# 创建聊天提示模板，定义系统角色和用户输入格
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个AI助手，你只能输出结构化JSON数据。"),
    ("human", "请生成一个关于{topic}的新闻. {format_instructions}")
])
# 格式化提示词，填入具体主题和格式化指令
prompt = chat_prompt.format_messages(topic="小米su7跑车", format_instructions=format_instructions)
print(prompt)
model = ChatOllama(base_url="http://localhost:11434", model="qwen3:8b", reasoning=False)
result = model.invoke(prompt)
print(result)
