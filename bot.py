import discord
import asyncio
from discord.ext import commands

import settings
import testers

logger = settings.logging.getLogger("bot")

def run():
    bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

    @bot.event
    async def on_ready():
        logger.info('Bot is ready')
        # asyncio.create_task(testers.channels_tester(bot))
        # asyncio.create_task(testers.guilds_tester(bot))
        # asyncio.create_task(testers.messages_tester(bot))
        # asyncio.create_task(testers.members_tester(bot))

        await bot.load_extension(f"cogs.channels_events")
        await bot.load_extension(f"cogs.guilds_events")
        await bot.load_extension(f"cogs.messages_events")
        await bot.load_extension(f"cogs.members_events")
        await bot.load_extension(f"cogs.reactions_events")
        await bot.load_extension(f"cogs.roles_events")


    bot.run(token=settings.BOT_TOKEN, root_logger=False)

if __name__=='__main__':
    run()