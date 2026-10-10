import base64
import httpx
import numpy as np
from pathlib import Path

OLLAMA_URL = "http://localhost:11434"
MODEL = "embeddinggemma-2:440m"


def embed_text(text: str) -> list[float]:
    """文本向量化"""
    res = httpx.post(f"{OLLAMA_URL}/api/embed", json={
        "model": MODEL,
        "input": text,
    }, timeout=30)
    return res.json()["embeddings"][0]


def embed_image(image_path: str) -> list[float]:
    """图像向量化"""
    img_data = Path(image_path).read_bytes()
    img_b64 = base64.b64encode(img_data).decode()
    res = httpx.post(f"{OLLAMA_URL}/api/embed", json={
        "model": MODEL,
        "images": [img_b64],
    }, timeout=30)
    return res.json()["embeddings"][0]


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """计算余弦相似度"""
    va, vb = np.array(a), np.array(b)
    return float(np.dot(va, vb) / (np.linalg.norm(va) * np.linalg.norm(vb)))


# 文本向量化
text_vec = embed_text("一只猫在沙发上睡觉")
print(f"文本向量维度: {len(text_vec)}")

# 图像向量化（需要准备一张图片）
image_vec = embed_image("cat.jpg")
print(f"图像向量维度: {len(image_vec)}")

# 计算文本与图像的相似度
sim = cosine_similarity(text_vec, image_vec)
print(f"文本与图像的相似度: {sim:.4f}")
