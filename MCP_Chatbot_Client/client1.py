import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient # Because we will connect our client with multiple servers
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import ToolMessage

load_dotenv()

# Config of server which we want to connect with

SERVERS = {
    "Calculator": {
        "transport": "stdio",
        "command": "uv",
        "args": [
            "run",
            "fastmcp",
            "run",
            r"D:\Coding\AL_ML\MCP\Simple_Calculator_with_Dice_Roll_Local_MCP_Server\main.py",
        ],
    }
}

async def main():

    client = MultiServerMCPClient(SERVERS) # Create an instance which is our client
    tools = await client.get_tools() # Get tools
    named_tool = {}
    for tool in tools:
        named_tool[tool.name] = tool

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