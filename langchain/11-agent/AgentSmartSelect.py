from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from mcp.server.fastmcp import FastMCP
import os
import httpx

load_dotenv(encoding="utf-8")

model = ChatOllama(base_url="http://localhost:11434", model="qwen3:8b", reasoning=False)
mcp = FastMCP("weather")


@mcp.tool()
def get_weather(loc: str) -> dict:
    """获取指定城市的天气信息，loc参数为城市名称，必须使用用户原文中的城市名（如London、Chicago），不要翻译或替换"""
    url = "https://api.openweathermap.org/data/2.5/weather"
    query = {"q": loc, "appid": os.getenv("WEATHER_APIKEY"), "units": "metric", "lang": "zh-cn", }
    response = httpx.get(url, params=query, timeout=60)
    data = response.json()
    return data


agent = create_agent(model, [get_weather], system_prompt="你是一个天气助手。重要规则：调用get_weather时，loc参数必须使用用户原文中提到的城市名称，保持原始语言，不要翻译、不要替换成其他城市。当用户询问多个城市天气时，分别调用工具获取数据并进行比较。")
result = agent.invoke({"input": "London和Chicago哪个城市更热？请查询这两个城市的天气并比较。"})
print(result["messages"][-1].content)
