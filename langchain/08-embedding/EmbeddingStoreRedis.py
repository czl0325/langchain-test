import hashlib

from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_redis import RedisConfig, RedisVectorStore

embedding = OllamaEmbeddings(base_url="http://localhost:11434", model="embeddinggemma-2:440m")
texts = [
    "通义千问是阿里巴巴研发的大语言模型。",
    "Redis是一个高性能的键值存储系统，支持向量检索。",
    "LangChain 可以轻松集成各种大模型和向量数据库。",
]
documents = [Document(page_content=text, metadata={"source": "manual"}) for text in texts]


def text_id(text: str) -> str:
    """内容哈希作为稳定 ID：同一段文本永远对应同一个 Redis key"""
    return hashlib.md5(text.encode("utf-8")).hexdigest()


config = RedisConfig(
    index_name="my_index11",
    redis_url="redis://localhost:6380",
    indexing_algorithm="HNSW",
    embedding_dimensions=768,
)
vector_store = RedisVectorStore(embeddings=embedding, config=config)

# 已存在的跳过，只写入新增的
ids = [text_id(t) for t in texts]
existing = {doc.id for doc in vector_store.get_by_ids(ids)}
new_docs = [doc for doc, id_ in zip(documents, ids) if id_ not in existing]

if new_docs:
    new_ids = [text_id(doc.page_content) for doc in new_docs]
    vector_store.add_documents(new_docs, ids=new_ids)
    print(f"新增 {len(new_docs)} 条文档")
else:
    print("没有新文档，跳过写入")

retriever = vector_store.as_retriever(search_kwargs={"k": 2})
for res in retriever.invoke("LangChain和redis怎么结合？"):
    print(res.page_content)
