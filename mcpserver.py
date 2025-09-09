
import sys


def main():
    if len(sys.argv) <= 1:
        raise Exception("argument excepted")
    
    print(sys.argv)
    
    mcp_name = sys.argv[1].strip().lower()
    print("[+] MCP selected:", mcp_name)

    host, port = "127.0.0.1", 8000 
    if len(sys.argv) >= 3:
        host_port = sys.argv[2].split(":")
        host = host_port[0]
        port = int(host_port[1])
        print(f"[+] listening on {host}:{port}")

    if mcp_name == "kali_terminal":
        from tools.kali.base import server
    else:
        raise Exception("invalid mcp name")

    # Start server
    server.settings.host = host 
    server.settings.port = port

    server.run(transport="streamable-http")



if __name__ == "__main__":
    main()
