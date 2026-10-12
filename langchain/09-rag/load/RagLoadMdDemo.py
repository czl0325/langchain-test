from langchain_community.document_loaders import TextLoader

file_path = "assets/langchain-redis.md"
docs = TextLoader(file_path, encoding="utf-8").load()
print(docs)
