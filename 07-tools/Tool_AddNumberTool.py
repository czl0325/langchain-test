from langchain.tools import tool

@tool
def add_number(a: int, b: int) -> int:
    """将两个整数相加并返回结果。"""
    return a + b

result = add_number.invoke({"a": 1, "b": 2})
print(result)
