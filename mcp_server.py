
from utils import clean_html_to_text

import json
import os
import asyncio
from fastmcp import FastMCP
import httpx


# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
load_dotenv()

mcp = FastMCP("docs")

SERPER_URL = "https://google.serper.dev/search"

async def search(query: str)->dict | None :
    payload = json.dumps({
      "q": query,
      "num":2
    })
    headers = {
      'X-API-KEY': os.getenv("SERPER_API_KEY"),
      'Content-Type': 'application/json'
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(SERPER_URL, data=payload, headers=headers,timeout=30.0)
        response.raise_for_status()
        return response.json()


async def fetch_url(url : str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url,timeout=30.0)
            response.raise_for_status()
            cleaned_response = clean_html_to_text(response.text)

            return cleaned_response
    except Exception as e:
        import sys
        print(f"Error fetching URL {url}: {e}", file=sys.stderr)
        return None
        
docs_urls={
    "langchain":"python.langchain.com/docs/",
    "chromadb":"docs.trychroma.com/",
    "openai":"platform.openai.com/docs/",
    "uv":"docs.astral.sh/uv/",
    "docker":"docs.docker.com/get-started/",
    "redis":"redis.com/docs/get-started/"
}

@mcp.tool()
async def get_docs(query : str, library : str)->str:
    """
    Search the latest docs for a given library and query
    Supports "langchain", "chromadb", "openai", "uv", "docker", "redis"

    Args:
        query: The query for search for (Eg: "How to create a docker container")
        library: the library to search in (Eg: "docker")

    Returns: 
        context string 

    """
    if library not in docs_urls:
        raise ValueError("Library is not supported Currently ")

    base_url = f"site:{docs_urls[library]}"
    search_url = f"{base_url} {query}"
    results = await search(search_url)

    if len(results["organic"]) == 0:
        return "No result found"

    context_list = []
    for result in results['organic']:
        link = result.get("link", "")
        raw_text = await fetch_url(link)
        if raw_text:
            labeled=f'SOURCE = {link}\n\n CONTENT = {raw_text}\n\n---'
            context_list.append(labeled)
        

    return "\n".join(context_list)


def main():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()