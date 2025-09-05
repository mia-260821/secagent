

from mcp.server.fastmcp import FastMCP
from tools.utils import execute_shell, CmdResult

mcp = FastMCP("kali_terminal")


@mcp.tool()
def remote_shell(command: str) -> CmdResult:
    return execute_shell(command)


