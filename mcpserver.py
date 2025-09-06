
import sys


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        raise Exception("argument excepted")
    
    print(sys.argv)
    
    mcp_name = sys.argv[1].strip().lower()
    print("[+] MCP selected:", mcp_name)

    if mcp_name == "info_gathering":
        from tools.info_gathering import mcp
        mcp.run(transport="streamable-http")

    elif mcp_name == "kali_terminal":
        from tools.base import mcp
        mcp.run(transport="stdio")

    else:
        raise Exception("invalid mcp name")

