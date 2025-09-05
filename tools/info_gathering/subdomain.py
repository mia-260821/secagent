

from dataclasses import dataclass
from tools.info_gathering.base import mcp
from tools.utils import execute_shell, CmdResult


@mcp.tool()
def enumerate_subdomain(domain: str) -> CmdResult:

    result = execute_shell("assetfinder", "-subs-only", domain)
    return result

