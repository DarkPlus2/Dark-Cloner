import os
import platform
import discord
import asyncio
import colorama
from colorama import Fore, init, Style

# Initialize colorama
colorama.init()

# Print functions with colors
def print_add(message):
    print(f'{Fore.GREEN}[+]{Style.RESET_ALL} {message}')

def print_delete(message):
    print(f'{Fore.RED}[-]{Style.RESET_ALL} {message}')

def print_warning(message):
    print(f'{Fore.YELLOW}[!]{Style.RESET_ALL} {message}')

def print_error(message):
    print(f'{Fore.RED}[ERROR]{Style.RESET_ALL} {message}')

def print_info(message):
    print(f'{Fore.CYAN}[*]{Style.RESET_ALL} {message}')

class Clone:
    # ... [Keep all your existing Clone class methods exactly as they are] ...

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_banner():
    print(f"""{Fore.RED}

                                    ██╗░░░░░██╗░░░██╗░█████╗░  ░█████╗░██╗░░░░░░█████╗░███╗░░██╗███████╗██████╗░
                                    ██║░░░░░██║░░░██║██╔══██╗  ██╔══██╗██║░░░░░██╔══██╗████╗░██║██╔════╝██╔══██╗
                                    ██║░░░░░██║░░░██║███████║  ██║░░╚═╝██║░░░░░██║░░██║██╔██╗██║█████╗░░██████╔╝
                                    ██║░░░░░██║░░░██║██╔══██║  ██║░░██╗██║░░░░░██║░░██║██║╚████║██╔══╝░░██╔══██╗
                                    ███████╗╚██████╔╝██║░░██║  ╚█████╔╝███████╗╚█████╔╝██║░╚███║███████╗██║░░██║
                                    ╚══════╝░╚═════╝░╚═╝░░╚═╝  ░╚════╝░╚══════╝░╚════╝░╚═╝░░╚══╝╚══════╝╚═╝░░╚═╝
{Style.RESET_ALL}""")

def show_menu():
    print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗")
    print(f"║ {Fore.MAGENTA}ULTIMATE HYPER ULTRA LUA CLONER v4.0{Fore.CYAN}                                    ║")
    print(f"║══════════════════════════════════════════════════════════════════════════════║")
    print(f"║ {Fore.YELLOW}1. Clone Server Structure                                       {Fore.CYAN}║")
    print(f"║ {Fore.YELLOW}2. Clone Server with Emojis                                     {Fore.CYAN}║")
    print(f"║ {Fore.YELLOW}3. Clone Server with Webhooks (Coming Soon)                     {Fore.CYAN}║")
    print(f"║ {Fore.YELLOW}4. Nuke Server (Coming Soon)                                    {Fore.CYAN}║")
    print(f"║ {Fore.YELLOW}5. Exit                                                         {Fore.CYAN}║")
    print(f"╚══════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    print(f"\n{Fore.GREEN}Credits: Dark | NotSaksh#6969 | Ultimate Lua Team{Style.RESET_ALL}\n")

async def clone_server(client, input_guild_id, output_guild_id, clone_emojis=False):
    try:
        print_info(f"Logged In as: {client.user}")
        print_info("Starting Server Clone Process...")
        
        guild_from = client.get_guild(int(input_guild_id))
        guild_to = client.get_guild(int(output_guild_id))
        
        print_info("Editing server settings...")
        await Clone.guild_edit(guild_to, guild_from)
        
        print_info("Deleting existing roles...")
        await Clone.roles_delete(guild_to)
        
        print_info("Deleting existing channels...")
        await Clone.channels_delete(guild_to)
        
        print_info("Creating new roles...")
        await Clone.roles_create(guild_to, guild_from)
        
        print_info("Creating categories...")
        await Clone.categories_create(guild_to, guild_from)
        
        print_info("Creating channels...")
        await Clone.channels_create(guild_to, guild_from)
        
        if clone_emojis:
            print_info("Deleting existing emojis...")
            await Clone.emojis_delete(guild_to)
            
            print_info("Creating new emojis...")
            await Clone.emojis_create(guild_to, guild_from)
        
        print(f"""{Fore.GREEN}

                                        ░█████╗░██╗░░░░░░█████╗░███╗░░██╗███████╗██████╗░
                                        ██╔══██╗██║░░░░░██╔══██╗████╗░██║██╔════╝██╔══██╗
                                        ██║░░╚═╝██║░░░░░██║░░██║██╔██╗██║█████╗░░██║░░██║
                                        ██║░░██╗██║░░░░░██║░░██║██║╚████║██╔══╝░░██║░░██║
                                        ╚█████╔╝███████╗╚█████╔╝██║░╚███║███████╗██████╔╝
                                        ░╚════╝░╚══════╝░╚════╝░╚═╝░░╚══╝╚══════╝╚═════╝░

                                        █▄█ █▀█ █░█ █ █▄░█ █▀▀ █▀
                                        ░█░ █▄█ █▄█ █ █░▀█ ██▄ ▄█

                                        {Style.RESET_ALL}""")
        print_info("Server cloned successfully! Exiting in 5 seconds...")
        await asyncio.sleep(5)
    except Exception as e:
        print_error(f"An error occurred: {str(e)}")

def main():
    # Set up Discord intents
    intents = discord.Intents.default()
    intents.guilds = True
    intents.members = True  # Needed if you want to work with members later
    
    client = discord.Client(intents=intents)
    
    # Clear screen and show banner
    clear_screen()
    show_banner()
    show_menu()
    
    option = input(f'{Fore.BLUE}Select an option (1-5): {Style.RESET_ALL}')

    if option == "1":
        token = input(f'{Fore.YELLOW}Please enter your token:\n > {Style.RESET_ALL}')
        guild_s = input(f'{Fore.YELLOW}Please enter guild id you want to copy:\n > {Style.RESET_ALL}')
        guild = input(f'{Fore.YELLOW}Please enter guild id where you want to copy:\n > {Style.RESET_ALL}')
        
        @client.event
        async def on_ready():
            await clone_server(client, guild_s, guild)
            await client.close()
        
        client.run(token, bot=False)
    
    elif option == "2":
        token = input(f'{Fore.YELLOW}Please enter your token:\n > {Style.RESET_ALL}')
        guild_s = input(f'{Fore.YELLOW}Please enter guild id you want to copy:\n > {Style.RESET_ALL}')
        guild = input(f'{Fore.YELLOW}Please enter guild id where you want to copy:\n > {Style.RESET_ALL}')
        
        @client.event
        async def on_ready():
            await clone_server(client, guild_s, guild, clone_emojis=True)
            await client.close()
        
        client.run(token, bot=False)
    
    elif option == "5":
        print_info("Exiting Ultimate Lua Cloner...")
        exit()
    else:
        print_warning("This feature is coming soon! Stay tuned for updates!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_error("\nOperation cancelled by user")
    except Exception as e:
        print_error(f"An unexpected error occurred: {str(e)}")
