# Map MCP Adapters

A simple demonstration of exposing geocoding and routing tools via an MCP server, and consuming them with a custom LangChain agent.

## Project Structure

```
├── map_server.py      # MCP server exposing geocode and get_directions tools
├── map_client.py      # LangChain client loading MCP tools and running an agent
└── README.md          # This file
```

## Prerequisites

- Python 3.8+
- An OpenAI API key set in `OPENAI_API_KEY`
- Dependencies:

  - `mcp` (Model Context Protocol SDK)
  - `langchain-mcp-adapters`
  - `langchain` (with OpenAI support)
  - `langgraph` (prebuilt agents)
  - `geopy` (for geocoding)

Install with:

```bash
pip install mcp langchain-mcp-adapters langchain[openai] langgraph geopy
```

## 1. Running the MCP Server

The server exposes two tools:

- `geocode(address: str) -> {latitude, longitude}`
- `get_directions(start: str, end: str) -> List[str]`

Start the server on stdio transport:

```bash
python map_server.py
```

> **Tip:** To use HTTP streaming, change `mcp.run(transport="stdio")` to `mcp.run(transport="streamable-http", port=3000)`.

## 2. Running the LangChain Client

The client spins up the MCP server, loads its tools, and wires them into a React agent.

```bash
python map_client.py
```

Update the path to `map_server.py` in `map_client.py` as needed. The client will print a natural‑language answer, e.g.:

```
→ Agent’s answer:
 1. Head north from the Eiffel Tower
 2. ...
```

## 3. Customization

- **Multiple Servers**: Use `MultiServerMCPClient` to combine tools from several MCP servers (e.g., weather, maps).
- **HTTP Transport**: Switch to `streamable-http` and use `streamablehttp_client` for non‑blocking requests.
- **Agent Types**: Swap `AgentType.ZERO_SHOT_REACT_DESCRIPTION` for other built‑in or custom agent templates.

### 🧪 Sample Output

```bash
> Entering new AgentExecutor chain...

Invoking: `get_directions` with `{'start': 'Eiffel Tower', 'end': 'Louvre'}`

Processing request of type CallToolRequest
['1. Head north from Eiffel Tower', '2. Turn right onto Main St', '3. Continue until you reach Louvre', '4. You have arrived.']
Here are the directions from the Eiffel Tower to the Louvre:

1. Head north from the Eiffel Tower.
2. Turn right onto Main St.
3. Continue until you reach the Louvre.
4. You have arrived.

## License

MIT © 2025
```
