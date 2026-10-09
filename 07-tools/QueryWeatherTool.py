import httpx
import json
import os
from langchain.tools import tool
from dotenv import load_dotenv

load_dotenv(encoding="utf-8")

CITY_NAME_MAP = {
    "北京": "Beijing", "上海": "Shanghai", "广州": "Guangzhou",
    "深圳": "Shenzhen", "杭州": "Hangzhou", "成都": "Chengdu",
    "武汉": "Wuhan", "南京": "Nanjing", "重庆": "Chongqing",
    "西安": "Xi'an", "天津": "Tianjin", "苏州": "Suzhou",
    "长沙": "Changsha", "郑州": "Zhengzhou", "青岛": "Qingdao",
    "大连": "Dalian", "厦门": "Xiamen", "昆明": "Kunming",
    "哈尔滨": "Harbin", "沈阳": "Shenyang",
}

@tool
def get_weather(loc):
    """获取天气，loc 为城市名称（中文或英文均可）"""
    loc = CITY_NAME_MAP.get(loc, loc)
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



# result = get_weather.invoke({"loc": "beijing"})
# print(result)