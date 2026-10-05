# 分支链demo

from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableBranch

english_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一位英语翻译专家，你叫小英"),
    ("human", "{question}")
])

japanese_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一位日语翻译专家，你叫小日"),
    ("human", "{question}")
])

korean_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一位韩语翻译专家，你叫小韩"),
    ("human", "{question}")
])

def determine_language(inputs):
    query = inputs["question"]
    if "日语" in query:
        return "japanese"
    elif "韩语" in query:
        return "korean"
    else:
        return "english"

model = ChatOllama(base_url="http://localhost:11434", model="qwen3:8b", reasoning=False)

test_queries = [
    {"question": "请用英语翻译：见到你很开心"},
    {"question": "请用日语翻译：见到你很开心"},
    {"question": "请用韩语翻译：见到你很开心"},
]

parser = StrOutputParser()

chain = RunnableBranch(
    (lambda x: determine_language(x) == "japanese", japanese_prompt | model | parser),
    (lambda x: determine_language(x) == "korean", korean_prompt | model | parser),
    english_prompt | model | parser,  # type: ignore[arg-type]
)


for test_query in test_queries:
    lang = determine_language(test_query)
    if lang == "japanese":
        chatPromptTemplate = japanese_prompt
    elif lang == "korean":
        chatPromptTemplate = korean_prompt
    else:
        chatPromptTemplate = english_prompt
    format_messages = chatPromptTemplate.format_messages(**test_query)
    print(format_messages)
    for msg in format_messages:
        print(f"{msg.type}: {msg.content}")
    result = chain.invoke(test_query)
    print(result)
