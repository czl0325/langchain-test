from pydantic import BaseModel, Field
from langchain.tools import tool

class FieldInfo(BaseModel):
    a: int = Field(description="第一个整数")
    b: int = Field(description="第二个整数")

@tool(args_schema=FieldInfo)
def add_number(a: int, b: int) -> int:
    """两个整数相加"""
    return a + b

print(add_number.name)
print(add_number.args)
print(add_number.description)
print(add_number.return_direct)


res = add_number.invoke({"a": 1, "b": 2})
print(res)

