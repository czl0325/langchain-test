from langchain.agents import create_agent
from langchain.tools import tool
from langchain_ollama import ChatOllama

PRODUCT_DATABASE = {
    "无线耳机": [
        {"id": "WH-1000XM5", "name": "索尼 WH-1000XM5", "popularity": 95, "price": 299},
        {"id": "QC45", "name": "Bose QuietComfort 45", "popularity": 88, "price": 329},
        {"id": "AIRMAX", "name": "果 AirPods Max", "popularity": 92, "price": 549},
        {"id": "PXC550", "name": "森海塞尔 PXC 550", "popularity": 76, "price": 299},
        {"id": "HT450", "name": "JBL Tune 76ONC", "popularity": 82, "price": 99}
    ],
    "游戏鼠标": [
        {"id": "GPW", "name": "罗技 G Pro 无线", "popularity": 90, "price": 129},
        {"id": "VIPER", "name": "雷 Viper V2 Pro", "popularity": 87, "price": 149},
        {"id": "DAV3", "name": "雷 DeathAdder V3", "popularity": 85, "price": 119}
    ],
    "笔记本电脑": [
        {"id": "MBP14", "name": "MacBook Pro 14英寸", "popularity": 94, "price": 1999},
        {"id": "XPS13", "name": "ThinkPad X1 Carbon", "popularity": 86, "price": 1499},
        {"id": "TPX1", "name": "戴尔 XPS 13", "popularity": 89, "price": 1299}
    ]
}
# 模拟库存数据库
INVENTORY_DATABASE = {
    "WH-1000XM5":{"stock":10,"location":"仓库-A"},
    "QC45":{"stock":0,"location":"仓库-B"},
    "AIRMAX":{"stock":5,"location":"仓库-C"},
    "PXC550":{"stock":15, "location":"仓库-A"},
    "HT450":{"stock":25, "location":"仓库-B"},
    "GPW":{"stock":8, "location":"仓库-C"},
    "VIPER":{"stock": 12, "location":"仓库-A"},
    "DAV3":{"stock":3,"location":"仓库-B"},
    "MBP14":{"stock":7, "location":"仓库-C"},
    "XPS13":{"stock":0,"location":"仓库-A"},
    "TPX1":{"stock":4,"location":"仓库-B"}
}

@tool
def search_products(query: str) -> str:
    """根据关键词搜索商品，返回匹配商品列表（按热度排序）"""
    print(f"[工具调用]search_products: {query}")
    results = []
    for category, products in PRODUCT_DATABASE.items():
        if query in category or category in query:
            results.extend(products)
    if not results:
        return f"未找到与'{query}'相关的商品"
    results.sort(key=lambda p: p["popularity"], reverse=True)
    lines = []
    for p in results:
        lines.append(f"ID:{p['id']} | {p['name']} | 热度:{p['popularity']} | 价格:${p['price']}")
    return "\n".join(lines)


@tool
def check_inventory(product_id: str) -> str:
    """根据产品ID查询库存信息"""
    print(f"[工具调用]check_inventory: {product_id}")
    if product_id in INVENTORY_DATABASE:
        stock = INVENTORY_DATABASE[product_id]["stock"]
        status = "有库存" if stock > 0 else "缺货"
        return f"产品：{product_id} {status} ({stock}件库存) - 位置：{INVENTORY_DATABASE[product_id]['location']}"
    else:
        return "没有查询到商品"



model = ChatOllama(base_url="http://localhost:11434", model="qwen3:8b", reasoning=False)
agent = create_agent(model, tools=[search_products, check_inventory], system_prompt="""你是电商助手，遵循ReAct模式：1.先推理用户的需求。2.选择合适的工具进行操作。3.基于工具结果进行下一步推理。4.重复直到获得完整答案。保持推理步骤简洁明了。""")
result = agent.invoke({
    "messages": [{"role": "user", "content": "查询当前最受欢迎的无线耳机并查询是否有库存？"}]
})
print(result['messages'][-1].content)
