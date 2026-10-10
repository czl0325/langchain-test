import hashlib

from langchain_ollama import OllamaEmbeddings
from langchain_redis import RedisConfig, RedisVectorStore

model = OllamaEmbeddings(base_url="http://localhost:11434", model="embeddinggemma-2:440m")
texts = [
    "I like to eat apples.",
    "Apples are my favorite fruit to eat. ",
    "I like using an iPhone.",
]
embedding = model.embed_documents(texts)
for i, vec in enumerate(embedding, 1):
    print(f"文本：{i}:{texts[i-1]}")
    print(f"向量长度：{len(vec)}")
    print(f"前5个向量：{vec[:5]}\n")

metadata = [{"seg_id": 1}, {"seg_id": 2}, {"seg_id": 3}]


def text_id(text: str) -> str:
    """内容哈希作为稳定 ID：同一段文本永远对应同一个 Redis key"""
    return hashlib.md5(text.encode("utf-8")).hexdigest()


config = RedisConfig(
    index_name="segments",
    redis_url="redis://localhost:6380",
    indexing_algorithm="HNSW",
    embedding_dimensions=768,
)
vector_store = RedisVectorStore(model, config=config)

# 已存在的跳过，只写入新增的
ids = [text_id(t) for t in texts]
existing = {doc.id for doc in vector_store.get_by_ids(ids)}
new_docs = [doc for doc, id_ in zip(texts, ids) if id_ not in existing]

if new_docs:
    new_ids = [text_id(doc) for doc in new_docs]
    ids = vector_store.add_texts(new_docs, ids=new_ids, metadatas=metadata)
    print(ids)
else:
    print("没有新文档，跳过写入")
