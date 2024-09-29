"""
Messages Events Cog for the Discord bot.

This cog handles events related to message edits and deletions, logging the
details in a specified channel. It utilizes Discord's API to listen for
message events and sends embedded messages to notify about edits and deletions.
"""

import discord
from discord.ext import commands
import config
from logger_init import logger


class MessagesEvents(commands.Cog):
    """Cog for managing message-related events."""

    def __init__(self, bot: commands.Bot) -> None:
        """Initialize the MessagesEvents cog.

        Args:
            bot (commands.Bot): The instance of the Discord bot.
        """
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        """Event listener for when a message is edited.

        Args:
            before (discord.Message): The message before it was edited.
            after (discord.Message): The message after it was edited.
        """
        if before.content == after.content:
            return  # No change in content, no need to log

        logger.info(
            "Message edited by %s in channel %s: Before: '%s', After: '%s'",
            before.author,
            before.channel,
            before.content,
            after.content,
        )

        embed = discord.Embed(
            title="Message Edited",
            description=f"A message by {before.author} was edited.",
            color=discord.Color.orange(),
        )
        embed.add_field(name="Channel", value=before.channel.mention, inline=False)
        embed.add_field(name="Author", value=before.author.mention, inline=False)
        embed.add_field(
            name="Before", value=before.content or "No content", inline=False
        )
        embed.add_field(name="After", value=after.content or "No content", inline=False)

        messages_updates_channel = self.bot.get_channel(
            config.MESSAGES_UPDATES_CHANNEL_ID
        )
        if messages_updates_channel:
            await messages_updates_channel.send(embed=embed)
        else:
            logger.warning(
                "Channel with ID %d not found.", config.MESSAGES_UPDATES_CHANNEL_ID
            )

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        """Event listener for when a message is deleted.

        Args:
            message (discord.Message): The message that was deleted.
        """
        # Skip if the message is in a DM (Direct Message) or if the message has no content
        if isinstance(message.channel, discord.DMChannel) or not message.content:
            return

        logger.info(
            "Message deleted by %s in channel %s: Content: '%s'",
            message.author,
            message.channel,
            message.content,
        )

        embed = discord.Embed(
            title="Message Deleted",
            description=f"A message by {message.author} was deleted.",
            color=discord.Color.red(),
        )
        embed.add_field(name="Channel", value=message.channel.mention, inline=False)
        embed.add_field(name="Author", value=message.author.mention, inline=False)
        embed.add_field(name="Content", value=message.content, inline=False)

        messages_updates_channel = self.bot.get_channel(
            config.MESSAGES_UPDATES_CHANNEL_ID
        )
        if messages_updates_channel:
            await messages_updates_channel.send(embed=embed)
        else:
            logger.warning(
                "Channel with ID %d not found.", config.MESSAGES_UPDATES_CHANNEL_ID
            )


async def setup(bot):
    """Set up the MessagesEvents cog.

    Args:
        bot (commands.Bot): The instance of the Discord bot.
    """
    await bot.add_cog(MessagesEvents(bot))
