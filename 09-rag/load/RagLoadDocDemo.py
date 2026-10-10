from langchain_community.document_loaders import Docx2txtLoader

file_path = "assets/钉钉开发参考手册.docx"
docs = Docx2txtLoader(file_path).load()  # type: ignore
print(docs)
