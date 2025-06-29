import discord
import asyncio
import aiohttp
import os
import sys
from colorama import Fore, Style, init
from datetime import datetime

init()

# ===== Constants =====
VERSION = "v3.1.0"
AUTHOR = "Dark Cloner Team"

# ===== Logger =====
class Logger:
    @staticmethod
    def timestamp():
        return datetime.now().strftime("%H:%M:%S")

    @staticmethod
    def info(message):
        print(f"{Fore.CYAN}[{Logger.timestamp()}] {message}{Style.RESET_ALL}")

    @staticmethod
    def success(message):
        print(f"{Fore.GREEN}[{Logger.timestamp()}] {message}{Style.RESET_ALL}")

    @staticmethod
    def warning(message):
        print(f"{Fore.YELLOW}[{Logger.timestamp()}] {message}{Style.RESET_ALL}")

    @staticmethod
    def error(message):
        print(f"{Fore.RED}[{Logger.timestamp()}] {message}{Style.RESET_ALL}")

# ===== Banner =====
def show_banner():
    banner = f"""
{Fore.RED}
██████╗  █████╗ ██████╗ ██╗  ██╗ ██████╗██╗  ██╗███████╗██████╗ 
██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝██╔════╝██║  ██║██╔════╝██╔══██╗
██║  ██║███████║██████╔╝█████╔╝ ██║     ███████║█████╗  ██████╔╝
██║  ██║██╔══██║██╔══██╗██╔═██╗ ██║     ██╔══██║██╔══╝  ██╔══██╗
██████╔╝██║  ██║██║  ██║██║  ██╗╚██████╗██║  ██║███████╗██║  ██║
╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
{Fore.BLUE}
PROFESSIONAL SERVER CLONER {VERSION}
{Fore.YELLOW}
• Safe and efficient server cloning
• Detailed logging system
• Supports both bot and user tokens
{Style.RESET_ALL}
"""
    print(banner)

# ===== Cloner Core =====
class DarkCloner:
    def __init__(self, token):
        self.token = token
        self.session = aiohttp.ClientSession()
        self.bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

    async def fetch_image(self, url):
        if not url:
            return None
        try:
            async with self.session.get(url) as response:
                return await response.read()
        except Exception as e:
            Logger.error(f"Failed to fetch image: {e}")
            return None

    async def verify_token(self):
        try:
            await self.bot.login(self.token)
            Logger.success(f"Token verified for user: {self.bot.user.name}")
            await self.bot.close()
            return True
        except Exception as e:
            Logger.error(f"Token verification failed: {e}")
            return False

    async def clone_roles(self, source_guild, target_guild):
        role_map = {}
        for role in sorted(source_guild.roles, key=lambda r: r.position, reverse=True):
            if role.is_default():
                continue
            try:
                new_role = await target_guild.create_role(
                    name=role.name,
                    permissions=role.permissions,
                    color=role.color,
                    hoist=role.hoist,
                    mentionable=role.mentionable
                )
                role_map[role.id] = new_role
                Logger.success(f"Created role: {new_role.name}")
            except Exception as e:
                Logger.error(f"Failed to create role {role.name}: {e}")
        return role_map

    async def clone_channels(self, source_guild, target_guild, role_map):
        # Clone categories first
        category_map = {}
        for category in source_guild.categories:
            try:
                new_category = await target_guild.create_category(
                    name=category.name,
                    position=category.position
                )
                category_map[category.id] = new_category
                Logger.success(f"Created category: {new_category.name}")
            except Exception as e:
                Logger.error(f"Failed to create category {category.name}: {e}")

        # Clone text and voice channels
        for channel in source_guild.channels:
            if not isinstance(channel, discord.CategoryChannel):
                try:
                    parent = category_map.get(channel.category_id)
                    if isinstance(channel, discord.TextChannel):
                        new_channel = await target_guild.create_text_channel(
                            name=channel.name,
                            topic=channel.topic,
                            slowmode_delay=channel.slowmode_delay,
                            nsfw=channel.is_nsfw(),
                            position=channel.position,
                            category=parent
                        )
                    elif isinstance(channel, discord.VoiceChannel):
                        new_channel = await target_guild.create_voice_channel(
                            name=channel.name,
                            bitrate=channel.bitrate,
                            user_limit=channel.user_limit,
                            position=channel.position,
                            category=parent
                        )
                    Logger.success(f"Created channel: {new_channel.name}")
                except Exception as e:
                    Logger.error(f"Failed to create channel {channel.name}: {e}")

    async def clone_emojis(self, source_guild, target_guild):
        for emoji in source_guild.emojis:
            try:
                emoji_data = await self.fetch_image(emoji.url)
                if emoji_data:
                    await target_guild.create_custom_emoji(
                        name=emoji.name,
                        image=emoji_data
                    )
                    Logger.success(f"Created emoji: {emoji.name}")
            except Exception as e:
                Logger.error(f"Failed to create emoji {emoji.name}: {e}")

    async def clone_server(self, source_id, new_name):
        try:
            Logger.info("Starting server cloning process...")
            await self.bot.login(self.token)

            source_guild = self.bot.get_guild(int(source_id))
            if not source_guild:
                Logger.error("Source server not found or bot doesn't have access")
                return False

            Logger.info(f"Cloning server: {source_guild.name}")

            # Create new guild
            icon = await self.fetch_image(source_guild.icon_url)
            new_guild = await self.bot.create_guild(
                name=new_name,
                icon=icon,
                region=source_guild.region
            )
            Logger.success(f"Created new server: {new_guild.name}")

            # Clone components
            await self.clone_roles(source_guild, new_guild)
            await self.clone_channels(source_guild, new_guild)
            await self.clone_emojis(source_guild, new_guild)

            Logger.success("Server cloning completed successfully!")
            return True

        except Exception as e:
            Logger.error(f"Cloning failed: {e}")
            return False
        finally:
            await self.bot.close()

