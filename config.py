"""
Configuration module for loading environment variables and setting up bot settings.

This module loads environment variables from a .env file using the dotenv library.
It retrieves bot settings such as the bot token, guild ID, and channel IDs for various updates.
Additionally, it ensures that the logs directory exists for logging purposes.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Bot Settings
BOT_TOKEN: str = os.getenv("BOT_TOKEN")
GUILD_ID: int = int(os.getenv("GUILD_ID"))
DEFAULT_INVITE_CHANNEL_ID: int = int(os.getenv("DEFAULT_INVITE_CHANNEL_ID"))

# Channels for updates
CHANNELS_UPDATES_CHANNEL_ID: int = int(os.getenv("CHANNELS_UPDATES_CHANNEL_ID"))
GUILDS_UPDATES_CHANNEL_ID: int = int(os.getenv("GUILDS_UPDATES_CHANNEL_ID"))
MESSAGES_UPDATES_CHANNEL_ID: int = int(os.getenv("MESSAGES_UPDATES_CHANNEL_ID"))
MEMBERS_UPDATES_CHANNEL_ID: int = int(os.getenv("MEMBERS_UPDATES_CHANNEL_ID"))
REACTIONS_UPDATES_CHANNEL_ID: int = int(os.getenv("REACTIONS_UPDATES_CHANNEL_ID"))
ROLES_UPDATES_CHANNEL_ID: int = int(os.getenv("ROLES_UPDATES_CHANNEL_ID"))

# Ensure logs directory exists
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
