
import asyncio

from app import App


def show_banner():
    RED = "\033[91m"
    RESET = "\033[0m"

    banner = r"""
    ____             _                        
    / ___|  ___   ___| | __ _ _ __   ___ _ __ 
    \___ \ / _ \ / __| |/ _` | '_ \ / _ \ '__|
    ___) | (_) | (__| | (_| | | | |  __/ |   
    |____/ \___/ \___|_|\__,_|_| |_|\___|_|   
                                            
    SECAGENT - Penetration Testing Assistant
    """
    
    print(f"{RED}{banner}{RESET}", "\n")
    


async def main():
    show_banner()
    await App().connect_to_server_and_run()
  


if __name__ == "__main__":
    asyncio.run(main())