# ===== Menu System =====
async def main_menu():
    while True:
        print(f"\n{Fore.CYAN}=== MAIN MENU ===")
        print(f"{Fore.YELLOW}1. Verify Token")
        print(f"2. Clone Server")
        print(f"3. Server Information")
        print(f"4. Exit{Style.RESET_ALL}")

        choice = input(f"{Fore.CYAN}[?] Select an option: {Style.RESET_ALL}")

        if choice == "1":
            token = input(f"{Fore.CYAN}[?] Enter your token: {Style.RESET_ALL}")
            cloner = DarkCloner(token)
            await cloner.verify_token()

        elif choice == "2":
            token = input(f"{Fore.CYAN}[?] Enter your token: {Style.RESET_ALL}")
            source_id = input(f"{Fore.CYAN}[?] Source server ID: {Style.RESET_ALL}")
            new_name = input(f"{Fore.CYAN}[?] New server name: {Style.RESET_ALL}")

            cloner = DarkCloner(token)
            await cloner.clone_server(source_id, new_name)

        elif choice == "3":
            Logger.info(f"Version: {VERSION}")
            Logger.info(f"Author: {AUTHOR}")
            Logger.info("Features:")
            Logger.info("- Complete server cloning")
            Logger.info("- Role, channel, and emoji duplication")
            Logger.info("- Safe and efficient operations")

        elif choice == "4":
            Logger.success("Exiting Dark Cloner...")
            break

        else:
            Logger.error("Invalid option selected")

# ===== Main Execution =====
if __name__ == "__main__":
    show_banner()
    Logger.info("Initializing Dark Cloner...")
    
    if not os.path.exists('/data/data/com.termux/files/home'):
        Logger.error("This script must be run in Termux")
        sys.exit(1)

    try:
        asyncio.run(main_menu())
    except KeyboardInterrupt:
        Logger.warning("Process interrupted by user")
    except Exception as e:
        Logger.error(f"Fatal error: {e}")
    finally:
        Logger.info("Dark Cloner session ended")
