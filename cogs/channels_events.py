import discord
import asyncio
import discord.ext
import discord.ext.commands
import settings
from discord.ext import commands

logger = settings.logging.getLogger("bot")

class ChannelsEvents(commands.Cog):
    def __init__(self, bot: discord.ext.commands.Bot) -> None:
        self.bot = bot 

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: discord.abc.GuildChannel):
        logger.info(f"Created {channel.name}, category: {channel.category}")

        embed = discord.Embed(
            title="Channel Created",
            description=f"Channel **{channel.mention}** was Created.",
            color=discord.Color.green()
        )

        category_name = channel.category.name if channel.category else "No Category"
        embed.add_field(name="Category", value=category_name)

        # Retrieve the channel to send the update
        channel_updates_channel = self.bot.get_channel(settings.CHANNELS_UPDATES_CHANNEL_ID)  # Replace with your channel ID
        if channel_updates_channel:
            await channel_updates_channel.send(embed=embed)
        else:
            logger.warning(f"Channel with ID {settings.CHANNELS_UPDATES_CHANNEL_ID} not found.")

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: discord.abc.GuildChannel):
        logger.info(f"Deleted {channel.name}, category: {channel.category}")    

        embed = discord.Embed(
            title="Channel Deleted",
            description=f"Channel **{channel.name}** was deleted.",
            color=discord.Color.red()
        )

        category_name = channel.category.name if channel.category else "No Category"
        embed.add_field(name="Category", value=category_name)

        # Retrieve the channel to send the update
        channel_updates_channel = self.bot.get_channel(settings.CHANNELS_UPDATES_CHANNEL_ID)  # Replace with your channel ID
        if channel_updates_channel:
            await channel_updates_channel.send(embed=embed)
        else:
            logger.warning(f"Channel with ID {settings.CHANNELS_UPDATES_CHANNEL_ID} not found.")
    

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before: discord.abc.GuildChannel, after: discord.abc.GuildChannel):
        changes = []
        
        # Get all attribute names
        all_attributes = set(dir(before)) | set(dir(after))
        
        # Filter out methods and private attributes
        all_attributes = [attr for attr in all_attributes if not callable(getattr(before, attr, None)) and not attr.startswith('_')]

        # Compare each attribute
        for attr in all_attributes:
            before_value = getattr(before, attr, None)
            after_value = getattr(after, attr, None)
            if before_value != after_value:
                changes.append(f"{attr} changed from '{before_value}' to '{after_value}'")

        # Output the changes
        if changes:
            logger.info(f"Channel '{before.mention}' was updated:")
            embed = discord.Embed(
                title="Channel Updated",
                description=f"Channel **{before.mention}** was updated.",
                color=discord.Color.orange()  # Color to signify an update
            )

            for change in changes:
                embed.add_field(name="Change Detected", value=change, inline=False)
                logger.info(f"  - {change}")
            
            # Retrieve the channel to send the update
            channel_updates_channel = self.bot.get_channel(settings.CHANNELS_UPDATES_CHANNEL_ID)  # Replace with your channel ID
            if channel_updates_channel:
                await channel_updates_channel.send(embed=embed)
            else:
                logger.warning(f"Channel with ID {settings.CHANNELS_UPDATES_CHANNEL_ID} not found.")
        else:
            logger.info(f"Channel '{before.name}' was updated, but no significant changes were detected.")
    

async def setup(bot):
    await bot.add_cog(ChannelsEvents(bot))
