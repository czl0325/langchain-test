from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
import os
import httpx
import uvicorn

load_dotenv(encoding="utf-8")
mcp = FastMCP("weather")

@mcp.tool()
def get_weather(loc: str) -> dict:
    """获取指定城市的天气信息"""
    url = "https://api.openweathermap.org/data/2.5/weather"
    query = {
        "q": loc,
        "appid": os.getenv("WEATHER_APIKEY"),
        "units": "metric",
        "lang": "zh-cn",
    }
    response = httpx.get(url, params=query, timeout=60)
    print(f"返回数据：{response}")
    data = response.json()
    return data

if __name__ == "__main__":
    uvicorn.run(mcp.sse_app(), host="0.0.0.0", port=9000)
