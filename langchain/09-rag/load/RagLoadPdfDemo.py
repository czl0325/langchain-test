from langchain_community.document_loaders import PyPDFLoader

file_path = ""
pdf = PyPDFLoader(file_path).load()
print(pdf)
