"""
Roles Events Cog for the Discord bot.

This cog handles events related to role creation, deletion, and updates 
within a guild. It logs details of each role event and sends notifications 
to a specified channel, providing comprehensive information about the changes.
"""

import discord
from discord.ext import commands

import config
from logger_init import logger


class RolesEvents(commands.Cog):
    """Cog for managing role-related events."""

    def __init__(self, bot: commands.Bot) -> None:
        """Initialize the RolesEvents cog.

        Args:
            bot (discord.ext.commands.Bot): The instance of the Discord bot.
        """
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_role_create(self, role: discord.Role):
        """Event listener for when a new role is created.

        Args:
            role (discord.Role): The role that was created.
        """
        embed = discord.Embed(
            title="Role Created",
            description="A new role has been created.",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow(),
        )
        embed.add_field(name="Role Name", value=role.name, inline=False)
        embed.add_field(name="Role ID", value=role.id, inline=False)
        embed.add_field(name="Permissions", value=str(role.permissions), inline=False)
        embed.add_field(name="Position", value=role.position, inline=False)

        update_channel = self.bot.get_channel(config.ROLES_UPDATES_CHANNEL_ID)
        if update_channel:
            await update_channel.send(embed=embed)
            logger.info("Role created: %s (ID: %s)", role.name, role.id)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: discord.Role):
        """Event listener for when a role is deleted.

        Args:
            role (discord.Role): The role that was deleted.
        """
        embed = discord.Embed(
            title="Role Deleted",
            description="A role has been deleted.",
            color=discord.Color.red(),
            timestamp=discord.utils.utcnow(),
        )
        embed.add_field(name="Role Name", value=role.name, inline=False)
        embed.add_field(name="Role ID", value=role.id, inline=False)

        update_channel = self.bot.get_channel(config.ROLES_UPDATES_CHANNEL_ID)
        if update_channel:
            await update_channel.send(embed=embed)
            logger.info("Role deleted: %s (ID: %s)", role.name, role.id)

    @commands.Cog.listener()
    async def on_guild_role_update(self, before: discord.Role, after: discord.Role):
        """Event listener for when a role is updated.

        Args:
            before (discord.Role): The role before the update.
            after (discord.Role): The role after the update.
        """
        changes = []

        if before.name != after.name:
            changes.append(f"Name changed from '{before.name}' to '{after.name}'")
        if before.permissions != after.permissions:
            changes.append(
                f"Permissions changed from '{before.permissions}' to '{after.permissions}'"
            )
        if before.position != after.position:
            changes.append(
                f"Position changed from '{before.position}' to '{after.position}'"
            )

        embed = discord.Embed(
            title="Role Updated",
            description=f"Role '{after.name}' was updated.",
            color=discord.Color.orange(),
            timestamp=discord.utils.utcnow(),
        )
        embed.add_field(name="Role Name", value=after.name, inline=False)
        embed.add_field(name="Role ID", value=after.id, inline=False)
        embed.add_field(
            name="Changes",
            value="\n".join(changes) if changes else "No significant changes detected.",
            inline=False,
        )

        update_channel = self.bot.get_channel(config.ROLES_UPDATES_CHANNEL_ID)
        if update_channel:
            await update_channel.send(embed=embed)
            logger.info(
                "Role updated: %s (ID: %s). Changes: %s",
                after.name,
                after.id,
                ", ".join(changes) if changes else "No significant changes detected.",
            )


async def setup(bot):
    """Set up the RolesEvents cog.

    Args:
        bot (discord.ext.commands.Bot): The instance of the Discord bot.
    """
    await bot.add_cog(RolesEvents(bot))
