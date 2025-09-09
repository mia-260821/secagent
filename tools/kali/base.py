

from mcp.server.fastmcp import FastMCP
from tools.utils import execute_shell, CmdResult


server = FastMCP("kali_terminal")


@server.tool(
    name="Remote Shell",
    description=(
        "This tool provides access to a Kali Linux environment where the current user can execute "
        "commands with `sudo` privileges without requiring a password. "
        "Please avoid installing new software; only use pre-installed tools and commands. "
        "Exercise caution and adhere to ethical hacking practices."
    )
)
def remote_shell(command: str) -> CmdResult:
    return execute_shell(*command.split(' '))

