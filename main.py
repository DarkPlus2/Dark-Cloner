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
    @staticmethod
    async def roles_delete(guild_to: discord.Guild):
        for role in guild_to.roles:
            try:
                if role.name != "@everyone":
                    await role.delete()
                    print_delete(f"Deleted Role: {role.name}")
            except discord.Forbidden:
                print_error(f"Error While Deleting Role: {role.name}")
            except discord.HTTPException:
                print_error(f"Unable to Delete Role: {role.name}")

    @staticmethod
    async def roles_create(guild_to: discord.Guild, guild_from: discord.Guild):
        roles = []
        role: discord.Role
        for role in guild_from.roles:
            if role.name != "@everyone":
                roles.append(role)
        roles = roles[::-1]
        for role in roles:
            try:
                await guild_to.create_role(
                    name=role.name,
                    permissions=role.permissions,
                    colour=role.colour,
                    hoist=role.hoist,
                    mentionable=role.mentionable
                )
                print_add(f"Created Role {role.name}")
            except discord.Forbidden:
                print_error(f"Error While Creating Role: {role.name}")
            except discord.HTTPException:
                print_error(f"Unable to Create Role: {role.name}")

    @staticmethod
    async def channels_delete(guild_to: discord.Guild):
        for channel in guild_to.channels:
            try:
                await channel.delete()
                print_delete(f"Deleted Channel: {channel.name}")
            except discord.Forbidden:
                print_error(f"Error While Deleting Channel: {channel.name}")
            except discord.HTTPException:
                print_error(f"Unable To Delete Channel: {channel.name}")

    @staticmethod
    async def categories_create(guild_to: discord.Guild, guild_from: discord.Guild):
        channels = guild_from.categories
        channel: discord.CategoryChannel
        new_channel: discord.CategoryChannel
        for channel in channels:
            try:
                overwrites_to = {}
                for key, value in channel.overwrites.items():
                    role = discord.utils.get(guild_to.roles, name=key.name)
                    overwrites_to[role] = value
                new_channel = await guild_to.create_category(
                    name=channel.name,
                    overwrites=overwrites_to)
                await new_channel.edit(position=channel.position)
                print_add(f"Created Category: {channel.name}")
            except discord.Forbidden:
                print_error(f"Error While Deleting Category: {channel.name}")
            except discord.HTTPException:
                print_error(f"Unable To Delete Category: {channel.name}")

    @staticmethod
    async def channels_create(guild_to: discord.Guild, guild_from: discord.Guild):
        channel_text: discord.TextChannel
        channel_voice: discord.VoiceChannel
        category = None
        for channel_text in guild_from.text_channels:
            try:
                for category in guild_to.categories:
                    try:
                        if category.name == channel_text.category.name:
                            break
                    except AttributeError:
                        print_warning(f"Channel {channel_text.name} doesn't have any category!")
                        category = None
                        break

                overwrites_to = {}
                for key, value in channel_text.overwrites.items():
                    role = discord.utils.get(guild_to.roles, name=key.name)
                    overwrites_to[role] = value
                try:
                    new_channel = await guild_to.create_text_channel(
                        name=channel_text.name,
                        overwrites=overwrites_to,
                        position=channel_text.position,
                        topic=channel_text.topic,
                        slowmode_delay=channel_text.slowmode_delay,
                        nsfw=channel_text.nsfw)
                except:
                    new_channel = await guild_to.create_text_channel(
                        name=channel_text.name,
                        overwrites=overwrites_to,
                        position=channel_text.position)
                if category is not None:
                    await new_channel.edit(category=category)
                print_add(f"Created Text Channel: {channel_text.name}")
            except discord.Forbidden:
                print_error(f"Error While Creating Text Channel: {channel_text.name}")
            except discord.HTTPException:
                print_error(f"Unable To Creating Text Channel: {channel_text.name}")
            except:
                print_error(f"Error While Creating Text Channel: {channel_text.name}")

        category = None
        for channel_voice in guild_from.voice_channels:
            try:
                for category in guild_to.categories:
                    try:
                        if category.name == channel_voice.category.name:
                            break
                    except AttributeError:
                        print_warning(f"Channel {channel_voice.name} doesn't have any category!")
                        category = None
                        break

                overwrites_to = {}
                for key, value in channel_voice.overwrites.items():
                    role = discord.utils.get(guild_to.roles, name=key.name)
                    overwrites_to[role] = value
                try:
                    new_channel = await guild_to.create_voice_channel(
                        name=channel_voice.name,
                        overwrites=overwrites_to,
                        position=channel_voice.position,
                        bitrate=channel_voice.bitrate,
                        user_limit=channel_voice.user_limit,
                        )
                except:
                    new_channel = await guild_to.create_voice_channel(
                        name=channel_voice.name,
                        overwrites=overwrites_to,
                        position=channel_voice.position)
                if category is not None:
                    await new_channel.edit(category=category)
                print_add(f"Created Voice Channel: {channel_voice.name}")
            except discord.Forbidden:
                print_error(f"Error While Creating Voice Channel: {channel_voice.name}")
            except discord.HTTPException:
                print_error(f"Unable To Creating Voice Channel: {channel_voice.name}")
            except:
                print_error(f"Error While Creating Voice Channel: {channel_voice.name}")

    @staticmethod
    async def emojis_delete(guild_to: discord.Guild):
        for emoji in guild_to.emojis:
            try:
                await emoji.delete()
                print_delete(f"Deleted Emoji: {emoji.name}")
            except discord.Forbidden:
                print_error(f"Error While Deleting Emoji{emoji.name}")
            except discord.HTTPException:
                print_error(f"Error While Deleting Emoji {emoji.name}")

    @staticmethod
    async def emojis_create(guild_to: discord.Guild, guild_from: discord.Guild):
        emoji: discord.Emoji
        for emoji in guild_from.emojis:
            try:
                emoji_image = await emoji.url.read()
                await guild_to.create_custom_emoji(
                    name=emoji.name,
                    image=emoji_image)
                print_add(f"Created Emoji {emoji.name}")
            except discord.Forbidden:
                print_error(f"Error While Creating Emoji {emoji.name} ")
            except discord.HTTPException:
                print_error(f"Error While Creating Emoji {emoji.name}")

    @staticmethod
    async def guild_edit(guild_to: discord.Guild, guild_from: discord.Guild):
        try:
            try:
                icon_image = await guild_from.icon_url.read()
            except discord.errors.DiscordException:
                print_error(f"Can't read icon image from {guild_from.name}")
                icon_image = None
            await guild_to.edit(name=f'{guild_from.name}')
            if icon_image is not None:
                try:
                    await guild_to.edit(icon=icon_image)
                    print_add(f"Guild Icon Changed: {guild_to.name}")
                except:
                    print_error(f"Error While Changing Guild Icon: {guild_to.name}")
        except discord.Forbidden:
            print_error(f"Error While Changing Guild Icon: {guild_to.name}")

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
    client = discord.Client()
    
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
