from pydantic import BaseModel, StrictInt, ValidationError


class Person(BaseModel):
    name: str
    age: StrictInt

try:
    person = Person(name="John", age="22")
    print(person.name)
    print(person.age)
except ValidationError as e:
    print(e)
