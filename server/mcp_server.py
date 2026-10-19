
from dotenv import load_dotenv
from fastmcp import FastMCP

from server.tools import register_tools

load_dotenv()

mcp = FastMCP("_My_Personal_Jarvis_")

register_tools(mcp)

def main():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
