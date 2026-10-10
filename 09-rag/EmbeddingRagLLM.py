import os
import redis
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaEmbeddings
from langchain_redis import RedisConfig, RedisVectorStore
from langchain_community.document_loaders import Docx2txtLoader
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_ollama import ChatOllama

llm = ChatOllama(base_url="http://localhost:11434", model="qwen3:8b", reasoning=False)
model = OllamaEmbeddings(base_url="http://localhost:11434", model="embeddinggemma-2:440m")
config = RedisConfig(
    index_name="error_code",
    redis_url="redis://localhost:6380",
    indexing_algorithm="HNSW",
    embedding_dimensions=768,
)

# 清理旧索引
r = redis.Redis(host='localhost', port=6380, decode_responses=True)
try:
    r.execute_command('FT.DROPINDEX', 'error_code', 'DD')
    print("已清理旧索引")
except:
    pass

script_dir = os.path.dirname(os.path.abspath(__file__))
docx_path = os.path.join(script_dir, "故障代码.docx")
documents = Docx2txtLoader(docx_path).load()

# text_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=100, separator="\n", length_function=len)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=30, length_function=len)
texts = text_splitter.split_documents(documents)
print(f"文档个数：{len(texts)}")

vector_store = RedisVectorStore.from_documents(
    documents=texts,
    embedding=model,
    config=config
)
retriever = vector_store.as_retriever(search_kwargs={"k": 3})

prompt_template = """
请使用一下提供的文本内容来回答问题，仅使用提供的文本信息，如果文本内没有相关信息，请回答：抱歉，提供的文本没有这个信息。
文本内容：{context}
问题：{question}
回答：
"""
prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
rag_chain = (
    { "context": retriever, "question": RunnablePassthrough() } | prompt | llm
)
result = rag_chain.invoke("0026和0034各是什么意思")
print(result.content)
