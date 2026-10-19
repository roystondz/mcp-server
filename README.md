# Docs MCP Server

A Model Context Protocol (MCP) server that provides a search-and-retrieve tool (`get_docs`) to query and extract clean, relevant information from official documentation sites for modern developer libraries and tools.

---

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

## Project Structure

```
mcp-server/
├── client/
│   ├── __init__.py
│   ├── client.py          # Main client implementation
│   ├── cli.py             # Command-line interface for the client
│   └── tests/             # Tests for the client
│       ├── __init__.py
│       └── test_client.py
├── server/
│   ├── __init__.py
│   ├── mcp_server.py      # MCP server implementation
│   ├── tools/             # Additional tools for the server
│   │   ├── __init__.py
│   │   └── get_docs.py    # Implementation of the `get_docs` tool
│   └── tests/             # Tests for the server
│       ├── __init__.py
│       └── test_server.py
├── utils/
│   ├── __init__.py
│   ├── utils.py           # Utility functions
│   ├── llm_helpers.py     # LLM-related helper functions
│   └── tests/             # Tests for utilities
│       ├── __init__.py
│       └── test_utils.py
├── config.py              # Configuration for server and client
├── .env                   # Environment variables
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
└── pyproject.toml         # Project configuration
```

---

## Getting Started

### 1. Requirements
Ensure you have the following installed:
- [uv](https://github.com/astral-sh/uv) (Python package manager)
- Python 3.12+
- API keys for:
  - **Google Serper API**: `SERPER_API_KEY`
  - **Groq API**: `GROQ_API_KEY`

### 2. Environment Configuration
Create a `.env` file in the root directory and add your API keys:
```env
SERPER_API_KEY=your_serper_api_key_here
GROQ_API_KEY=your_groq_api_key_here
```

---

## Usage

### Run the MCP Server
To start the MCP server:
```bash
uv run server/mcp_server.py
```

### Run the Client
To query the server using the client:
```bash
python client/client.py --query "How to start a Docker container?" --library "docker"
```

### Debugging with the MCP Inspector
You can inspect the server, list tools, and execute them using the interactive MCP Inspector:
```bash
npx @modelcontextprotocol/inspector uv run server/mcp_server.py
```

---

## Running Tests

### Run All Tests
To run all tests for the project:
```bash
python -m unittest discover
```

### Run Specific Tests
To run tests for a specific module (e.g., `utils`):
```bash
python -m unittest utils.tests.test_utils
```

---

## Docker (Optional)

### Build the Docker Image
To containerize the application:
```bash
docker build -t mcp-server .
```

### Run the Docker Container
To run the server inside a Docker container:
```bash
docker run -p 8000:8000 mcp-server
```

---

## Contribution Guidelines

1. Fork the repository.
2. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add feature-name"
   ```
4. Push to your branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

---

## License
This project is licensed under the MIT License.