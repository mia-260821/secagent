import anthropic
import typing
import json

import nest_asyncio
nest_asyncio.apply()


import dotenv
dotenv.load_dotenv(".env")

from mcp import ClientSession, StdioServerParameters, stdio_client


def load_server_params(server_name: str = "default-server") -> StdioServerParameters:
    # Load JSON
    with open("mcpserver.json", "r") as f:
        config = json.load(f)['mcpServers']

    server_params = StdioServerParameters(**config[server_name])
    return server_params


class App:

    Model = "claude-3-5-haiku-latest"
    MaxTokens = 1024

    def __init__(self):
        # Initialize session and client objects
        self.session: typing.Union[ClientSession, None] = None 
        # make sure environmetal variable ANTHROPIC_API_KEY is set
        self.anthropic = anthropic.Anthropic()
        self.available_tools: typing.List[anthropic.types.ToolUnionParam] = []

    async def process_query(self, query: str):
        messages = [{'role': 'user', 'content': query}]
        response = self.anthropic.messages.create(
            max_tokens=self.MaxTokens,
            model=self.Model,
            messages=messages, # type: ignore
            tools=self.available_tools,
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
                    
                    result = await self.session.call_tool(tool_name, arguments=tool_args) # type: ignore
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
                        tools=self.available_tools,
                        messages=messages # type: ignore
                    ) 
                    if len(response.content) == 1 and response.content[0].type == "text":
                        print("\U0001F916 >", response.content[0].text)
                        process_query = False
        pass


    async def connect_to_server_and_run(self):
            # Create server parameters for stdio connection
            server_params = load_server_params()
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:

                    self.session = session
                    # Initialize the connection
                    await session.initialize()
        
                    # List available tools
                    response = await session.list_tools()
                    
                    tools = response.tools
                    print("\nConnected to server with tools:", [tool.name for tool in tools])
                    
                    self.available_tools = [ # type: ignore
                        dict(
                            name=tool.name,
                            description=tool.description,
                            input_schema=tool.inputSchema
                        ) for tool in response.tools
                    ]
        
                    await self.loop()

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
