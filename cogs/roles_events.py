import typing
import discord
import asyncio
import discord.ext
import discord.ext.commands
import settings
from discord.ext import commands

logger = settings.logging.getLogger("bot")

class RolesEvents(commands.Cog):
    def __init__(self, bot: discord.ext.commands.Bot) -> None:
        self.bot = bot 

    @commands.Cog.listener()
    async def on_guild_role_create(self, role: discord.Role):
        embed = discord.Embed(
            title="Role Created",
            description=f"A new role has been created.",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        )
        embed.add_field(name="Role Name", value=role.name, inline=False)
        embed.add_field(name="Role ID", value=role.id, inline=False)
        embed.add_field(name="Permissions", value=str(role.permissions), inline=False)
        embed.add_field(name="Position", value=role.position, inline=False)

        update_channel = self.bot.get_channel(settings.ROLES_UPDATES_CHANNEL_ID)
        if update_channel:
            await update_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: discord.Role):
        embed = discord.Embed(
            title="Role Deleted",
            description=f"A role has been deleted.",
            color=discord.Color.red(),
            timestamp=discord.utils.utcnow()
        )
        embed.add_field(name="Role Name", value=role.name, inline=False)
        embed.add_field(name="Role ID", value=role.id, inline=False)

        update_channel = self.bot.get_channel(settings.ROLES_UPDATES_CHANNEL_ID)
        if update_channel:
            await update_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_update(self, before: discord.Role, after: discord.Role):
        changes = []

        if before.name != after.name:
            changes.append(f"Name changed from '{before.name}' to '{after.name}'")
        if before.permissions != after.permissions:
            changes.append(f"Permissions changed from '{before.permissions}' to '{after.permissions}'")
        if before.position != after.position:
            changes.append(f"Position changed from '{before.position}' to '{after.position}'")

        embed = discord.Embed(
            title="Role Updated",
            description=f"Role '{after.name}' was updated.",
            color=discord.Color.orange(),
            timestamp=discord.utils.utcnow()
        )
        embed.add_field(name="Role Name", value=after.name, inline=False)
        embed.add_field(name="Role ID", value=after.id, inline=False)
        embed.add_field(name="Changes", value="\n".join(changes) if changes else "No significant changes detected.", inline=False)

        update_channel = self.bot.get_channel(settings.ROLES_UPDATES_CHANNEL_ID)
        if update_channel:
            await update_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(RolesEvents(bot))
