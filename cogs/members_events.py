"""
Members Events Cog for the Discord bot.

This cog handles events related to members in the Discord server, including 
joining, leaving, updating their profiles, banning, and unbanning. It logs these 
events and sends notifications to a specified channel.
"""

import discord
from discord.ext import commands

import config
from logger_init import logger


class MembersEvents(commands.Cog):
    """Cog for managing member-related events."""

    def __init__(self, bot: commands.Bot) -> None:
        """Initialize the MembersEvents cog.

        Args:
            bot (commands.Bot): The instance of the Discord bot.
        """
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Event listener for when a member joins the server.

        Args:
            member (discord.Member): The member who joined the server.
        """
        logger.info("Member joined: %s (%s)", member, member.id)

        # Create a welcome message
        embed = discord.Embed(
            title="Welcome!",
            description=f"Welcome to {member.guild.name}, {member.mention}! "
            "We're glad to have you here.",
            color=discord.Color.green(),
        )

        # Add member's profile picture as a thumbnail
        if member.avatar:
            embed.set_thumbnail(url=member.avatar.url)

        # Send the welcome message to the specified channel
        welcome_channel = self.bot.get_channel(config.MEMBERS_UPDATES_CHANNEL_ID)
        if welcome_channel:
            await welcome_channel.send(embed=embed)
        else:
            logger.warning(
                "Channel with ID %d not found.", config.MEMBERS_UPDATES_CHANNEL_ID
            )

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        """Event listener for when a member leaves the server.

        Args:
            member (discord.Member): The member who left the server.
        """
        # Log the event
        logger.info(
            "Member %s (%d) has left the guild %s.",
            member.name,
            member.id,
            member.guild.name,
        )

        # Prepare the embed
        embed = discord.Embed(
            title="Member Left",
            description=f"{member.mention} has left the server.",
            color=discord.Color.red(),
            timestamp=discord.utils.utcnow(),
        )
        if member.avatar:
            embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="User ID", value=str(member.id), inline=False)
        embed.add_field(
            name="Joined",
            value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"),
            inline=False,
        )
        embed.set_footer(text=f"Member left | {member.guild.name}")

        # Send the embed to the specified channel
        channel = self.bot.get_channel(config.MEMBERS_UPDATES_CHANNEL_ID)
        if channel:
            await channel.send(embed=embed)
        else:
            logger.warning(
                "Members updates channel not found. Please check the channel ID."
            )

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        """Event listener for when a member updates their profile.

        Args:
            before (discord.Member): The member's profile before the update.
            after (discord.Member): The member's profile after the update.
        """
        changes = []

        # Compare nickname
        if before.nick != after.nick:
            changes.append(f"**Nickname:** '{before.nick}' ➔ '{after.nick}'")

        # Compare roles
        before_roles = [role.name for role in before.roles]
        after_roles = [role.name for role in after.roles]
        if set(before_roles) != set(after_roles):
            removed_roles = [role for role in before_roles if role not in after_roles]
            added_roles = [role for role in after_roles if role not in before_roles]
            roles_change = []
            if removed_roles:
                roles_change.append(f"Removed: {', '.join(removed_roles)}")
            if added_roles:
                roles_change.append(f"Added: {', '.join(added_roles)}")
            changes.append(f"**Roles:**\n" + "\n".join(roles_change))

        # Compare pending status
        if before.pending != after.pending:
            changes.append(f"**Pending:** {after.pending}")

        # Compare timeout
        if before.timed_out_until != after.timed_out_until:
            before_timeout = (
                before.timed_out_until.strftime("%Y-%m-%d %H:%M:%S")
                if before.timed_out_until
                else "None"
            )
            after_timeout = (
                after.timed_out_until.strftime("%Y-%m-%d %H:%M:%S")
                if after.timed_out_until
                else "None"
            )
            changes.append(
                f"**Timeout:**\nBefore: {before_timeout} ➔ After: {after_timeout}"
            )

        # Compare guild avatar
        if before.guild_avatar != after.guild_avatar:
            before_guild_avatar_url = (
                "None" if before.guild_avatar is None else before.guild_avatar.url
            )
            after_guild_avatar_url = (
                "None" if after.guild_avatar is None else after.guild_avatar.url
            )
            changes.append(
                f"**Guild Avatar:**\n[Before]({before_guild_avatar_url}) "
                f"➔ [After]({after_guild_avatar_url})"
            )

        # Compare flags
        before_flags = ", ".join([flag.name for flag in before.public_flags.all()])
        after_flags = ", ".join([flag.name for flag in after.public_flags.all()])
        if before_flags != after_flags:
            changes.append(f"**Flags:**\nBefore: {before_flags} ➔ After: {after_flags}")

        # Log changes if any
        if changes:
            # Prepare the embed
            embed = discord.Embed(
                title="Member Updated",
                description=f"{before.mention} was updated.",
                color=discord.Color.blue(),
                timestamp=discord.utils.utcnow(),
            )
            embed.set_thumbnail(
                url=after.avatar.url if after.avatar else after.default_avatar.url
            )

            # Add each change as a separate field
            for i, change in enumerate(changes, 1):
                embed.add_field(name=f"Change {i}", value=change, inline=False)

            embed.set_footer(text=f"Member update | {before.guild.name}")

            # Send the message to the specified channel
            channel = self.bot.get_channel(config.MEMBERS_UPDATES_CHANNEL_ID)
            if channel:
                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_user_update(self, before: discord.User, after: discord.User):
        """Event listener for when a user updates their global profile.

        Args:
            before (discord.User): The user's profile before the update.
            after (discord.User): The user's profile after the update.
        """
        changes = []

        # Compare the username (global name)
        if before.name != after.name:
            changes.append(f"**Username:** '{before.name}' ➔ '{after.name}'")

        # Compare the discriminator
        if before.discriminator != after.discriminator:
            changes.append(
                f"**Discriminator:** '{before.discriminator}' ➔ '{after.discriminator}'"
            )

        # Compare the global avatar
        if before.avatar != after.avatar:
            before_avatar_url = "None" if before.avatar is None else before.avatar.url
            after_avatar_url = "None" if after.avatar is None else after.avatar.url
            changes.append(
                f"**Avatar:** \n[Before]({before_avatar_url}) ➔ [After]({after_avatar_url})"
            )

        # Compare the global name (if applicable)
        if hasattr(before, "global_name") and hasattr(after, "global_name"):
            if before.global_name != after.global_name:
                changes.append(
                    f"**Global Name:** '{before.global_name}' ➔ '{after.global_name}'"
                )

        # Log changes if any
        if changes:
            # Prepare the embed
            embed = discord.Embed(
                title="User Updated",
                description=f"{before.mention} was updated.",
                color=discord.Color.blue(),
                timestamp=discord.utils.utcnow(),
            )
            embed.set_thumbnail(
                url=after.avatar.url if after.avatar else after.default_avatar.url
            )

            # Add each change as a separate field
            for i, change in enumerate(changes, 1):
                embed.add_field(name=f"Change {i}", value=change, inline=False)

            embed.set_footer(text=f"Member update")

            # Send the message to the specified channel
            channel = self.bot.get_channel(config.MEMBERS_UPDATES_CHANNEL_ID)
            if channel:
                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild: discord.Guild, user: discord.User):
        """Event listener for when a member is banned.

        Args:
            guild (discord.Guild): The guild from which the member was banned.
            user (discord.User): The user who was banned.
        """
        logger.info("User unbanned: %s (%s) from %s", user, user.id, guild)

        embed = discord.Embed(
            title="Member Banned",
            description="{} has been banned from {}.".format(user, guild.name),
            color=discord.Color.red(),
        )
        embed.add_field(name="User ID", value=user.id, inline=False)
        if user.avatar:
            embed.set_thumbnail(
                url=user.avatar.url if user.avatar else discord.Embed.Empty
            )

        # Send the embed to the specified channel
        ban_channel = self.bot.get_channel(config.MEMBERS_UPDATES_CHANNEL_ID)
        if ban_channel:
            await ban_channel.send(embed=embed)
        else:
            logger.warning(
                "Ban updates channel not found. Please check the channel ID."
            )

    @commands.Cog.listener()
    async def on_member_unban(self, guild: discord.Guild, user: discord.User):
        """Event listener for when a member is unbanned.

        Args:
            guild (discord.Guild): The guild from which the member was unbanned.
            user (discord.User): The user who was unbanned.
        """
        logger.info("User unbanned: %s (%s) from %s", user, user.id, guild)

        embed = discord.Embed(
            title="Member Unbanned",
            description=f"{user} has been unbanned from {guild.name}.",
            color=discord.Color.green(),
        )
        embed.add_field(name="User ID", value=user.id, inline=False)
        if user.avatar:
            embed.set_thumbnail(
                url=user.avatar.url if user.avatar else discord.Embed.Empty
            )

        # Send the embed to the specified channel
        unban_channel = self.bot.get_channel(config.MEMBERS_UPDATES_CHANNEL_ID)
        if unban_channel:
            await unban_channel.send(embed=embed)
        else:
            logger.warning(
                "Unban updates channel not found. Please check the channel ID."
            )


async def setup(bot: commands.Bot):
    """Load the MembersEvents cog.

    Args:
        bot (discord.ext.commands.Bot): The instance of the Discord bot.
    """
    await bot.add_cog(MembersEvents(bot))
