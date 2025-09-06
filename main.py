
import asyncio

from app import App


def show_banner():
    import pyfiglet

    banner = fr"""

    {pyfiglet.figlet_format("SECAGENT", font="slant")}
                     
    SECAGENT - Penetration Testing Assistant

    """

    COLOR = "\033[38;5;46m"
    RESET = "\033[0m"
    
    print(f"{COLOR}{banner}{RESET}")
    


async def main():
    show_banner()

    async with App() as app:
        await app.loop()
        

if __name__ == "__main__":
    asyncio.run(main())
