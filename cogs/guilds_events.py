"""
Guilds Events Cog for the Discord bot.

This cog handles events related to the creation and deletion of invites 
within a guild. It logs details of each invite event and sends notifications 
to a specified channel, providing comprehensive information about the changes.
"""

import discord
from discord.ext import commands
import config
from logger_init import logger


class GuildsEvents(commands.Cog):
    """Cog for managing guild-related events."""

    def __init__(self, bot: commands.Bot) -> None:
        """Initialize the GuildsEvents cog.

        Args:
            bot (commands.Bot): The instance of the Discord bot.
        """
        self.bot = bot

    @commands.Cog.listener()
    async def on_invite_create(self, invite: discord.Invite):
        """Event listener for when an invite is created.

        Args:
            invite (discord.Invite): The invite that was created.
        """
        logger.info(
            "Invite created: %s by %s for %s",
            invite.code,
            invite.inviter,
            invite.channel,
        )

        # Create an embed for the invite creation
        embed = discord.Embed(
            title="Invite Created",
            description=f"An invite code **{invite.code}** was created.",
            color=discord.Color.blue(),  # Use blue to indicate creation
        )
        embed.add_field(
            name="Inviter",
            value=invite.inviter.mention if invite.inviter else "Unknown",
            inline=False,
        )
        embed.add_field(
            name="Channel",
            value=invite.channel.mention if invite.channel else "Unknown",
            inline=False,
        )

        max_age_value = f"{invite.max_age} seconds" if invite.max_age else "Never"
        embed.add_field(name="Max Age", value=max_age_value, inline=False)

        max_uses_value = str(invite.max_uses) if invite.max_uses > 0 else "Unlimited"
        embed.add_field(name="Max Uses", value=max_uses_value, inline=False)

        embed.add_field(
            name="Temporary Membership",
            value="Yes" if invite.temporary else "No",
            inline=False,
        )
        embed.add_field(name="Uses", value=str(invite.uses), inline=False)
        embed.add_field(name="URL", value=invite.url, inline=False)

        if invite.target_type:
            embed.add_field(
                name="Target Type", value=str(invite.target_type), inline=False
            )

        if invite.target_user:
            embed.add_field(
                name="Target User",
                value=invite.target_user.mention if invite.target_user else "None",
                inline=False,
            )

        if invite.target_application:
            embed.add_field(
                name="Target Application",
                value=invite.target_application.name,
                inline=False,
            )

        if invite.expires_at:
            embed.add_field(
                name="Expires At",
                value=invite.expires_at.strftime("%Y-%m-%d %H:%M:%S"),
                inline=False,
            )

        # Retrieve the channel to send the update
        invite_channel = self.bot.get_channel(config.GUILDS_UPDATES_CHANNEL_ID)
        if invite_channel:
            await invite_channel.send(embed=embed)
            logger.info("Notification sent for invite creation.")
        else:
            logger.warning(
                "Channel with ID %s not found.", config.GUILDS_UPDATES_CHANNEL_ID
            )

    @commands.Cog.listener()
    async def on_invite_delete(self, invite: discord.Invite):
        """Event listener for when an invite is deleted.

        Args:
            invite (discord.Invite): The invite that was deleted.
        """
        logger.info("Invite deleted: %s for %s", invite.code, invite.channel)

        # Create an embed for the invite deletion
        embed = discord.Embed(
            title="Invite Deleted",
            description=f"An invite code **{invite.code}** was deleted.",
            color=discord.Color.red(),
        )
        embed.add_field(
            name="Channel",
            value=invite.channel.mention if invite.channel else "Unknown",
            inline=False,
        )

        # Retrieve the channel to send the update
        invite_channel = self.bot.get_channel(config.GUILDS_UPDATES_CHANNEL_ID)
        if invite_channel:
            await invite_channel.send(embed=embed)
            logger.info("Notification sent for invite deletion.")
        else:
            logger.warning(
                "Channel with ID %s not found.", config.GUILDS_UPDATES_CHANNEL_ID
            )


async def setup(bot):
    """Set up the GuildsEvents cog.

    Args:
        bot (discord.ext.commands.Bot): The instance of the Discord bot.
    """
    await bot.add_cog(GuildsEvents(bot))
