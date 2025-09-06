import anthropic
import typing
import json
from contextlib import AsyncExitStack

import nest_asyncio
nest_asyncio.apply()


import dotenv
dotenv.load_dotenv(".env")

from mcp import ClientSession


class ToolDefinition(typing.TypedDict):
    name: str
    description: str
    input_schema: dict


class App:

    Model = "claude-3-5-haiku-latest"
    MaxTokens = 1024

    def __init__(self):
        # Initialize session and client objects
        self.sessions: typing.List[ClientSession] = []
        self.exit_stack = AsyncExitStack()
        # make sure environmetal variable ANTHROPIC_API_KEY is set
        self.anthropic = anthropic.Anthropic()
        self.available_tools: typing.List[ToolDefinition] = []
        self.tool_to_session: typing.Dict[str, ClientSession] = {}
        
        print("[+] Initialization is done")
    
    async def __aenter__(self):
        await self._connect_to_servers()
        print("[+] Connecting to mcp servers ...")
        return self
    
    async def __aexit__(self, exc_type, exc_value, traceback):
        print("[+] Releaing asychronous resources ...")
        await self._cleanup()
        print("[+] Cleaning is done")

    
    async def _cleanup(self): # new
        """Cleanly close all resources using AsyncExitStack."""
        await self.exit_stack.aclose()

    async def process_query(self, query: str):
        messages = [{'role': 'user', 'content': query}]
        response = self.anthropic.messages.create(
            max_tokens=self.MaxTokens,
            model=self.Model,
            messages=messages, # type: ignore
            tools=self.available_tools, # type: ignore
        ) # type: ignore
        process_query = True
        while process_query:
            assistant_content = []
            for content in response.content:
                assistant_content.append(content)

                if content.type == 'text':
                    print("\U0001F916 >", content.text)
                    if len(response.content) == 1:
                        process_query = False
                
                elif content.type == 'tool_use':
                    messages.append({'role': 'assistant', 'content': assistant_content}) # type: ignore
                    
                    tool_id = content.id
                    tool_args = content.input
                    tool_name = content.name
                    print(f"Calling tool {tool_name} with args {tool_args}")

                    result = await self.tool_to_session[tool_name].call_tool(tool_name, arguments=tool_args) # type: ignore
                    messages.append(
                        {
                            "role": "user", 
                            "content": [
                                anthropic.types.ToolResultBlockParam(
                                    tool_use_id=tool_id, 
                                    type="tool_result", 
                                    content=result.content # type: ignore
                                )
                            ]
                        }
                    )
                    response = self.anthropic.messages.create(
                        max_tokens=self.MaxTokens,
                        model=self.Model, 
                        tools=self.available_tools, # type: ignore
                        messages=messages # type: ignore
                    ) 
                    if len(response.content) == 1 and response.content[0].type == "text":
                        print("\U0001F916 >", response.content[0].text)
                        process_query = False
        pass


    async def _connect_to_server(self, server_name: str, server_config: dict):
            # Create MCP client
            if server_config["type"] == "stdio":
                from mcp import StdioServerParameters, stdio_client
                client = stdio_client(StdioServerParameters(**server_config))
            elif server_config["type"] == "streamable-http":
                from mcp.client.streamable_http import streamablehttp_client
                client = streamablehttp_client(url=server_config["url"])
            elif server_config["type"] == "sse":
                from mcp.client.sse import sse_client
                client = sse_client(url=server_config["url"], headers=server_config.get("headers"))
            else:
                raise Exception(f"Invalid server type {server_config["type"]}")
            
            (read, write, _) = await self.exit_stack.enter_async_context(client) # type: ignore
            session = await self.exit_stack.enter_async_context(ClientSession(read, write))

            # Initialize the connection
            await session.initialize()

            self.sessions.append(session)

            # List available tools
            response = await session.list_tools()
            
            tools = response.tools
            print(f"\nConnected to server {server_name} with tools:", [tool.name for tool in tools])
            
            for tool in tools:
                self.tool_to_session[tool.name] = session
                self.available_tools.append(
                    {
                        "name": tool.name,
                        "description": tool.description, # type: ignore
                        "input_schema": tool.inputSchema
                    }
                )
                
    
    async def _connect_to_servers(self): 
        # Load JSON
        with open("server_config.json", "r") as f:
            data: typing.Dict = json.load(f)['mcpServers']
        
        for server_name, server_config in data.items():
            await self._connect_to_server(server_name, server_config)


    async def loop(self):
        """Run an interactive chat loop"""
        print("\nSecAgent Started!")
        print("Type your queries or 'bye' to exit.")
        
        while True:
            try:
                query = input("\n\U0001F464 > ").strip()

                if len(query) <= 0:
                    continue
        
                if query.lower() == 'bye':
                    print("     Bye!\n")
                    break
                    
                await self.process_query(query)
                print("\n")
                    
            except Exception as e:
                print(f"\nError: {str(e)}")
