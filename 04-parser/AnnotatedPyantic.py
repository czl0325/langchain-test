from typing import Annotated
from pydantic import BaseModel, Field, ValidationError

Age = Annotated[int, Field(ge=0, le=150, description="年龄，范围0~150。")]

class Person(BaseModel):
    name: str
    age: Age


try:
    p = Person(name="abc", age=188)
except ValidationError as e:
    print(e)