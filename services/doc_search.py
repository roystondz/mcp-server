
import logging
import os

import httpx
from utils.utils import clean_html_to_text

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
    api_key = os.getenv("SERPER_API_KEY")

    if not api_key:
        raise RuntimeError("SERPER_API_KEY is missing.")

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            SERPER_URL,
            json={"q": query, "num": 3},
            headers={"X-API-KEY": api_key},
        )
        response.raise_for_status()

        data = response.json()
        return data.get("organic", [])


async def fetch_url(url: str) -> str | None:
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
