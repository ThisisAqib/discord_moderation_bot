import typing
import discord
import asyncio
import discord.ext
import discord.ext.commands
import settings
from discord.ext import commands

logger = settings.logging.getLogger("bot")

class ReactionsEvents(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        # Avoid logging the bot's own reactions
        if user.bot:
            return
        
        channel = reaction.message.channel

        embed = discord.Embed(
            title="Reaction Added",
            description=f"{user.mention} added a reaction.",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        )
        embed.add_field(name="Message", value=f"[Jump to message]({reaction.message.jump_url})", inline=False)
        embed.add_field(name="Channel", value=channel.mention, inline=False)
        embed.add_field(name="Emoji", value=str(reaction.emoji), inline=False)
        embed.add_field(name="User", value=user.mention, inline=False)

        update_channel = self.bot.get_channel(settings.REACTIONS_UPDATES_CHANNEL_ID)
        if update_channel:
            await update_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction: discord.Reaction, user: discord.User):
        # Avoid logging the bot's own reactions
        if user.bot:
            return

        channel = reaction.message.channel

        embed = discord.Embed(
            title="Reaction Removed",
            description=f"{user.mention} removed a reaction.",
            color=discord.Color.red(),
            timestamp=discord.utils.utcnow()
        )
        embed.add_field(name="Message", value=f"[Jump to message]({reaction.message.jump_url})", inline=False)
        embed.add_field(name="Channel", value=channel.mention, inline=False)
        embed.add_field(name="Emoji", value=str(reaction.emoji), inline=False)
        embed.add_field(name="User", value=user.mention, inline=False)

        update_channel = self.bot.get_channel(settings.REACTIONS_UPDATES_CHANNEL_ID)
        if update_channel:
            await update_channel.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_reaction_clear(self, message: discord.Message, reactions: typing.List[discord.Reaction]):
        channel = message.channel

        embed = discord.Embed(
            title="Reactions Cleared",
            description=f"Reactions were cleared from a message.",
            color=discord.Color.orange(),
            timestamp=discord.utils.utcnow()
        )
        embed.add_field(name="Message", value=f"[Jump to message]({message.jump_url})", inline=False)
        embed.add_field(name="Channel", value=channel.mention, inline=False)
        embed.add_field(name="Cleared Reactions", value=", ".join([str(reaction.emoji) for reaction in reactions]), inline=False)

        update_channel = self.bot.get_channel(settings.REACTIONS_UPDATES_CHANNEL_ID)
        if update_channel:
            await update_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ReactionsEvents(bot))
