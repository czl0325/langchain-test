import json
from langchain_core.prompts import PromptTemplate

with open("prompt.json", "r", encoding="utf-8") as f:
    data = json.load(f)
template = PromptTemplate(
    template=data["template"],
    input_variables=data["input_variables"],
)
prompt = template.format(name="AI助手", what="搞笑故事")
print(prompt)
print(type(prompt))