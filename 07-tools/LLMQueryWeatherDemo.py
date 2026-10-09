from langchain_core.output_parsers import JsonOutputKeyToolsParser, StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.runnables import RunnableLambda
from QueryWeatherTool import get_weather

model = ChatOllama(base_url="http://localhost:11434", model="qwen3:8b", reasoning=False)
llm = model.bind_tools([get_weather])
parser = JsonOutputKeyToolsParser(key_name=get_weather.name, first_tool_only=True)
weather_chain = llm | parser | get_weather
output_prompt = PromptTemplate.from_template(
    """你将收到一段 JS0N格式的天气数据{weather_json}，请用简洁自然的方式将其转述给用户。
    以下是天气JSON 数据:
    请将其转换为中文天气描述，例如:“北京现在天气:多云，气温28°C，体感能见度很好，大约10公里。建议穿短袖
    有点闷热(约32°C)，湿度75%，微风(东南风2米/秒)，
    短裤。适合做户外运动。""")
output_parser = StrOutputParser()
output_chain = output_prompt | llm | output_parser

full_chain = weather_chain | RunnableLambda(lambda x: { "weather_json": x }) | output_chain
result = full_chain.invoke("今天厦门天气如何")
print(result)
