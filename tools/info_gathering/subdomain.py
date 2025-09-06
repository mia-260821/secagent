

from dataclasses import dataclass
from tools.info_gathering.base import mcp
from tools.utils import execute_shell, CmdResult


@mcp.tool()
def enumerate_subdomain(domain: str) -> CmdResult:
    return execute_shell("assetfinder", "-subs-only", domain)


@mcp.tool()
def enumerate_url_dir(url: str, cookie: str = "", header: str = "", ignore_http_code: str = "") -> CmdResult:
    cmd = ["dirb", url]
 
    if cookie:
        cmd.extend(["-c", cookie])
    if header:
        cmd.extend(["-H", header])
    if ignore_http_code:
        cmd.extend(["-N", ignore_http_code])

    return execute_shell(*cmd)


@mcp.tool()
def discover_host(subnet: str) -> CmdResult:
    cmd = ["nmap", "-sn", subnet]
    return execute_shell(*cmd)


@mcp.tool()
def scan_ports(ip: str) -> CmdResult:
    cmd = ["nmap", "-p-", ip]
    return execute_shell(*cmd)


@mcp.tool()
def enumerate_services(ip: str) -> CmdResult:
    cmd = ["nmap", "-sV", ip]
    return execute_shell(*cmd)

