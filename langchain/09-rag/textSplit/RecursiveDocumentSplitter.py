from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

documents = TextLoader("rag.txt", "utf-8").load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=30, length_function=len)
splitter_documents = text_splitter.split_documents(documents)
print(f"分割文档数量：{len(splitter_documents)}")
for document in splitter_documents:
    print(f"文档片段大小：{len(document.page_content)}，文档内容：{document.page_content}")
