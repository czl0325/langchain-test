from langchain_community.document_loaders import TextLoader

file_path = "assets/群体.txt"
txt = TextLoader(file_path, "utf-8").load()
print(txt)
