import asyncio
import logging

from dotenv import load_dotenv
from mcp import ClientSession
from mcp.client.stdio import stdio_client

from config import server_info
from utils import generate_llm_response
from .cli import parse_arguments

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    args = parse_arguments()

    async with stdio_client(server_info) as (
        read_stream,
        write_stream,
    ):
        async with ClientSession(
            read_stream, write_stream
        ) as session:
            await session.initialize()
            logger.info("MCP session initialized")

            tools_response = await session.list_tools()
            tool_names = [
                tool.name for tool in tools_response.tools
            ]
            logger.info("Available tools: %s", tool_names)

            result = await session.call_tool(
                "get_docs",
                arguments={
                    "query": args.query,
                    "library": args.library,
                },
            )

            if getattr(result, "isError", False):
                raise RuntimeError(
                    f"MCP tool failed: {result.content}"
                )

            context = "\n".join(
                item.text
                for item in result.content
                if hasattr(item, "text")
            )

            if not context.strip():
                print("No documentation context was returned.")
                return

            answer = generate_llm_response(
                args.query,
                context,
            )

            print("\nAnswer:\n")
            print(answer)


if __name__ == "__main__":
    asyncio.run(main())
