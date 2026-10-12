from fastmcp import FastMCP

mcp = FastMCP("demo")

@mcp.tool()
def add(a, b):
    """两个数相加"""
    return a + b

# 为MCP实例添加资源
@mcp.resource("greeting://default")
def get_greeting():
    return "hello from static resource!"

# 为MCP实例添加提示词
@mcp.prompt()
def greet_user(name: str, style: str = "friendly"):
    styles = {
        "friendly": "写一句友善的问候",
        "formal": "写一句正式的问候",
        "casual": "写一句轻松的问候",
    }
    return f"为{name}{styles[style]}"


if __name__ == "__main__":
    mcp.run(transport="stdio")