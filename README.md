# Docs MCP Server

A Model Context Protocol (MCP) server that provides a search-and-retrieve tool (`get_docs`) to query and extract clean, relevant information from official documentation sites for modern developer libraries and tools.

## Features

- **Google Serper API Integration**: Queries official documentation sites with specific `site:` constraints.
- **HTML Content Extraction**: Automatically scrapes the top organic search results and converts raw HTML into clean plain text using `trafilatura` (ignoring navigation menus, tables, and footers).
- **Supported Documentation Libraries**:
  - `langchain` (`python.langchain.com/docs/`)
  - `chromadb` (`docs.trychroma.com/`)
  - `openai` (`platform.openai.com/docs/`)
  - `uv` (`docs.astral.sh/uv/`)
  - `docker` (`docs.docker.com/get-started/`)
  - `redis` (`redis.com/docs/get-started/`)
- **Ready-to-Use Client**: Includes a sample client that runs the MCP server via `stdio` transport and utilizes Groq (`llama-3.1-8b-instant`) to synthesize answers from the retrieved documentation context.

---

## Getting Started

### 1. Requirements
Ensure you have the following installed:
- [uv](https://github.com/astral-sh/uv) (Python package manager)
- Python 3.10+

### 2. Environment Configuration
Create a `.env` file in the root directory and add your API keys:
```env
SERPER_API_KEY=your_serper_api_key_here
GROQ_API_KEY=your_groq_api_key_here
```

---

## Usage

### Run the Client Demonstration
The client starts the MCP server as a subprocess, calls the `get_docs` tool for a query, and feeds the context to Groq to generate a final answer:
```bash
uv run client.py
```

### Run the MCP Server directly
To run the stdio server standalone:
```bash
uv run mcp_server.py
```

### Debugging with the MCP Inspector
You can inspect the server, list tools, and execute them using the interactive MCP Inspector:
```bash
npx @modelcontextprotocol/inspector uv run mcp_server.py
```

---

## Claude Desktop Integration

To make this server's tool available to your Claude Desktop client, edit your configuration file:

- **Path**: `~/Library/Application Support/Claude/claude_desktop_config.json`

Add the following to the `mcpServers` object:

```json
{
  "mcpServers": {
    "docs-search": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/roystondsouza/Desktop/mcp-server",
        "run",
        "mcp_server.py"
      ],
      "env": {
        "SERPER_API_KEY": "your_serper_api_key_here",
        "GROQ_API_KEY": "your_groq_api_key_here"
      }
    }
  }
}
```

*Note: Replace `your_serper_api_key_here` and `your_groq_api_key_here` with your actual API keys, or ensure your local environment contains them.*

---

## Project Structure

- `mcp_server.py`: The MCP server implementation exposing the `get_docs` tool.
- `client.py`: The client script that initializes the stdio session, executes the tool, and queries Groq.
- `utils.py`: Contains HTML text extraction and LLM interaction helpers.
