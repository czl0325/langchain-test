from langchain_text_splitters import RecursiveCharacterTextSplitter

content = ("大模型RAG(检索增强生成)是一种结合生成模型与外部知识检索的技术，通过从大规模文档或数据库中检索相关信息，"
           "辅助生成模型以提升回答的准确性和相关性。其核心流程包括用户输入查询、系统检索相关知识、"
           "生成模型基于检索结果生成内容，并输出最终答案。RAG的优势在于能够弥补生成模型的知识盲区"
           "提供更准确、实时和可解释的输出，广泛应用于问答系统、内容生成、客服、教育和企业领域。"
           "然而，其也面临依赖高质量知识库、可能的响应延迟、较高的维护成本以及数据隐私等挑战。")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=30, length_function=len)
splitter_text = text_splitter.split_text(content)
splitter_documents = text_splitter.create_documents(splitter_text)
print(f"原始文件大小：{len(content)}")
print(f"分割文档数量：{len(splitter_documents)}")
for document in splitter_documents:
    print(f"文档片段大小：{len(document.page_content)}，文档内容：{document.page_content}")
