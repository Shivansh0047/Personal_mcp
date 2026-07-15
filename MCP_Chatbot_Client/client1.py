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

    prompt = "What is the product of 12 and 15 using the math tool" # Prompt that forces use of tool
    response = await llm_with_tools.ainvoke(prompt)

    if not getattr(response, "tool_calls", None): # If no tool is needed
        print("\nLLM Reply:", response.content)
        return

    print("Response: ", response) # has LLM calls tools (not use it)

    selected_tool = response.tool_calls[0]["name"] # name of tool to use
    selected_tool_args = response.tool_calls[0]["args"] # arguments of tool to use
    tool_call_id = response.tool_calls[0]["id"] # Id of selected tool

    tool_result = await named_tool[selected_tool].ainvoke(selected_tool_args) # Select tool and pass its args

    print(tool_result)

    tool_message = ToolMessage(content=tool_result,tool_call_id=tool_call_id,) # Create toll message

    final_response = await llm_with_tools.ainvoke([prompt, response, tool_message]) # Pass entire history

    print(final_response.content)

if __name__ == '__main__':
    asyncio.run(main()) # Run async main functions