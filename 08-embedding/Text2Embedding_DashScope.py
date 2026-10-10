from langchain_ollama import OllamaEmbeddings
import dashscope

embeddings = OllamaEmbeddings(base_url="http://localhost:11434", model="embeddinggemma-2:440m")

input_text = "this is a test document"
res = embeddings.embed_query(input_text)
print(f"向量维度: {len(res)}")

doc_results = embeddings.embed_documents([
    "Hi there!",
    "Oh, Hello!",
    "What your name?",
    "My friend call me world",
    "Hello World!",
])
print(doc_results)
print(f"文本向量数量：{len(doc_results)}，向量长度：{len(doc_results[0])}")