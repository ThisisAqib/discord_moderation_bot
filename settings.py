import os 
import pathlib
import logging
import discord
from logging.config import dictConfig
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))
DEFAULT_INVITE_CHANNEL_ID = int(os.getenv('DEFAULT_INVITE_CHANNEL_ID'))

CHANNELS_UPDATES_CHANNEL_ID = int(os.getenv('CHANNELS_UPDATES_CHANNEL_ID'))
GUILDS_UPDATES_CHANNEL_ID = int(os.getenv('GUILDS_UPDATES_CHANNEL_ID'))
MESSAGES_UPDATES_CHANNEL_ID = int(os.getenv('MESSAGES_UPDATES_CHANNEL_ID'))
MEMBERS_UPDATES_CHANNEL_ID = int(os.getenv('MEMBERS_UPDATES_CHANNEL_ID'))
REACTIONS_UPDATES_CHANNEL_ID = int(os.getenv('REACTIONS_UPDATES_CHANNEL_ID'))
ROLES_UPDATES_CHANNEL_ID = int(os.getenv('ROLES_UPDATES_CHANNEL_ID'))

BASE_DIR = pathlib.Path(__file__).parent

LOGGING_CONFIG = {
    "version": 1,
    "disabled_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)-10s - %(asctime)s - %(module)-15s : %(message)s"
        },
        "standard": {"format": "%(levelname)-10s - %(name)-15s : %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "console2": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "logs/infos.log",
            "mode": "w",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "bot": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "discord": {
            "handlers": ["console2", "file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

dictConfig(LOGGING_CONFIG)