import os
import discord
import asyncio
from discord.ext import commands, tasks
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

# Intents setup
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    schedule_task.start()  # Start the background task


@tasks.loop(seconds=1)
async def schedule_task():
    # sweden tiemzone
    now = datetime.now(timezone.utc) + timedelta(hours=2)
    if now.weekday() == 0 and now.hour == 12 and now.minute == 0:  # Monday at 12:00 UTC
        await send_role_list()


async def send_role_list():
    guild = bot.get_guild(GUILD_ID)
    if not guild:
        print("Guild not found.")
        return

    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        print("Channel not found.")
        return

    role_message = ""
    for role in guild.roles:
        if role.name == "@everyone":  # Skip @everyone role
            continue
        members = [member.display_name for member in role.members]
        if not members:
            continue
        role_message += f"**{role.name}:**\n" + \
            "\n".join(f"- {m}" for m in members) + "\n\n"

    if not role_message:
        await channel.send("No roles with members found.")
        return

    await channel.send(role_message)


bot.run(TOKEN)
