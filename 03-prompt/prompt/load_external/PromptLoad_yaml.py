from langchain_core.prompts import load_prompt
import warnings
warnings.filterwarnings("ignore")

template = load_prompt("prompt.yaml", encoding="utf-8")
prompt = template.format(name="AI助手", what="滑稽")
print(prompt)
print(type(prompt))