import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model


load_dotenv(encoding="utf-8")
llm = init_chat_model(
    model="glm-4.7",
    model_provider="openai",
    api_key=os.getenv("ZP_APIKEY"),
    base_url="https://open.bigmodel.cn/api/paas/v4",
)
res = llm.invoke("你是谁？")
print(res)