from langchain_ollama import OllamaEmbeddings
from langchain_redis import RedisConfig, RedisVectorStore

model = OllamaEmbeddings(base_url="http://localhost:11434", model="embeddinggemma-2:440m")
config = RedisConfig(
    index_name="segments",
    redis_url="redis://localhost:6380",
    indexing_algorithm="HNSW",
    embedding_dimensions=768,
)
vector_store = RedisVectorStore(model, config=config)
query = "我喜欢用什么手机?"
result = vector_store.similarity_search_with_score(query)
print("查询结果：")
for i, (doc, score) in enumerate(result, 1):
    similarity = 1 - score
    print(f"结果：{i}")
    print(f"内容：{doc.page_content}")
    print(f"元数据：{doc.metadata}")
    print(f"相似度：{similarity:.4f}")
