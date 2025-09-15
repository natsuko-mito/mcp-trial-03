import asyncio
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.tools import load_mcp_tools
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

server_params = StdioServerParameters(
    command="/Users/hasegawanatsuko/myapp/mcp-trial-02/venv/bin/python",
    args=["/Users/hasegawanatsuko/myapp/mcp-trial-02/src/aws_updates.py"]
)

async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
          await session.initialize()

          agent = create_react_agent(
              model="anthropic:claude-4-sonnet-20250514",
              tools=await load_mcp_tools(session)
          )

          response = await agent.ainvoke(
              {"messages": "Amazon Bedrockのアップデート情報を教えてください。" }
          )
          print(response["messages"][-1].content)

asyncio.run(main())
