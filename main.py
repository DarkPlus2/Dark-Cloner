import discord
import asyncio
import aiohttp
import os
import sys
from colorama import Fore, Style, init

init()

# ===== BANNER =====
BANNER = f"""
{Fore.RED}
██████╗  █████╗ ██████╗ ██╗  ██╗ ██████╗██╗  ██╗███████╗██████╗ 
██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝██╔════╝██║  ██║██╔════╝██╔══██╗
██║  ██║███████║██████╔╝█████╔╝ ██║     ███████║█████╗  ██████╔╝
██║  ██║██╔══██║██╔══██╗██╔═██╗ ██║     ██╔══██║██╔══╝  ██╔══██╗
██████╔╝██║  ██║██║  ██║██║  ██╗╚██████╗██║  ██║███████╗██║  ██║
╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
{Fore.BLUE}
MEGA ULTRA HYPER DARK CLONER v5.0
{Fore.YELLOW}
- Supports BOT & USER tokens
- Full Server Copy (Roles, Channels, Emojis, Settings)
- Webhook & Ban Cloning
{Style.RESET_ALL}
"""

print(BANNER)

# ===== CONFIG =====
USE_USER_TOKEN = True  # Set False for bot token
CLONE_BANS = False     # Enable if you have perms
CLONE_WEBHOOKS = False # Enable if needed

# ===== CLONER CLASS =====
class DarkCloner:
    def __init__(self, token):
        self.token = token
        self.session = aiohttp.ClientSession()
        self.bot = commands.Bot(command_prefix="!", intents=discord.Intents.all(), self_bot=USE_USER_TOKEN)

    async def fetch_image(self, url):
        if not url: return None
        async with self.session.get(url) as r:
            return await r.read()

    async def clone_server(self, source_id, new_name):
        try:
            await self.bot.login(self.token)
            print(f"{Fore.GREEN}[+] Logged in as {self.bot.user.name}{Style.RESET_ALL}")

            source = self.bot.get_guild(int(source_id))
            if not source:
                print(f"{Fore.RED}[!] Server not found!{Style.RESET_ALL}")
                return False

            print(f"{Fore.YELLOW}[*] Cloning {source.name}...{Style.RESET_ALL}")

            # Create new server
            icon = await self.fetch_image(source.icon_url)
            new_guild = await self.bot.create_guild(name=new_name, icon=icon)
            print(f"{Fore.GREEN}[+] Created: {new_guild.name}{Style.RESET_ALL}")

            # Clone roles
            role_map = {}
            for role in sorted(source.roles, key=lambda r: r.position, reverse=True):
                if role.is_default(): continue
                new_role = await new_guild.create_role(
                    name=role.name,
                    permissions=role.permissions,
                    color=role.color,
                    hoist=role.hoist,
                    mentionable=role.mentionable
                )
                role_map[role.id] = new_role
                print(f"{Fore.BLUE}[+] Role: {new_role.name}{Style.RESET_ALL}")

            # Clone categories & channels
            for category in source.categories:
                new_category = await new_guild.create_category(category.name)
                for channel in category.channels:
                    if isinstance(channel, discord.TextChannel):
                        await new_guild.create_text_channel(
                            name=channel.name,
                            topic=channel.topic,
                            nsfw=channel.is_nsfw(),
                            slowmode_delay=channel.slowmode_delay,
                            category=new_category
                        )
                    elif isinstance(channel, discord.VoiceChannel):
                        await new_guild.create_voice_channel(
                            name=channel.name,
                            bitrate=channel.bitrate,
                            user_limit=channel.user_limit,
                            category=new_category
                        )
                    print(f"{Fore.CYAN}[+] Channel: {channel.name}{Style.RESET_ALL}")

            # Clone emojis
            for emoji in source.emojis:
                emoji_data = await self.fetch_image(emoji.url)
                await new_guild.create_custom_emoji(name=emoji.name, image=emoji_data)
                print(f"{Fore.MAGENTA}[+] Emoji: {emoji.name}{Style.RESET_ALL}")

            # Clone bans (if enabled)
            if CLONE_BANS:
                bans = await source.bans()
                for ban in bans:
                    try:
                        await new_guild.ban(ban.user, reason=ban.reason)
                        print(f"{Fore.RED}[+] Banned: {ban.user.name}{Style.RESET_ALL}")
                    except: pass

            print(f"{Fore.GREEN}\n[✔] SERVER CLONED SUCCESSFULLY!{Style.RESET_ALL}")
            return True

        except Exception as e:
            print(f"{Fore.RED}[!] ERROR: {e}{Style.RESET_ALL}")
            return False
        finally:
            await self.session.close()
            await self.bot.close()

# ===== MAIN =====
async def main():
    token = input(f"{Fore.CYAN}[?] Enter token: {Style.RESET_ALL}")
    source_id = input(f"{Fore.CYAN}[?] Source server ID: {Style.RESET_ALL}")
    new_name = input(f"{Fore.CYAN}[?] New server name: {Style.RESET_ALL}")

    cloner = DarkCloner(token)
    await cloner.clone_server(source_id, new_name)

if __name__ == "__main__":
    if not os.path.exists('/data/data/com.termux/files/home'):
        print(f"{Fore.RED}[!] Run in Termux!{Style.RESET_ALL}")
        sys.exit(1)
    asyncio.run(main())
