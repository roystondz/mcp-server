from pathlib import Path
from mcp import StdioServerParameters

PROJECT_ROOT = Path(__file__).resolve().parent

server_info = StdioServerParameters(
    command="uv",
    args=[
        "run",
        "--directory",
        str(PROJECT_ROOT),
        "python",
        "-m",
        "server.mcp_server",
    ],
    env=None,
)
