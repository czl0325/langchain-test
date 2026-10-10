from langchain_ollama import OllamaEmbeddings
import numpy as np

embeddings = OllamaEmbeddings(base_url="http://localhost:11434", model="embeddinggemma-2:440m")
texts = [
    "我喜欢吃苹果",
    "苹果是我最喜欢吃的水果",
    "我喜欢用苹果手机"
]

def cosine_similarity(a: list[float], b: list[float]) -> float:
    """计算余弦相似度"""
    va, vb = np.array(a), np.array(b)
    return float(np.dot(va, vb) / (np.linalg.norm(va) * np.linalg.norm(vb)))

vectors = embeddings.embed_documents(texts)

print(f"{'':>20} | {texts[0]:>12} | {texts[1]:>12} | {texts[2]:>12}")
print("-" * 70)
for i, t in enumerate(texts):
    sims = [cosine_similarity(vectors[i], vectors[j]) for j in range(len(texts))]
    print(f"{t:>16} | {sims[0]:>10.4f} | {sims[1]:>10.4f} | {sims[2]:>10.4f}")

print("\n各对文本的余弦相似度：")
pairs = [(0, 1), (0, 2), (1, 2)]
for i, j in pairs:
    sim = cosine_similarity(vectors[i], vectors[j])
    print(f"  \"{texts[i]}\" vs \"{texts[j]}\" => {sim:.4f}")