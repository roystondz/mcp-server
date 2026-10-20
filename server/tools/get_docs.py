from services.doc_search import DOCS_URLS, search, fetch_url

def register_tool(mcp):

    @mcp.tool()
    async def get_docs(query: str, library: str) -> str:
        """Search documentation for a supported library.

        Args:
            query: The documentation question to search for.
            library: The library to search.
        """

        library = library.strip().lower()

        if library not in DOCS_URLS:
            supported = ", ".join(sorted(DOCS_URLS))
            return f"Unsupported library. Supported libraries: {supported}"

        results = await search(
            f"site:{DOCS_URLS[library]} {query}"
        )

        if not results:
            return "No documentation results found."

        context_parts = []

        for result in results[:3]:
            link = result.get("link")

            if not link:
                continue

            content = await fetch_url(link)

            if content:
                context_parts.append(
                    f"SOURCE URL: {link}\n"
                    f"CONTENT:\n{content[:10000]}"
                )

        if not context_parts:
            return "No documentation page content could be retrieved."

        return "\n\n---\n\n".join(context_parts)
