import discord
import asyncio
import discord.ext
import discord.ext.commands
import settings
from discord.ext import commands

logger = settings.logging.getLogger("bot")

class GuildsEvents(commands.Cog):
    def __init__(self, bot: discord.ext.commands.Bot) -> None:
        self.bot = bot 

    @commands.Cog.listener()
    async def on_invite_create(self, invite: discord.Invite):
        logger.info(f"Invite created: {invite.code} by {invite.inviter} for {invite.channel}")

        # Create an embed for the invite creation
        embed = discord.Embed(
            title="Invite Created",
            description=f"An invite code **{invite.code}** was created.",
            color=discord.Color.blue()  # Use blue to indicate creation
        )
        embed.add_field(name="Inviter", value=invite.inviter.mention if invite.inviter else "Unknown", inline=False)
        embed.add_field(name="Channel", value=invite.channel.mention if invite.channel else "Unknown", inline=False)
        
        max_age_value = f"{invite.max_age} seconds" if invite.max_age else "Never"
        embed.add_field(name="Max Age", value=max_age_value, inline=False)
        
        max_uses_value = str(invite.max_uses) if invite.max_uses > 0 else "Unlimited"
        embed.add_field(name="Max Uses", value=max_uses_value, inline=False)
        
        embed.add_field(name="Temporary Membership", value="Yes" if invite.temporary else "No", inline=False)
        embed.add_field(name="Uses", value=str(invite.uses), inline=False)
        embed.add_field(name="URL", value=invite.url, inline=False)
        
        if invite.target_type:
            embed.add_field(name="Target Type", value=str(invite.target_type), inline=False)
        
        if invite.target_user:
            embed.add_field(name="Target User", value=invite.target_user.mention if invite.target_user else "None", inline=False)
        
        if invite.target_application:
            embed.add_field(name="Target Application", value=invite.target_application.name, inline=False)
        
        if invite.expires_at:
            embed.add_field(name="Expires At", value=invite.expires_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        
        # Retrieve the channel to send the update
        invite_channel = self.bot.get_channel(settings.GUILDS_UPDATES_CHANNEL_ID)
        if invite_channel:
            await invite_channel.send(embed=embed)
        else:
            logger.warning(f"Channel with ID {settings.GUILDS_UPDATES_CHANNEL_ID} not found.")

    @commands.Cog.listener()
    async def on_invite_delete(self, invite: discord.Invite):
        logger.info(f"Invite deleted: {invite.code} for {invite.channel}")

        # Create an embed for the invite deletion
        embed = discord.Embed(
            title="Invite Deleted",
            description=f"An invite code **{invite.code}** was deleted.",
            color=discord.Color.red()
        )
        embed.add_field(name="Channel", value=invite.channel.mention if invite.channel else "Unknown", inline=False)

        # Retrieve the channel to send the update
        invite_channel = self.bot.get_channel(settings.GUILDS_UPDATES_CHANNEL_ID)
        if invite_channel:
            await invite_channel.send(embed=embed)
        else:
            logger.warning(f"Channel with ID {settings.GUILDS_UPDATES_CHANNEL_ID} not found.")


async def setup(bot):
    await bot.add_cog(GuildsEvents(bot))
