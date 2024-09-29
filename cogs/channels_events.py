"""
Channels Events Cog for the Discord bot.

This cog handles events related to channel creation, deletion, and updates 
within a guild. It logs details of each channel event and sends notifications 
to a specified channel, providing comprehensive information about the changes.
"""

import discord
from discord.ext import commands
import config
from logger_init import logger


class ChannelsEvents(commands.Cog):
    """Cog for managing channel-related events."""

    def __init__(self, bot: commands.Bot) -> None:
        """Initialize the ChannelsEvents cog.

        Args:
            bot (commands.Bot): The instance of the Discord bot.
        """
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: discord.abc.GuildChannel):
        """Event listener for when a new channel is created.

        Args:
            channel (discord.abc.GuildChannel): The channel that was created.
        """
        logger.info("Created %s, category: %s", channel.name, channel.category)

        embed = discord.Embed(
            title="Channel Created",
            description=f"Channel **{channel.mention}** was created.",
            color=discord.Color.green(),
        )

        category_name = channel.category.name if channel.category else "No Category"
        embed.add_field(name="Category", value=category_name)

        # Retrieve the channel to send the update
        channel_updates_channel = self.bot.get_channel(
            config.CHANNELS_UPDATES_CHANNEL_ID
        )
        if channel_updates_channel:
            await channel_updates_channel.send(embed=embed)
            logger.info("Notification sent for channel creation.")
        else:
            logger.warning(
                "Channel with ID %s not found.", config.CHANNELS_UPDATES_CHANNEL_ID
            )

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: discord.abc.GuildChannel):
        """Event listener for when a channel is deleted.

        Args:
            channel (discord.abc.GuildChannel): The channel that was deleted.
        """
        logger.info("Deleted %s, category: %s", channel.name, channel.category)

        embed = discord.Embed(
            title="Channel Deleted",
            description=f"Channel **{channel.name}** was deleted.",
            color=discord.Color.red(),
        )

        category_name = channel.category.name if channel.category else "No Category"
        embed.add_field(name="Category", value=category_name)

        # Retrieve the channel to send the update
        channel_updates_channel = self.bot.get_channel(
            config.CHANNELS_UPDATES_CHANNEL_ID
        )
        if channel_updates_channel:
            await channel_updates_channel.send(embed=embed)
            logger.info("Notification sent for channel deletion.")
        else:
            logger.warning(
                "Channel with ID %s not found.", config.CHANNELS_UPDATES_CHANNEL_ID
            )

    @commands.Cog.listener()
    async def on_guild_channel_update(
        self, before: discord.abc.GuildChannel, after: discord.abc.GuildChannel
    ):
        """Event listener for when a channel is updated.

        Args:
            before (discord.abc.GuildChannel): The channel before the update.
            after (discord.abc.GuildChannel): The channel after the update.
        """
        changes = []

        # Get all attribute names
        all_attributes = set(dir(before)) | set(dir(after))

        # Filter out methods and private attributes
        all_attributes = [
            attr
            for attr in all_attributes
            if not callable(getattr(before, attr, None)) and not attr.startswith("_")
        ]

        # Compare each attribute
        for attr in all_attributes:
            before_value = getattr(before, attr, None)
            after_value = getattr(after, attr, None)
            if before_value != after_value:
                changes.append(
                    f"{attr} changed from '{before_value}' to '{after_value}'"
                )

        # Output the changes
        if changes:
            logger.info("Channel '%s' was updated:", before.mention)
            embed = discord.Embed(
                title="Channel Updated",
                description=f"Channel **{before.mention}** was updated.",
                color=discord.Color.orange(),  # Color to signify an update
            )

            for change in changes:
                embed.add_field(name="Change Detected", value=change, inline=False)
                logger.info("  - %s", change)

            # Retrieve the channel to send the update
            channel_updates_channel = self.bot.get_channel(
                config.CHANNELS_UPDATES_CHANNEL_ID
            )
            if channel_updates_channel:
                await channel_updates_channel.send(embed=embed)
                logger.info("Notification sent for channel update.")
            else:
                logger.warning(
                    "Channel with ID %s not found.", config.CHANNELS_UPDATES_CHANNEL_ID
                )
        else:
            logger.info(
                "Channel '%s' was updated, but no significant changes were detected.",
                before.name,
            )


async def setup(bot):
    """Set up the ChannelsEvents cog.

    Args:
        bot (discord.ext.commands.Bot): The instance of the Discord bot.
    """
    await bot.add_cog(ChannelsEvents(bot))
