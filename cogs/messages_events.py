import discord
import asyncio
import discord.ext
import discord.ext.commands
import settings
from discord.ext import commands

logger = settings.logging.getLogger("bot")

class MessagesEvents(commands.Cog):
    def __init__(self, bot: discord.ext.commands.Bot) -> None:
        self.bot = bot 

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if before.content == after.content:
            return  # No change in content, no need to log

        embed = discord.Embed(
            title="Message Edited",
            description=f"A message by {before.author} was edited.",
            color=discord.Color.orange()
        )
        embed.add_field(name="Channel", value=before.channel.mention, inline=False)
        embed.add_field(name="Author", value=before.author.mention, inline=False)
        embed.add_field(name="Before", value=before.content or "No content", inline=False)
        embed.add_field(name="After", value=after.content or "No content", inline=False)

        messages_updates_channel = self.bot.get_channel(settings.MESSAGES_UPDATES_CHANNEL_ID)
        if messages_updates_channel:
            await messages_updates_channel.send(embed=embed)
        else:
            logger.warning(f"Channel with ID {settings.MESSAGES_UPDATES_CHANNEL_ID} not found.")

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        # Skip if the message is in a DM (Direct Message) or if the message has no content
        if isinstance(message.channel, discord.DMChannel) or not message.content:
            return

        embed = discord.Embed(
            title="Message Deleted",
            description=f"A message by {message.author} was deleted.",
            color=discord.Color.red()
        )
        embed.add_field(name="Channel", value=message.channel.mention, inline=False)
        embed.add_field(name="Author", value=message.author.mention, inline=False)
        embed.add_field(name="Content", value=message.content, inline=False)

        messages_updates_channel = self.bot.get_channel(settings.MESSAGES_UPDATES_CHANNEL_ID)
        if messages_updates_channel:
            await messages_updates_channel.send(embed=embed)
        else:
            logger.warning(f"Channel with ID {settings.MESSAGES_UPDATES_CHANNEL_ID} not found.")

async def setup(bot):
    await bot.add_cog(MessagesEvents(bot))
