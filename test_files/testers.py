import asyncio
import discord
from discord.ext import commands

import config

from logger_init import logger

async def channels_tester(bot: commands.Bot):
    while True:
        try:
            logger.info(f"Running")
            guild = bot.get_guild(config.GUILD_ID)

            channels = guild.channels
            for channel in channels:
                if channel.name in ['test-channel', 'new-name']:
                    await channel.delete()

            channel = await guild.create_text_channel(name='test-channel')
            # logger.info(f"Created channel")
            await asyncio.sleep(5)

            # logger.info(f"Update channel")
            await channel.edit(name='new-name')
            await asyncio.sleep(5)

            # logger.info(f"Deleted channel")
            await channel.delete()
            await asyncio.sleep(5)

        except Exception as e:
            logger.error(e)
            break

async def guilds_tester(bot: commands.Bot):
    while True:
        try:
            logger.info(f"Running")
            guild = bot.get_guild(config.GUILD_ID)

            channel = guild.get_channel(config.DEFAULT_INVITE_CHANNEL_ID)
            invite = await channel.create_invite(
                max_age=1,
                max_uses=2,
                temporary=True
            )
            await asyncio.sleep(5)

            await invite.delete()
            await asyncio.sleep(5)


        except Exception as e:
            logger.error(e)
            break        


async def messages_tester(bot: commands.Bot):
    while True:
        try:
            logger.info(f"Running")
            guild = bot.get_guild(config.GUILD_ID)

            channel = guild.get_channel(1273237043572641824)
            message = await channel.send(content='Normal Text.')
            await asyncio.sleep(5)

            await message.edit(content='This is edited text.')
            await asyncio.sleep(5)

            await message.delete()
            await asyncio.sleep(5)


        except Exception as e:
            logger.error(e)
            break    
    

async def members_tester(bot: commands.Bot):
    while True:
        try:
            logger.info(f"Running")
            guild = bot.get_guild(config.GUILD_ID)


            # ## Create a welcome message
            # member = guild.get_member(454945968752951296)
            # embed = discord.Embed(
            #     title="Welcome!",
            #     description=f"Welcome to {member.guild.name}, {member.mention}! We're glad to have you here.",
            #     color=discord.Color.green()
            # )
            
            # # Add member's profile picture as a thumbnail
            # embed.set_thumbnail(url=member.avatar.url)

            # # Send the welcome message to the specified channel
            # welcome_channel = bot.get_channel(settings.MEMBERS_UPDATES_CHANNEL_ID)
            # if welcome_channel:
            #     await welcome_channel.send(embed=embed)
            # else:
            #     logger.warning(f"Channel with ID {settings.MEMBERS_UPDATES_CHANNEL_ID} not found.")
            
            # ## ban member
            # # Fetch member from API if not found in cache
            # try:
            #     member = await guild.fetch_member(939424644799266828)
            #     if member:
            #         await member.ban(reason="Test ban reason")
            # except discord.NotFound:
            #     logger.info("Member not found in the guild.")
            # except discord.Forbidden:
            #     logger.info("Missing permissions to fetch the member.")
            # except discord.HTTPException as e:
            #     logger.error(f"Failed to fetch member: {e}")

            # await asyncio.sleep(1)


            ## unban member
            try:
                # Fetch the user from Discord API
                user = await bot.fetch_user(939424644799266828)
                if user:
                    # Attempt to unban the user from the guild
                    await guild.unban(user, reason="Test unban reason")
                    logger.info(f"Unbanned user {user} ({user.id}) from {guild.name}.")
                else:
                    logger.info("User not found.")
            except discord.NotFound:
                logger.info("User not found.")
            except discord.Forbidden:
                logger.info("Missing permissions to unban the user.")
            except discord.HTTPException as e:
                logger.error(f"Failed to unban user: {e}")

            # ## change bot name
            # new_name = 'new_namee321'
            # try:
            #     await bot.user.edit(username=new_name)
            #     print(f"Bot name changed to {new_name}")
            # except discord.HTTPException as e:
            #     print(f"Failed to change bot name: {e}")


            # # give role
            # member = guild.get_member(939424644799266828)
            # role = guild.get_role(1274961239235362977)
            # await member.add_roles(role)
            # await asyncio.sleep(5)
            # await member.remove_roles(role)
            


            await asyncio.sleep(5)

            # break


        except Exception as e:
            logger.error(e)
            break    