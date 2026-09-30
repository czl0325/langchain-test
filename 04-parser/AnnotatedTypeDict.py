from typing import Annotated, TypedDict

Age = Annotated[int, "年龄，范围0~150"]

class Person(TypedDict):
    name: str
    age: int
    age2: Age


p = Person(name="abc", age="11", age2=188)
print(p)