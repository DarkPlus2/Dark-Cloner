import discord
import asyncio
import aiohttp
from discord.ext import commands
import os
import sys
from colorama import Fore, Style, init

# Initialize colorama
init()

# Banner
BANNER = f"""
{Fore.RED}╔╦╗┌─┐┬─┐┌─┐  ╔═╗┌─┐┌┬┐┌─┐┌─┐
 ║ ├┤ ├┬┘├─┤  ╚═╗│ │ ││├┤ └─┐
 ╩ └─┘┴└─┴ ┴  ╚═╝└─┘─┴┘└─┘└─┘
{Fore.BLUE}╔═╗┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐  ╔═╗┌─┐┬─┐┌─┐┌─┐┌┬┐
║  │  ├─┤└─┐ │ ├┤ ├┬┘  ║  │ │├┬┘├─┤└─┐ │ 
╚═╝┴─┘┴ ┴└─┘ ┴ └─┘┴└─  ╚═╝└─┘┴└─┴ ┴└─┘ ┴ 
{Fore.GREEN}
Mega Hyper Ultra Discord Server Cloner
Dark Cloner v3.0 - Ultimate All-in-One
{Style.RESET_ALL}
"""

print(BANNER)

# Initialize bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

async def fetch_image(session, url):
    if not url:
        return None
    async with session.get(url) as response:
        return await response.read()

async def clone_server(source_guild_id, new_guild_name, token):
    try:
        # Connect the bot
        await bot.login(token)
        print(f"{Fore.GREEN}[+] Bot logged in successfully!{Style.RESET_ALL}")

        # Get the source guild
        source_guild = bot.get_guild(int(source_guild_id))
        if not source_guild:
            print(f"{Fore.RED}[!] Source server not found or bot not in server{Style.RESET_ALL}")
            return False

        print(f"{Fore.YELLOW}[*] Starting to clone server: {source_guild.name}{Style.RESET_ALL}")

        # Create new guild
        async with aiohttp.ClientSession() as session:
            icon = await fetch_image(session, source_guild.icon_url)
            new_guild = await bot.create_guild(
                name=new_guild_name,
                icon=icon,
                region=source_guild.region
            )
            print(f"{Fore.GREEN}[+] Created new server: {new_guild.name}{Style.RESET_ALL}")

            # Clone roles
            role_map = {}
            for role in sorted(source_guild.roles, key=lambda r: r.position, reverse=True):
                if role.managed or role.is_default():
                    continue

                new_role = await new_guild.create_role(
                    name=role.name,
                    permissions=role.permissions,
                    color=role.color,
                    hoist=role.hoist,
                    mentionable=role.mentionable
                )
                role_map[role.id] = new_role
                print(f"{Fore.BLUE}[+] Created role: {new_role.name}{Style.RESET_ALL}")

            # Clone categories
            categories = [c for c in source_guild.channels if isinstance(c, discord.CategoryChannel)]
            category_map = {}

            for category in categories:
                overwrites = {}
                for target, overwrite in category.overwrites.items():
                    if isinstance(target, discord.Role):
                        if target.id in role_map:
                            overwrites[role_map[target.id]] = overwrite
                    else:
                        overwrites[target] = overwrite

                new_category = await new_guild.create_category_channel(
                    name=category.name,
                    overwrites=overwrites,
                    position=category.position
                )
                category_map[category.id] = new_category
                print(f"{Fore.CYAN}[+] Created category: {new_category.name}{Style.RESET_ALL}")

            # Clone text and voice channels
            channels = [c for c in source_guild.channels if not isinstance(c, discord.CategoryChannel)]
            
            for channel in channels:
                overwrites = {}
                for target, overwrite in channel.overwrites.items():
                    if isinstance(target, discord.Role):
                        if target.id in role_map:
                            overwrites[role_map[target.id]] = overwrite
                    else:
                        overwrites[target] = overwrite

                parent = category_map.get(channel.category_id, None)
                
                if isinstance(channel, discord.TextChannel):
                    new_channel = await new_guild.create_text_channel(
                        name=channel.name,
                        topic=channel.topic,
                        slowmode_delay=channel.slowmode_delay,
                        nsfw=channel.is_nsfw(),
                        position=channel.position,
                        overwrites=overwrites,
                        category=parent
                    )
                    print(f"{Fore.MAGENTA}[+] Created text channel: {new_channel.name}{Style.RESET_ALL}")
                
                elif isinstance(channel, discord.VoiceChannel):
                    new_channel = await new_guild.create_voice_channel(
                        name=channel.name,
                        bitrate=channel.bitrate,
                        user_limit=channel.user_limit,
                        position=channel.position,
                        overwrites=overwrites,
                        category=parent
                    )
                    print(f"{Fore.MAGENTA}[+] Created voice channel: {new_channel.name}{Style.RESET_ALL}")

            # Clone emojis
            for emoji in source_guild.emojis:
                try:
                    emoji_data = await fetch_image(session, str(emoji.url))
                    await new_guild.create_custom_emoji(
                        name=emoji.name,
                        image=emoji_data,
                        reason="Server clone"
                    )
                    print(f"{Fore.YELLOW}[+] Created emoji: {emoji.name}{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}[!] Failed to clone emoji {emoji.name}: {e}{Style.RESET_ALL}")

            # Clone server settings
            await new_guild.edit(
                afk_channel=next((c for c in new_guild.voice_channels if c.name == source_guild.afk_channel.name), None) if source_guild.afk_channel else None,
                afk_timeout=source_guild.afk_timeout,
                verification_level=source_guild.verification_level,
                default_notifications=source_guild.default_notifications,
                explicit_content_filter=source_guild.explicit_content_filter,
                system_channel=next((c for c in new_guild.text_channels if c.name == source_guild.system_channel.name), None) if source_guild.system_channel else None
            )

            print(f"{Fore.GREEN}\n[+] Server cloning complete!{Style.RESET_ALL}")
            return True

    except Exception as e:
        print(f"{Fore.RED}[!] Error during cloning: {e}{Style.RESET_ALL}")
        return False
    finally:
        await bot.close()

async def main():
    print(f"{Fore.YELLOW}[*] Discord Server Cloner - Ultimate Edition{Style.RESET_ALL}")
    
    # Get user input
    token = input(f"{Fore.CYAN}[?] Enter your bot token: {Style.RESET_ALL}")
    source_id = input(f"{Fore.CYAN}[?] Enter source server ID: {Style.RESET_ALL}")
    new_name = input(f"{Fore.CYAN}[?] Enter new server name: {Style.RESET_ALL}")

    # Start cloning
    print(f"{Fore.YELLOW}\n[*] Starting cloning process...{Style.RESET_ALL}")
    success = await clone_server(source_id, new_name, token)
    
    if success:
        print(f"{Fore.GREEN}[+] Cloning completed successfully!{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}[!] Cloning failed{Style.RESET_ALL}")

if __name__ == "__main__":
    # Check if running in Termux
    if not os.path.exists('/data/data/com.termux/files/home'):
        print(f"{Fore.RED}[!] This script is designed to run in Termux{Style.RESET_ALL}")
        sys.exit(1)
    
    # Run the main function
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
