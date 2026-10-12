import json

from langchain_community.document_loaders import JSONLoader

file_path = "assets/hotel.json"
json_data = JSONLoader(file_path=file_path, jq_schema=".", text_content=False).load()

# JSONLoader 内部用 ensure_ascii=True 序列化，中文被转义成 \uXXXX；解析回原始对象再重新序列化
for doc in json_data:
    parsed = json.loads(doc.page_content)
    doc.page_content = json.dumps(parsed, ensure_ascii=False, indent=2)

print(json_data)
