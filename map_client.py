# map_client.py
import asyncio
import asyncio
from dotenv import load_dotenv
import os

# Load environment
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

from mcp import ClientSession
from mcp.client.stdio import stdio_client
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain_mcp_adapters.tools import load_mcp_tools
from mcp.client.stdio import StdioServerParameters

async def main():
    # 1. Define how to launch the server process
    server_params = StdioServerParameters(
        command="python",
        args=["./map_server.py"],  # ← update to your absolute path
    )

    # 2. Launch MCP stdio client
    async with stdio_client(server_params) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            # 3. Initialize & fetch all tools exposed by the server
            await session.initialize()
            tools = await load_mcp_tools(session)

            # 4. Create your custom LangChain agent
            llm = ChatOpenAI(model="gpt-4", temperature=0)
            agent = initialize_agent(
                tools,
                llm,
                agent=AgentType.OPENAI_FUNCTIONS,
                verbose=True,
            )

            # 5. Ask a routing question
            question = "How do I get from the Eiffel Tower to the Louvre?"
            result = await agent.ainvoke({"input": question})
            print("\n→ Agent’s answer:\n", result)

if __name__ == "__main__":
    asyncio.run(main())
