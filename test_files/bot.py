"""
Discord Bot to manage channels and guild events.

This bot uses the Discord API to manage various events related to channels, 
guilds, messages, members, reactions, and roles. The bot loads its functionalities 
as extensions (cogs) and can respond to events in real-time.

Features include:
- Asynchronous loading of extensions
- Logging of events and actions
- Graceful shutdown on user interruption

To run the bot, ensure that the BOT_TOKEN is set in the configuration.
"""

import asyncio

import discord
from discord.ext import commands

import config
from logger_init import logger

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


async def load_extensions():
    """Load all the cogs/extensions asynchronously."""
    extensions = [
        "cogs.channels_events",
        "cogs.guilds_events",
        "cogs.messages_events",
        "cogs.members_events",
        "cogs.reactions_events",
        "cogs.roles_events",
    ]

    for ext in extensions:
        await bot.load_extension(ext)
        logger.info("Loaded extension %s", ext)


@bot.event
async def on_ready():
    """Triggered when the bot has successfully logged in."""
    logger.info("Bot is ready. Logged in as %s", bot.user)
    await load_extensions()

    # Uncomment these if you want to run the testers
    # asyncio.create_task(testers.channels_tester(bot))
    # asyncio.create_task(testers.guilds_tester(bot))
    # asyncio.create_task(testers.messages_tester(bot))
    # asyncio.create_task(testers.members_tester(bot))


async def main():
    """Run the bot and handle any shutdowns or reloads."""
    try:
        await bot.start(config.BOT_TOKEN)
    except KeyboardInterrupt:
        logger.info("Bot is shutting down...")
        await bot.close()


if __name__ == "__main__":
    asyncio.run(main())
