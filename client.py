import asyncio
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters
from groq import Groq
from utils import get_response_from_llm
import os
from dotenv import load_dotenv

load_dotenv()

server_info = StdioServerParameters(
    command="uv",
    args=["run", "mcp_server.py"],
    env=None
)


async def main():
    async with stdio_client(server_info) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:

            print(f"Initialized with: {await session.initialize()}")

            tools_response = await session.list_tools()
            print(f"Available tools :{', '.join([t.name for t in tools_response.tools])}")

            query = "How to use start a container ?"
            library = "docker"
            
            
            result = await session.call_tool("get_docs", arguments={'query': query, 'library': library})
            context = result.content[0].text

            # LLM function to create a human readable response 
            SYSTEM_PROMPT = """
            You are a helpful assistant that answers questions about libraries, tools, and general concepts.
            Answer only using the provided context. If info is missing say you dont know.
            Keeep the 'SOURCE:' line exactly same to same
            """

            USER_PROMPT = f"""
            Query: {query}
            Context: {context}
            """
    
            answer = get_response_from_llm(user_prompt=USER_PROMPT,model="llama-3.1-8b-instant",system_prompt=SYSTEM_PROMPT)

            print("Answer : ",answer)

if __name__ == "__main__":
    asyncio.run(main())