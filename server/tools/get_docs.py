
import logging
import os

import httpx
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

SERPER_URL = "https://google.serper.dev/search"

DOCS_URLS = {
    "langchain": "python.langchain.com/docs/",
    "chromadb": "docs.trychroma.com/",
    "openai": "platform.openai.com/docs/",
    "uv": "docs.astral.sh/uv/",
    "docker": "docs.docker.com/get-started/",
    "redis": "redis.com/docs/get-started/",
}


async def search(query: str) -> list[dict]:
    """Search Serper and return organic search results."""

    api_key = os.getenv("SERPER_API_KEY")

    if not api_key:
        raise RuntimeError("SERPER_API_KEY is missing from .env")

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            SERPER_URL,
            json={"q": query, "num": 2},
            headers={"X-API-KEY": api_key},
        )
        response.raise_for_status()

        data = response.json()
        return data.get("organic", [])


async def fetch_url(url: str) -> str | None:
    """Fetch a page and convert its HTML to readable text."""

    from utils.utils import clean_html_to_text

    try:
        async with httpx.AsyncClient(
            timeout=30.0,
            follow_redirects=True,
        ) as client:
            response = await client.get(url)
            response.raise_for_status()

            return clean_html_to_text(response.text)

    except (httpx.HTTPError, ValueError) as exc:
        logger.warning("Could not fetch %s: %s", url, exc)
        return None


def register_tools(mcp):
    """Register documentation tools on the supplied FastMCP instance."""

    @mcp.tool()
    async def get_docs(query: str, library: str) -> str:
        """
        Search documentation for a supported library.

        Args:
            query: The documentation question to search for.
            library: One of langchain, chromadb, openai, uv,
                     docker, or redis.

        Returns:
            Retrieved documentation context with source URLs.
        """
        library = library.strip().lower()

        if library not in DOCS_URLS:
            supported = ", ".join(sorted(DOCS_URLS))
            raise ValueError(
                f"Unsupported library '{library}'. "
                f"Supported libraries: {supported}"
            )

        search_query = f"site:{DOCS_URLS[library]} {query}"
        results = await search(search_query)

        if not results:
            return "No search results found."

        context_list = []

        for result in results:
            link = result.get("link")

            if not link:
                continue

            raw_text = await fetch_url(link)

            if raw_text:
                context_list.append(
                    f"SOURCE = {link}\n\n"
                    f"CONTENT = {raw_text}\n\n---"
                )

        if not context_list:
            return "Search succeeded, but no page content could be retrieved."

        return "\n\n".join(context_list)
