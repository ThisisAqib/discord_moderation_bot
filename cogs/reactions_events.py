"""
Reactions Events Cog for the Discord bot.

This cog handles events related to reactions on messages, logging the
details of added, removed, and cleared reactions in a specified channel.
"""

import typing
import discord
from discord.ext import commands
import config
from logger_init import logger


class ReactionsEvents(commands.Cog):
    """Cog for managing reaction-related events."""

    def __init__(self, bot: commands.Bot) -> None:
        """Initialize the ReactionsEvents cog.

        Args:
            bot (commands.Bot): The instance of the Discord bot.
        """
        self.bot = bot

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        """Event listener for when a reaction is added.

        Args:
            reaction (discord.Reaction): The reaction that was added.
            user (discord.User): The user who added the reaction.
        """
        # Avoid logging the bot's own reactions
        if user.bot:
            return

        channel = reaction.message.channel

        logger.info(
            "User %s added a reaction %s in channel %s", user, reaction.emoji, channel
        )

        embed = discord.Embed(
            title="Reaction Added",
            description=f"{user.mention} added a reaction.",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow(),
        )
        embed.add_field(
            name="Message",
            value=f"[Jump to message]({reaction.message.jump_url})",
            inline=False,
        )
        embed.add_field(name="Channel", value=channel.mention, inline=False)
        embed.add_field(name="Emoji", value=str(reaction.emoji), inline=False)
        embed.add_field(name="User", value=user.mention, inline=False)

        update_channel = self.bot.get_channel(config.REACTIONS_UPDATES_CHANNEL_ID)
        if update_channel:
            await update_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction: discord.Reaction, user: discord.User):
        """Event listener for when a reaction is removed.

        Args:
            reaction (discord.Reaction): The reaction that was removed.
            user (discord.User): The user who removed the reaction.
        """
        # Avoid logging the bot's own reactions
        if user.bot:
            return

        channel = reaction.message.channel

        logger.info(
            "User %s removed a reaction %s in channel %s", user, reaction.emoji, channel
        )

        embed = discord.Embed(
            title="Reaction Removed",
            description=f"{user.mention} removed a reaction.",
            color=discord.Color.red(),
            timestamp=discord.utils.utcnow(),
        )
        embed.add_field(
            name="Message",
            value=f"[Jump to message]({reaction.message.jump_url})",
            inline=False,
        )
        embed.add_field(name="Channel", value=channel.mention, inline=False)
        embed.add_field(name="Emoji", value=str(reaction.emoji), inline=False)
        embed.add_field(name="User", value=user.mention, inline=False)

        update_channel = self.bot.get_channel(config.REACTIONS_UPDATES_CHANNEL_ID)
        if update_channel:
            await update_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_reaction_clear(
        self, message: discord.Message, reactions: typing.List[discord.Reaction]
    ):
        """Event listener for when reactions are cleared from a message.

        Args:
            message (discord.Message): The message from which reactions were cleared.
            reactions (typing.List[discord.Reaction]): The list of cleared reactions.
        """
        channel = message.channel

        logger.info("Reactions cleared from message in channel  %s", channel)

        embed = discord.Embed(
            title="Reactions Cleared",
            description="Reactions were cleared from a message.",
            color=discord.Color.orange(),
            timestamp=discord.utils.utcnow(),
        )
        embed.add_field(
            name="Message", value=f"[Jump to message]({message.jump_url})", inline=False
        )
        embed.add_field(name="Channel", value=channel.mention, inline=False)
        embed.add_field(
            name="Cleared Reactions",
            value=", ".join([str(reaction.emoji) for reaction in reactions]),
            inline=False,
        )

        update_channel = self.bot.get_channel(config.REACTIONS_UPDATES_CHANNEL_ID)
        if update_channel:
            await update_channel.send(embed=embed)


async def setup(bot):
    """Set up the ReactionsEvents cog.

    Args:
        bot (commands.Bot): The instance of the Discord bot.
    """
    await bot.add_cog(ReactionsEvents(bot))
