
from dotenv import load_dotenv
from fastmcp import FastMCP

from server.tools import register_docs_tools, register_code_examples_tools

load_dotenv()

mcp = FastMCP("_My_Personal_Jarvis_")

register_docs_tools(mcp)
register_code_examples_tools(mcp)

def main():
    mcp.run(transport="stdio")

# def main():
#     mcp.run(transport="http", host="127.0.0.1", port=8000)

if __name__ == "__main__":
    main()
