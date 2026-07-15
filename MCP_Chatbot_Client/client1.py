import asyncio
from pathlib import Path # For building a relative path that works regardless of cwd
from langchain_mcp_adapters.client import MultiServerMCPClient # Because we will connect our client with multiple servers
from fastmcp.client.auth import OAuth # Handles the OAuth browser login + token caching for the expense server
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import ToolMessage
 
load_dotenv()
 
# Resolve the calculator server path relative to this file's location,
# so it works no matter where the script is run from.
# client1.py is in .../MCP/MCP_Chatbot_Client/, calculator is a sibling folder in .../MCP/
CALCULATOR_PATH = (
    Path(__file__).resolve().parent.parent
    / "Simple_Calculator_with_Dice_Roll_Local_MCP_Server"
    / "main.py"
)
 
# Config of server which we want to connect with
 
SERVERS = {
    "Calculator": {
        "transport": "stdio",
        "command": "uv",
        "args": [
            "run",
            "fastmcp",
            "run",
            str(CALCULATOR_PATH), # relative-safe path, resolved above
        ],
    },
    # "expense":{
    #     "transport": "streamable_http", # or sse
    #     "url":"https://expense-tracker-shiv0047.fastmcp.app/mcp",
    #     "auth": OAuth(mcp_url="https://expense-tracker-shiv0047.fastmcp.app/mcp"), # opens browser on first run, caches token after
    # }
    # ^ commented out for now — OAuth token exchange gets rejected (401 unauthorized)
    # on the free/Personal FastMCP Cloud plan; needs a higher tier (Developer/Enterprise)
    # that includes "Access user seats" for external OAuth clients to consume this server.
    # Re-enable once the plan is upgraded, or once you confirm with FastMCP Cloud support.
}

async def main():

    client = MultiServerMCPClient(SERVERS) # Create an instance which is our client
    tools = await client.get_tools() # Get tools
    named_tool = {}
    for tool in tools:
        named_tool[tool.name] = tool

    print("Available tools: ", named_tool.keys()) # List of available tools

    llm = ChatGoogleGenerativeAI( #LLM
        model="gemini-2.5-flash",
        temperature=0,
    )

    llm_with_tools = llm.bind_tools(tools) # Bind tools with LLM

    prompt = "What is the product of 12 and 15 using the math tool, add 2 to the result using tool as well" # Prompt that forces use of tool

    messages = [prompt]

    while True:

        response = await llm_with_tools.ainvoke(messages)
        messages.append(response)

        if not getattr(response, "tool_calls", None): # If no tool is needed
            print("\nLLM Reply:", response.content)
            break

        print("Response: ", response) # has LLM calls tools (not use it)

        for tc in response.tool_calls:
            selected_tool = tc["name"] # name of tool to use
            selected_tool_args = tc.get("args") or {} # arguments of tool to use
            tool_call_id = tc["id"] # Id of selected tool

            print(f"\nExecuting remote tool: {selected_tool}")
            tool_result = await named_tool[selected_tool].ainvoke(selected_tool_args) # Select tool and pass its args

            tool_message = ToolMessage(
                content=str(tool_result),
                tool_call_id=tool_call_id,
            ) # Create tool message

            messages.append(tool_message)

if __name__ == '__main__':
    asyncio.run(main()) # Run async main functions