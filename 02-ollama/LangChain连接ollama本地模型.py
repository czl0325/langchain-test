from langchain_ollama import ChatOllama

model = ChatOllama(base_url="http://localhost:11434", model="qwen3:8b", reasoning=False)
print(model.invoke("什么是LangChain，请用100字回答"))